import os
import glob
import base64
from groq import Groq
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=API_KEY)

def encode_image(image_path):
    """Converts a local image file to a base64 string so it can be sent securely over the internet."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def extract_text_from_image(image_path):
    """
    Sends an image to the Groq API using a high-speed multimodal vision model to extract text.
    """
    print(f"Uploading and reading: {os.path.basename(image_path)}...")
    
    try:
        base64_image = encode_image(image_path)
        prompt = "Extract all the text from this document exactly as it appears. Do not add any conversational filler, explanations, or descriptions."
        
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=0,
        )
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error communicating with Groq API: {e}")
        return None


if __name__ == "__main__":
    INPUT_DIR = "data/raw_images"
    image_files = glob.glob(os.path.join(INPUT_DIR, "*.png"))
    
    if not image_files:
        print("No images found! Make sure you run pdf_to_image.py first.")
    else:
        print(f"Found {len(image_files)} images. Connecting to Groq Cloud...\n")
        
        for img_path in image_files:
            extracted_text = extract_text_from_image(img_path)
            
            print("\n" + "="*40)
            print(f"--- EXTRACTED TEXT FOR {os.path.basename(img_path)} ---")
            print("="*40)
            print(extracted_text.strip() if extracted_text else "None")
            print("="*40 + "\n")