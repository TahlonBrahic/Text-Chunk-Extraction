import PyPDF2
import pytesseract
import cv2
import os
from pdf2image import convert_from_path

# encoded text extraction
def extract_encoded_pdf_text(pdf_file, page_start, page_end):
    pdf = PyPDF2.PdfFileReader(pdf_file)
    text = ''
    for page_num in range(page_start, page_end):
        text += pdf.getPage(page_num).extract_text()
    return text

# scanned text extraction
def extract_pdf_to_images(pdf_file, page_start, page_end, image_dir='C:/Users/Tahlon/Desktop'):
    pages = convert_from_path(pdf_file, dpi=300)
    for i, page in enumerate(pages[page_start:page_end]):
        image_path = f"{image_dir}/page{i + page_start}.jpg"
        page.save(image_path, 'JPEG')

def extract_text_from_image(image_dir='C:/Users/Tahlon/Desktop'):
    text = ''
    for image_file in os.listdir(image_dir):
        if image_file.endswith('.jpg'):
            image_path = os.path.join(image_dir, image_file)
            image = cv2.imread(image_path)    
            text += pytesseract.image_to_string(image) + '\n'
    
    return text

# chunk processing and file saving
def split_text(text, chunk_size):
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
    with open(filename, 'w') as f:
        for chunk in chunks:
            f.write(chunk + '\n')

# processing 
def extraction_method():
    return input("Enter extraction method: 'scanned' or 'encoded' ")

# user input
def user_input(extraction_method):
    pdf_file = input("Enter the PDF's directory': ")
    page_start = int(input("Enter the starting page number: "))
    page_end = int(input("Enter the ending page number: "))
    chunk_size = int(input("Enter the desired chunk size (in words): "))
    filename = input("Enter the text file name: ")

    text = ''
    if extraction_method == 'encoded':
        try:
            text = extract_encoded_pdf_text(pdf_file, page_start, page_end)
        except:
            print("File could not be found.")
    elif extraction_method == 'scanned':
        try:
            extract_pdf_to_images(pdf_file, page_start, page_end)
            for page_num in range(page_start, page_end):
                text += extract_text_from_image(page_num=page_num)
        except: 
            print("File could not be found.")
    chunks = split_text(text, chunk_size)
    save_text_to_file(chunks, filename) 


# program
if __name__ == '__main__':
    user_input(extraction_method())
    print('Your file has been sent to your local directory.')
