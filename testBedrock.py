# James Butcher
# 9/23/24
#
# Test out invoking bedrock models and formatting payloads.
# Using guidance from tutorial: 
# "Amazon Bedrock Tutorial: Generative AI on AWS" by Pixegami
# https://www.youtube.com/watch?v=kwkaBrK_-Bs
#
# I decided to use Llama3-8b-instruct instead of Claude because it is
# a lot cheaper and I think it's performace was actually much better
# than Claude when I tested side-by-side on the prompt "Describe the
# theme of Atlas Shrugged".

import boto3
import json

prompt_data = """
Write a one-liner 90s style B-movie horror/comedy pitch about 
a giant man-eating Python,
with a hilarious and surprising twist.
"""


bedrock = boto3.client(service_name="bedrock-runtime")


# Claude

# model_id = "anthropic.claude-v2"
# payload = {
#     "prompt": f"\n\nHuman:{prompt_data}\n\nAssistant:",
#     "max_tokens_to_sample": 512,
#     "temperature": 0.8,
#     "top_p": 0.8,
# }



# Llama

model_id = "meta.llama3-8b-instruct-v1:0"
payload = {
    "prompt": f"\n\nHuman:{prompt_data}\n\nAssistant:",
    "max_gen_len": 512,
    "temperature": 0.8,
    "top_p": 0.8,
}


body = json.dumps(payload)
response = bedrock.invoke_model(
    body=body,
    modelId=model_id,
    accept="application/json",
    contentType="application/json",
)


response_body = json.loads(response.get("body").read())
print("----------------")
print(response_body)
print("----------------")
response_text = response_body.get("generation")
print(response_text)
print("----------------")
