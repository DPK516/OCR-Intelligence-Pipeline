import os
import glob
import re      
import time    
from src.ingestion.pdf_to_image import convert_pdf_to_images
from src.ocr_engine.extract_text import extract_text_from_image
from src.postprocessing.vision_correction import correct_text_with_vision
from src.export.builder import create_word_document

def run_pipeline():
    print("===========================================")
    print("   STARTING LAYOUT-AWARE OCR PIPELINE")
    print("===========================================\n")

    INPUT_PDF = "data/input_pdfs/sample.pdf"
    RAW_IMAGES_DIR = "data/raw_images"
    
    if not os.path.exists(INPUT_PDF):
        print(f"ERROR: Cannot find {INPUT_PDF}. Please add a PDF to process.")
        return

    print("--- STEP 1: Converting PDF to Images ---")
    convert_pdf_to_images(INPUT_PDF, RAW_IMAGES_DIR)

    print("\n--- STEP 2: Extracting Text, Typography, & Layout ---")
    raw_files = glob.glob(os.path.join(RAW_IMAGES_DIR, "*.png"))
    
    
    image_files = sorted(raw_files, key=lambda x: int(re.findall(r'\d+', os.path.basename(x))[0]))
    
    all_structured_pages = []

    for image_path in image_files:
        filename = os.path.basename(image_path)
        print(f"\nProcessing {filename}...")
        
        raw_text = extract_text_from_image(image_path)
        
        if raw_text:
            result = correct_text_with_vision(image_path, raw_text)
            all_structured_pages.append(result)
        else:
            all_structured_pages.append({
                "page_layout_corrected": [{
                    "type": "paragraph", 
                    "alignment": "left",
                    "font_style": "sans-serif",
                    "text_spans": [{"text": "[Extraction Error]", "bold": False, "italic": False}]
                }]
            })
            
        
        print("Pausing for 10 seconds to respect API limits...")
        time.sleep(10) 

    print("\n--- STEP 3: Assembling Styled Word Document ---")
    if all_structured_pages:
        create_word_document(all_structured_pages, "Final_Digitized_Output.docx")
    else:
        print("No pages processed, skipping document assembly.")

    print("\n===========================================")
    print(" PIPELINE COMPLETE.")
    print("===========================================")

if __name__ == "__main__":
    run_pipeline()