import boto3, json
from database_functions import storeEmbedding


client = boto3.client('bedrock-runtime', region_name='us-east-1')

def generateEmbeddings(conn, cursor, pages: list):

    allEmbeddings = []  # list of objects representing each page  

    for i, page in enumerate(pages):
        
        text = page['text']

        request_body = {
                'inputText': text,
                'dimensions': 512, 
                'normalize': True  # normalization eliminates vector magnitude influencing similarity comparison
        }

        try:  # have to call api for each page.  does not support batch processing.  very inefficient 
            response = client.invoke_model(
                modelId = 'amazon.titan-embed-text-v2:0',
                contentType = 'application/json',
                accept = 'application/json', 
                body = json.dumps(request_body)
            )

            response_body = json.loads(response['body'].read())

            embedding = response_body['embedding']

            allEmbeddings.append(  # add object representing each page with metadata to list
                {
                    'embedding': embedding,
                    'pdf_path': page['pdf_path'],
                    'page_number': page['page_number'],
                    'text': text[:100]  # just a preview of the contents of the page
                }
            )
            
            storeEmbedding(conn, cursor, page['pdf_path'], page['page_number'], embedding)  # store embedding in sql db 

        except Exception as e: 
            print(f'Error page {i+1}: {e}')


    print(f'{page['pdf_path']} embedded.')

    return allEmbeddings



def embedQuery(search_query):

    try: 
        request_body = {
                'inputText': search_query,
                'dimensions': 512, 
                'normalize': True
        }

        response = client.invoke_model(
            modelId = 'amazon.titan-embed-text-v2:0',
            contentType = 'application/json',
            accept = 'application/json', 
            body = json.dumps(request_body)
        )

        response_body = json.loads(response['body'].read())

        query_vector = response_body['embedding']

        return query_vector

    except Exception as e: 
        print(f'Error embeddding search query ({search_query}): {e}')


    





