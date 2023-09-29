import json
from aiohttp import ClientError
import requests
import boto3

def lambda_handler(event, context):
    # Retrieve OpenAI API Key from environment variables
    api_key = get_secret()
    
    # Retrieve the question from the event object
    question = event.get('question')
    
    # Add any additional context and policy here
    context = "Create a legal document as descriped in the prompt"
    policy = "Some policy information here."
    
    # Construct the prompt by combining question, context, and policy
    prompt = f"{context}\n\n{policy}\n\n{question}"
    
    # Define OpenAI API endpoint
    url = "https://api.openai.com/v1/engines/davinci-codex/completions"
    
    # Set up the API call headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # Define the API call payload
    payload = {
        "prompt": prompt,
        "max_tokens": 100, # You can adjust max_tokens as per your requirements
    }
    
    # Make the API call
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    # Check if the API call was successful
    if response.status_code == 200:
        # Return the API response
        return {
            "statusCode": 200,
            "body": json.dumps(response.json())
        }
    else:
        # Return an error response
        return {
            "statusCode": response.status_code,
            "body": "Error calling OpenAI API"
        }


def get_secret():

    secret_name = "OpenAPIKey"
    region_name = "us-east-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    return secret
