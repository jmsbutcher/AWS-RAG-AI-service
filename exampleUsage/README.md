# AWS RAG AI Service

### An AWS Bedrock chatbot service that answers questions about my knowledge base with natural language.

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

#### Main steps:

1. Create main Python application for creating vector database, handling queries, etc. (followed tutorial for this part.)
2. **Populate the database** with the source PDF documents for the Chatbot to use. I used the AI Knowledge Base RDF graph string representation I created in one of my other projects: (AIKB)[https://github.com/jmsbutcher/AI-Knowledge-Base]
3. **Create Docker** image for running the app on AWS.
4. **Deploy the image** to AWS lambda using AWS CDK.
5. **Set up Bedrock service on AWS** - I chose Meta's Llama 3 8B Instruct model due to its very low cost ($0.00022 per 1000 tokens) and its superior performance over Anthropic's comparable model Claude when I tested it.
6. **Test the service** using my (AIKB)[https://github.com/jmsbutcher/AI-Knowledge-Base] project.

### Usage


   

