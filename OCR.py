import pytesseract
import pdf2image
from PIL import Image
import fitz
import os

# print pytesseract.image_to_string(Image.open('C:\Users\Berries\Desktop\mccals.pdf'))
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files(x86)\Tesseract-OCR\tesseract'

def PDF2ImgConvert(pages):
    counter = 1
    result = []
    for page in pages:
        filename = "C:\Users\Berries\Desktop\images\page_"+str(counter)+".jpg"
        page.save(filename,'JPEG')
        result.append(filename)
        counter = counter + 1

    return result




def fitzconvert(file):

    doc = fitz.open(file)

    if not os.path.isdir(outfile):
        os.path.mkdir(outfile)

    for x in range(1,84):
        out = outfile+"page_"+str(x)+".png"
        page = doc.loadPage(x)
        pix = page.getPixmap()
        pix.writePNG(out)

def ocrconvert():
    files = os.listdir(outfile)
    print outfile

    with open(ocr+"OCR.txt","wb") as infile:
        for x in range(len(files)):
            txt = pytesseract.image_to_string(Image.open(outfile+files[x]))
            print txt.encode("utf-8")
            infile.write(txt.encode("utf-8"))

def test():
    pix = Image.open(invoice)
    txt = pytesseract.image_to_string(pix)
    print txt.encode("utf8")
    with open("C:\Users\Berries\Desktop\OCR.txt","wb") as infile:
        infile.write(txt.encode("utf-8"))





best = "C:/Users/Berries/Downloads/Documents/Best-Sellers_8-7-2020_PRINT.pdf"
clearance = r'C:/Users/Berries/Downloads/Documents/2020_Clearance_8-3-2020_PRINT.pdf'







outfile = r'C:\\Users\Berries\Desktop\\Images\\'
ocr = r'C:\\Users\Berries\Desktop\\'
invoice = r'C:\\Users\Berries\Desktop\invoice-sample.png'


def main():
    # pages = pdf2image.convert_from_path(poppler_path=r'C:\Program Files\Poppler\bin',clearance,500)
    # pages = pdf2image.convert_from_path(clearance,500)

    # images = PDF2ImgConvert(pages)

    # f = open(outfile,"a")
    # for image in images:
    #     text = pytesseract.image_to_string(Image.open(image))
    #     text = text.replace("\n",'')
    # f.close()
    
    # fitzconvert(clearance)
    ocrconvert()
    # test()





if __name__ == "__main__":
    main()    