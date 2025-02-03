import pickle

def storeEmbedding(conn, cursor, pdf_path, page_number, embedding):

    try:
        # INSERT OR IGNORE handles duplicates
        cursor.execute( 
        '''
            INSERT OR IGNORE INTO embeddings (pdf_path, page_number, embedding)
            VALUES (?, ?, ?)
        ''', (pdf_path, page_number+1, pickle.dumps(embedding)) # pickle.dumps for serializing the embedding
        )
        conn.commit()

    except Exception as e:
        print(f'Error storing in db: {e}')


def isPDFinDB(cursor, pdf_path):
    cursor.execute('SELECT COUNT(*) FROM embeddings WHERE pdf_path = ?', (pdf_path,))
    count = cursor.fetchone()[0] # number of matches

    return count > 0  # returns true if pdf path in db


