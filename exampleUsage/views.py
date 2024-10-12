from flask import Blueprint, render_template, request, session
import requests

views = Blueprint('views', __name__)



@views.route('/query-rag', methods=['GET', 'POST'])
def query_rag():
    """
    Query Knowledge Base Chatbot

    - Ask a natual-language question about the knowledge base to a chatbot

    Uses a RAG AI service running on AWS bedrock.
    """
    ROOT_URL = "https://mhkyeven3e3yrdzqa36g443c4q0xyqkm.lambda-url.us-east-1.on.aws/"
    answer = "-"
    if (session.get("last_query_id") is not None):
        print("Last question ID: [", session["last_query_id"], "]")
    else:
        session["last_query_id"] = ""
        print("Set last query ID to empty.")

    # When "Enter" button is pressed:
    if request.method == 'POST':

        # Get the question asked by the user
        question = request.form.get('question')

        #------------------------------------------------------------------------------
        # Send submit query POST request to route "/docs/submit_query"
        SUBMIT_QUERY_URL = ROOT_URL + "submit_query/"
        query_contents = {
            "query_text": question
        }

        response = requests.post(SUBMIT_QUERY_URL, json = query_contents)
        query_id = response.json()["query_id"]
        session["last_query_id"] = query_id

        #------------------------------------------------------------------------------
        # Wait to receive answer via GET request to route "/docs/get_query"
        import time
        GET_QUERY_URL = ROOT_URL + "get_query/"
        is_complete = False
        timeout_in_s = 120
        time_in_s = 0

        while not is_complete or time_in_s > timeout_in_s:
            # Wait for answer
            time.sleep(3)
            time_in_s += 3
            print("Waiting for answer...", time_in_s)

            query_contents = {
                "query_id": query_id
            }

            response = requests.get(GET_QUERY_URL, params = query_contents)

            is_complete = response.json()["is_complete"]
            if (is_complete):
                answer = response.json()["answer_text"]
            elif (time_in_s > timeout_in_s):
                print("Timeout.")
                

    elif session["last_query_id"] != "":
        GET_QUERY_URL = ROOT_URL + "get_query/"
        query_contents = {
            "query_id": session["last_query_id"]
        }
        response = requests.get(GET_QUERY_URL, params = query_contents)
        is_complete = response.json()["is_complete"]
        if (is_complete):
            answer = response.json()["answer_text"]


    # Pass all the values and results (if any) to the query template to be displayed
    return render_template('query-rag.html', answer=answer)

