import faiss, numpy as np, pickle


def searchPDF(cursor, query: list):

    # retrieve all embeddings and metadata from database
    cursor.execute('SELECT pdf_path, page_number, embedding FROM embeddings')
    rows = cursor.fetchall() # returns list of tuples representing each row in the result set

    if not rows:
        print('No embeddings found in the database.')
        return 


    # separate embeddings and metadata
    embeddings = []
    metadata = []

    for row in rows:
        # destructure each row into three variables with respective values 
        pdf_path, page_number, embedding_blob = row 

        embedding = pickle.loads(embedding_blob) # deserialize the embedding
        embeddings.append(embedding)

        metadata.append(
            {
                'pdf_path': pdf_path, 
                'page_number': page_number
            }
        )


    # create FAISS index 
    embeddings = np.array(embeddings, dtype='float32') # FAISS expects vectors to be float32 format
    dimensionality = embeddings.shape[1] # check dimensionality of vectors
    
    index = faiss.IndexFlatIP(dimensionality) # create index using inner product to work with cosine similarity
    index.add(embeddings) # add embeddings to index

    queryVector = np.array(query, dtype='float32')


    # FAISS search needs 2 dimensional arrays so if its 1D, reshape to 2D
    if queryVector.ndim == 1:  
        queryVector = queryVector.reshape(1, -1)  # reshapes to 2D


    # search embeddings index for similarity to query vector, return 5 closest matches
    distances, indices = index.search(queryVector, k=5) 
    '''
        distances are lists of the cosine similarity scores
        indices are the indexes of the closest vectors to the query vector in the embeddings list.  the k parameter determines
        the number of indices that are returned.  (k=5 means 5 closest vectors.)
    '''

    results = []

    for i, indice in enumerate(indices[0]):  
        result = {
            'pdf_path': metadata[indice]['pdf_path'],
            'page_number': metadata[indice]['page_number'],
            'cosine_similarity': distances[0][i], 
            'embedding': embeddings[indice]
        }
        
        results.append(result)

    '''
        FAISS search can handle multiple queries per search and returns distances and indices as 2d arrays 
        so distances[0] and indices[0] refers to the results of the first query in your search.
        if you were to add more queries than you would just increment that index for the query results you're looking for. 
    '''

    return results
    
    