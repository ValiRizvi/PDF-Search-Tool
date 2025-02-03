import os, sqlite3
from database_functions import isPDFinDB
from process_pdf import textExtraction
from embed import generateEmbeddings, embedQuery
from search import searchPDF
from call_bedrock import callBedrock
from pathlib import Path


conn = sqlite3.connect('pdf_embeddings.db')
cursor = conn.cursor()

# any pdfs in the 'pdfs' folder will be loaded / embedded.  any previously embedded pdfs will be skipped. 
pdf_folder = 'pdfs'
# combine file path of pdf folder with names of each pdf for complete file paths 
pdf_paths = [os.path.join(pdf_folder, file_name) for file_name in os.listdir(pdf_folder) if file_name.endswith('.pdf')]

if not pdf_paths: # exit program if there are no pdfs to process
    print(f'no pdf files found.')
    exit()

# loop through each pdf 
for pdf_path in pdf_paths:
    print(f'Processing {pdf_path}')

    if not isPDFinDB(cursor, pdf_path):  # if pdf isnt found in the db
        pages = textExtraction(pdf_path)  # extract all the page texts
        print(f'Extracted {len(pages)} pages from {pdf_path}')

        print(f'Embedding {pdf_path}...')
        embeddings = generateEmbeddings(conn, cursor, pages)  # embed each page and store in db

    else:
        print(f'{pdf_path} previously processed.')


search_query = input('Search: ')  # user enters a question
query_vector = embedQuery(search_query)  # embed users query

results = searchPDF(cursor, query_vector)  # returns results of FAISS cosine similarity search (5 most relevant pdf pages)


# extract text from pages returned by similarity search 
result_texts = []
references = ''  # page references for client to view

for result in results: 
    result_texts.append(textExtraction(result['pdf_path'], result['page_number']))

    pdf_name = Path(result['pdf_path']).stem  # extract pdf name from file path with pathlib
    references += f'\n{pdf_name}, pg. {result['page_number']}'  # concatenate all references as strings for easy printing

context = '\n\n'.join(result_texts)  # context for bedrock prompt to answer search query
#print(context)

for i, result in enumerate(results):
    print(f'Result {i+1}:')
    print(f'PDF Path: {result["pdf_path"]}')
    print(f'Page Number: {result["page_number"]}')
    print(f'Cosine Similarity: {result["cosine_similarity"]:.4f}')  # limit to 4 decimal places
    print('-' * 50) 


response = callBedrock(result_texts, search_query)

print(response)
print(f'\n\nFor more information reference: {references}')