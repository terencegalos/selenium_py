import pytesseract
from pdf2image import convert_from_path
import os

pdf_path = 'C:/Users/Berries/Code/downloads/CHC Wholesale Order Form.2023.pdf'

pages = convert_from_path(pdf_path)

text = ''
for i,page in enumerate(pages):
    text += pytesseract.image_to_string(page)

print(text)
with open('pytesseract.txt','w') as file:
    file.write(text)