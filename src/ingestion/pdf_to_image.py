import fitz 
import os

def convert_pdf_to_images(pdf_path, output_folder, zoom=2.0):
    """
    Takes a PDF and saves each page as a high-res PNG image.
    """
    
    pdf_document = fitz.open(pdf_path)
    
    
    os.makedirs(output_folder, exist_ok=True)
    
    print(f"Opening {pdf_path}...")
    
    
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        
        # Zoom in to make the image high resolution (CRITICAL for AI OCR)
        matrix = fitz.Matrix(zoom, zoom)
        pixel_map = page.get_pixmap(matrix=matrix)
        
        
        output_filename = f"page_{page_number + 1}.png"
        output_filepath = os.path.join(output_folder, output_filename)
        
        
        pixel_map.save(output_filepath)
        print(f"Saved: {output_filename}")
        
    print(f"Success! Converted {len(pdf_document)} pages to images.")


if __name__ == "__main__":
    
    INPUT_PDF = "data/input_pdfs/sample.pdf"
    OUTPUT_DIR = "data/raw_images"
    
    if os.path.exists(INPUT_PDF):
        convert_pdf_to_images(INPUT_PDF, OUTPUT_DIR)
    else:
        print(f"Waiting for a test file! Please place a PDF named 'sample.pdf' in the data/input_pdfs/ folder.")