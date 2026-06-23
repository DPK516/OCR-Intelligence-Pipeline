### Step 1:

Installed PyMuPDF to process scanned PDFs and convert pages into images for OCR.
written a Python script pdf_to_image.py that takes a PDF file, chops it up page-by-page, and saves each page as a high-quality picture (a PNG file).

Installed OpenCV to handle the image editing, and NumPy , which OpenCV relies on under the hood to calculate the pixel changes.
written a script clean_image.py that takes the raw images we just generated and mathematically cleans them up. It will turn them black and white, erase shadows, and sharpen the text.
