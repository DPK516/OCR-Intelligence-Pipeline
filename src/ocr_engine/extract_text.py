import os
import glob
import requests

API_KEY = "K87030846488957"
OCR_SPACE_URL = "https://api.ocr.space/parse/image"

def extract_text_from_image(image_path):
    """
    Sends a local image file to the OCR.space API and returns the extracted text.
    """
    print(f"Uploading and reading: {os.path.basename(image_path)}...")
    
    try:
        
        payload = {
            'apikey': API_KEY,
            'language': 'eng',         
            'isOverlayRequired': False, 
            'isTable': True            
        }
        
        
        with open(image_path, 'rb') as img_file:
            files = {'file': img_file}
            
            
            response = requests.post(OCR_SPACE_URL, data=payload, files=files)
            
        
        result = response.json()
        
        
        if result.get("OCRExitCode") == 1:
            parsed_results = result.get("ParsedResults", [])
            if parsed_results:
                return parsed_results[0].get("ParsedText", "")
            return "No text detected on this page."
        else:
            print(f"API Error: {result.get('ErrorMessage')}")
            return None
            
    except Exception as e:
        print(f"Connection error: {e}")
        return None


if __name__ == "__main__":
    INPUT_DIR = "data/raw_images"
    image_files = glob.glob(os.path.join(INPUT_DIR, "*.png"))
    
    if not image_files:
        print("No images found! Make sure you run pdf_to_image.py first.")
    else:
        print(f"Found {len(image_files)} images. Connecting to OCR.space...\n")
        
        for img_path in image_files:
            extracted_text = extract_text_from_image(img_path)
            
            print("\n" + "="*40)
            print(f"--- EXTRACTED TEXT FOR {os.path.basename(img_path)} ---")
            print("="*40)
            print(extracted_text)
            print("="*40 + "\n")