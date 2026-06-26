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

def run_visual_inspection(image_path, extracted_text):
    """
    Acts as a strict QA Tester. Compares the original image against our extracted text
    and explicitly lists all the visual formatting we missed.

    """
    print(f"\n Running Visual QA Inspection on {os.path.basename(image_path)}...")
    
    try:
        base64_image = encode_image(image_path)
        
        
        qa_prompt = f"""You are a strict Document Quality Assurance Inspector. 

Here is the plain text we managed to extract from this document:
--- START EXTRACTED TEXT ---
{extracted_text}
--- END EXTRACTED TEXT ---

Your job is to look at the attached original source image with your own eyes and compare it to the text above. 
Identify what visual, formatting, or layout issues are missing or incorrect in our extraction.

Specifically check for and list:
1. Font Colors (e.g., "The main title is actually blue")
2. Text Alignment (e.g., "The date should be aligned to the far right")
3. Layout Structure (e.g., "Paragraph 2 is actually split into two columns")
4. Missing Visuals (e.g., "There is a company logo at the top left")

Output a clear, bulleted list of the visual discrepancies you found. Be specific."""

        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct", 
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": qa_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.2,
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error during Visual QA: {e}"



if __name__ == "__main__":
    import sys
    
    
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    
    
    sys.path.append(project_root)
    
    
    from src.ocr_engine.extract_text import extract_text_from_image
    
    TEST_IMAGE = "data/raw_images/page_1.png" 
    
    if os.path.exists(TEST_IMAGE):
        print("Getting current text extraction...")
        current_text = extract_text_from_image(TEST_IMAGE)
        
        if current_text:
            inspection_report = run_visual_inspection(TEST_IMAGE, current_text)
            
            print("\n" + "="*50)
            print("   👀 VISUAL QA INSPECTION REPORT")
            print("="*50)
            print(inspection_report)
            print("="*50 + "\n")
    else:
        print(f"Waiting for {TEST_IMAGE} to run the test!")