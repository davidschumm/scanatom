from PIL import Image

image1 = Image.open(r'walmart.jpg')
im1 = image1.convert('RGB')
im1.save(r'pdfpic.pdf')