import json
import openai

def lambda_handler(event, context):
    data = json.loads(event['body'])
    response = openai.ChatCompletion.create(
      model="gpt-4.0-turbo",
      messages=[
            {"role": "system", "content": data['context']},
            {"role": "user", "content": data['query']}
        ]
    )
    return {
        'statusCode': 200,
        'body': json.dumps(response.choices[0].message['content']),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'  # adjust this in production
        }
    }