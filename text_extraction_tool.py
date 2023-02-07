import PyPDF2

def extract_pdf_text(pdf_file, page_start, page_end):
    # Open the PDF file and extract text
    pdf = PyPDF2.PdfFileReader(pdf_file)
    text = ''
    for page_num in range(page_start, page_end):
        text += pdf.getPage(page_num).extract_text()
    return text

def split_text(text, chunk_size):
    # Split the text into chunks of a given size
    chunks = []
    current_chunk = ''
    words = text.split()
    for word in words:
        if len(current_chunk) + len(word) <= chunk_size:
            current_chunk += word + ' '
        else:
            chunks.append(current_chunk)
            current_chunk = word + ' '
    chunks.append(current_chunk)
    return chunks

def save_text_to_file(chunks, filename):
    # Save the text chunks to a text file
    with open(filename, 'w') as f:
        for chunk in chunks:
            f.write(chunk + '\n')

if __name__ == '__main__':
    pdf_file = input("Enter the PDF's directory': ")
    page_start = int(input("Enter the starting page number: "))
    page_end = int(input("Enter the ending page number: "))
    chunk_size = int(input("Enter the desired chunk size (in words): "))
    filename = input("Enter the text file name: ")

    text = extract_pdf_text(pdf_file, page_start, page_end)
    chunks = split_text(text, chunk_size)
    save_text_to_file(chunks, filename) 