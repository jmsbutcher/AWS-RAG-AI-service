# AWS RAG AI Service

### An AWS Bedrock chatbot service that answers questions within the context a knowledge base using natural language.

[Try it here](https://aikb-bfe2tw67tq-ue.a.run.app/query-rag)

The purpose of this project was to learn how to deploy an AI service to to the cloud and use it from another web application.

The main part of the work can be credited to Pixegami and his very helpful tutorial video https://www.youtube.com/watch?v=ldFONBo2CR0
The original source code for the core of the application is located here: https://github.com/pixegami/deploy-rag-to-aws/tree/main

It consists of a RAG application that allows you to ask questions about the information contained in a document.

According to Google: "**RAG (Retrieval-Augmented Generation)** is an AI framework that combines the strengths of traditional information retrieval systems (such as search and databases) with the capabilities of generative large language models (LLMs)." (https://cloud.google.com/use-cases/retrieval-augmented-generation)

For example, you could ask the service a question like:
<br>
"What are the pros and cons of decision trees?" 

and it would respond with something like: 
<br>
"Based on the provided context, the pros of decision trees are: 
* Can deal with data where features interact with each other
* Can deal with large, complicated, differently-scaled data
* Can deal with non-linear data
* Creates good explanations
* Interpretable
  
The cons of decision trees are:
* Fails to deal with linear relationships without adding splits, which is inefficient
* Lack of smoothness; slight changes in an input feature can have a big impact on the predicted outcome
* Only easily interpretable when short
* Unstable"
  
(This information was taken directly from the knowledge base I provided to it.)

<br>

### Architecture overview:

<p align="center">
  <img src="https://github.com/jmsbutcher/AWS-RAG-AI-service/blob/main/readmeImages/architectureDiagram.png">
</p>
Adapted from Pixegami https://www.youtube.com/watch?v=ldFONBo2CR0

#### Main steps:

1. Create main Python application for creating vector database, handling queries, etc. (followed tutorial for this part.)
2. **Populate the database** with the source PDF documents for the Chatbot to use. I used the AI Knowledge Base RDF graph string representation I created in one of my other projects: [AIKB](https://github.com/jmsbutcher/AI-Knowledge-Base)
3. **Create Docker** image for running the app on AWS.
4. **Deploy the image** to AWS Lambda using AWS CDK. AWS Lambda is a serverless architecture, meaning it only runs when it receives a request, allowing it to be very low cost.
5. **Set up Bedrock service on AWS** - I chose Meta's Llama 3 8B Instruct model due to its very low cost ($0.00022 per 1000 tokens) and its superior performance over Anthropic's comparable model Claude when I tested it.
6. **Test the service** using my [AIKB](https://github.com/jmsbutcher/AI-Knowledge-Base) project, a Flask app that queries the service using the requests library hosted on Google Cloud.

### Usage

<p align="center">
  <img src="https://github.com/jmsbutcher/AWS-RAG-AI-service/blob/main/readmeImages/usageScreenshot.png">
</p>

[Try it here](https://aikb-bfe2tw67tq-ue.a.run.app/query-rag)

I put two files in the "exampleUsage" folder showing how I called the RAG service from another app.

In views.py, the 'query-rag' POST route is called when the user types a query into the entry box and clicks "Enter":

```python
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
```

This submits the query to the model, which then begins crafting a response. The client app then waits for a response by checking the 'is_complete' field, and when it is complete it passes the answer text to the HTML template "query-rag.html" to be displayed on the webpage.

```python
        # ...

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
```

```html
<form method="POST">
    <div class="row mb-3">
        <label for="question" class="col-sm-2 col-form-label">Question:</label>
        <div class="col-sm-10">
            <input type="text"
                class="form-control"
                id="question"
                name="question"
                placeholder="Enter your question"
                aria-describedby="questionInputHelp"/>
            <div id="questionInputHelp" class="form-text">
                (e.g., What are the pros and cons of decision trees?)
            </div>
        </div>
    </div>
    <button type="submit" class="btn btn-primary">Enter</button>
</form>

<br/>

<div class="container">
    <h4>Answer:</h4>
    <p>{{ answer }}</p>
</div>
```
   
10/12/24
(c) James Butcher
