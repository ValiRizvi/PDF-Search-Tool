import boto3, json  

client = boto3.client('bedrock-runtime', region_name='us-east-1')

def callBedrock(texts, search_query):

    model_id = 'anthropic.claude-3-haiku-20240307-v1:0'

    context = '\n\n'.join(texts)

    # prompt is roughly 1000-1500 tokens.  output is about 150-250 tokens. 
    prompt = ( 
        'You are an AI assistant that briefly answers client questions based on the provided information.'
        'Use only the given text to formulate your response. If the answer is not in the provided texts, say so.'
        f'Context: {context}'
        f'Client Question: {search_query}'
    )

    native_request = {
        'anthropic_version': 'bedrock-2023-05-31',
        'max_tokens': 500,
        'temperature': 0.5,
        'messages': [
            {
                'role': 'user', 
                'content': [
                    {
                        'type': 'text', 
                        'text': prompt
                    }
                ]
            }
        ],
    }

    request = json.dumps(native_request)
    response = client.invoke_model(modelId=model_id, body=request)

    model_response = json.loads(response['body'].read())
    response_text = model_response['content'][0]['text']
    
    return response_text
