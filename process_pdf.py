import pymupdf 


def textExtraction(pdf_path, page_number):
    pdf = pymupdf.open(pdf_path)

    # returns all pages
    if not page_number: 
        pages = []

        for i, page in enumerate(pdf): 
            text = page.get_text() # pymupdf module function to get text from a pdf 

            pages.append(
                {
                    'pdf_path': pdf_path,
                    'page_number': i,
                    'text': text
                }
            )

        pdf.close()

        return pages
    
    # return specific page text only if page number parameter is provided
    page = pdf[page_number-1] # pdf is zero indexed
    text = page.get_text()
    pdf.close()

    return text





    