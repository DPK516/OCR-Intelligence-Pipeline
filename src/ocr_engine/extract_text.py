import os
import base64
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def encode_image(image_path):
    """Converts the image to base64 so Groq can see it."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def extract_text_from_image(image_path):
    """
    Phase 3: Initial Raw Text Extraction.
    Sends the image to Groq's Vision model to get a baseline transcription.
    """
    print(f"Uploading and reading: {os.path.basename(image_path)}...")
    
    try:
        base64_image = encode_image(image_path)
        
        response = client.chat.completions.create(
            
            model="meta-llama/llama-4-scout-17b-16e-instruct", 
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract all the text from this image exactly as it appears. Do not add any conversational text or markdown formatting. Just return the raw text."},
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
        print(f"Error during raw extraction: {e}")
        return None


if __name__ == "__main__":
    TEST_IMAGE = "data/raw_images/page_1.png" 
    if os.path.exists(TEST_IMAGE):
        text = extract_text_from_image(TEST_IMAGE)
        print("\n--- Extracted Text ---")
        print(text)