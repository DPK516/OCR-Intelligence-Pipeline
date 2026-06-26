import os
import glob
from src.ingestion.pdf_to_image import convert_pdf_to_images
from src.ocr_engine.extract_text import extract_text_from_image
from src.postprocessing.vision_correction import correct_text_with_vision
from src.export.builder import create_word_document

def run_pipeline():
    print("===========================================")
    print("   STARTING INTELLIGENT OCR PIPELINE")
    print("===========================================\n")

    
    INPUT_PDF = "data/input_pdfs/sample.pdf"
    RAW_IMAGES_DIR = "data/raw_images"
    
    if not os.path.exists(INPUT_PDF):
        print(f"ERROR: Cannot find {INPUT_PDF}. Please add a PDF to process.")
        return

    print("--- STEP 1: Converting PDF to Images ---")
    convert_pdf_to_images(INPUT_PDF, RAW_IMAGES_DIR)

    
    print("\n--- STEP 2: Extracting & Cleaning Text ---")
    image_files = sorted(glob.glob(os.path.join(RAW_IMAGES_DIR, "*.png")))
    
    all_cleaned_pages = [] 
    for image_path in image_files:
        filename = os.path.basename(image_path)
        print(f"\nProcessing {filename}...")
        
        
        raw_text = extract_text_from_image(image_path)
        
        
        if raw_text:
            result = correct_text_with_vision(image_path, raw_text)
            clean_text = result.get("final_corrected_text", "")
            all_cleaned_pages.append(clean_text)
        else:
            all_cleaned_pages.append("[Error extracting text for this page]")

    
    print("\n--- STEP 3: Assembling Final Document ---")
    if all_cleaned_pages:
        
        create_word_document(all_cleaned_pages, "Final_Digitized_Output.docx")
    else:
        print("No text was extracted, skipping document creation.")

    print("\n===========================================")
    print(" PIPELINE COMPLETE.")
    print("===========================================")

if __name__ == "__main__":
    run_pipeline()