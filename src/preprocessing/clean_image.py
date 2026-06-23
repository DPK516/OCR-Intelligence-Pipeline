import cv2
import numpy as np
import os
import glob

def preprocess_image(image_path, output_path):
    """
    To cleans up a raw image to make the text pop for the OCR AI.

    """
    
    img = cv2.imread(image_path)
    
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    
    binary = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    
    
    cv2.imwrite(output_path, binary)
    print(f"Processed and saved: {os.path.basename(output_path)}")


if __name__ == "__main__":
    INPUT_DIR = "data/raw_images"
    OUTPUT_DIR = "data/processed_images"
    
    
    image_files = glob.glob(os.path.join(INPUT_DIR, "*.png"))
    
    if not image_files:
        print("No images found! Make sure you run pdf_to_image.py first.")
    else:
        print(f"Found {len(image_files)} images. Starting cleanup...")
        for img_path in image_files:
            
            filename = os.path.basename(img_path)
            out_path = os.path.join(OUTPUT_DIR, filename)
            
            
            preprocess_image(img_path, out_path)
            
        print("Preprocessing complete! Check the data/processed_images folder.")