import os
import glob
from src.ocr_engine.extract_text import extract_text_from_image
from src.postprocessing.vision_correction import correct_text_with_vision

def run_test():
    
    input_directory = "data/raw_images"
    image_files = glob.glob(os.path.join(input_directory, "*.png"))
    

    print(f"Found {len(image_files)} images. Starting the structured pipeline test...\n")
    
    for image_path in image_files:
        filename = os.path.basename(image_path)
        print(f"========== PROCESSING: {filename} ==========")
        
        
        print("1. Extracting raw text...")
        raw_text = extract_text_from_image(image_path)
        
        if not raw_text:
            print("Failed to get raw text. Skipping to next image.")
            continue
            
        print("--- Raw Text Snippet ---")
        print(raw_text[:200] + "...\n") 
        
        
        print("2. Sending to Vision Proofreader for corrections and audit trail...")
        
        result = correct_text_with_vision(image_path, raw_text) 
        
        print("\n" + "="*40)
        print("--- FINAL CORRECTED TEXT ---")
        
        print(result.get("final_corrected_text", "No text found."))
        
        print("\n--- AUDIT TRAIL (ERROR LOG) ---")
        error_log = result.get("error_log", []) 
        
        if not error_log:
            print("The AI did not find any high-confidence errors to fix.")
        else:
            printed_errors = 0
            for error in error_log:
                original = error.get('original_mistake', '')
                fixed = error.get('correction', '')
                
                
                if original.strip() == fixed.strip():
                    continue 
                
                printed_errors += 1
                print(f"[{printed_errors}] Location: {error.get('location', 'Unknown')}")
                print(f"    Mistake: '{original}'")
                print(f"    Fixed to: '{fixed}'\n")
            
            if printed_errors == 0:
                print("No actual text changes were required on this page.")
                
        print("================================================\n")

if __name__ == "__main__":
    run_test()