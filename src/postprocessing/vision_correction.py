import os
import base64
import json 
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def encode_image(image_path):
    """Converts the image to base64 so Groq can see it."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def correct_text_with_vision(image_path, transcribed_text):
    """
    Sends the image and first-draft text to the vision model, 
    and returns a structured JSON dictionary containing the fixed text 
    AND a log of where the errors were located.

    """
    print(f"Asking vision model to find and locate mistakes for: {os.path.basename(image_path)}...")
    
    try:
        base64_image = encode_image(image_path)
        
        
        prompt = f"""Here is a scanned document image, and the initial transcribed text extracted from it:

--- START OF TRANSCRIBED TEXT ---
{transcribed_text}
--- END OF TRANSCRIBED TEXT ---

Your task is to act as a proofreader. Look at the image and compare it to the transcribed text. Identify and fix HIGH CONFIDENCE mistakes. 

You MUST output your response in strict JSON format matching this exact structure:
{{
  "final_corrected_text": "The complete, fully corrected text of the document.",
  "error_log": [
    {{
      "original_mistake": "The wrong word/phrase",
      "correction": "The fixed word/phrase",
      "location": "A brief description of where this is on the page (e.g., 'Paragraph 1, line 2' or 'Top right corner')"
    }}
  ]
}}

Output ONLY valid JSON. Do not add any conversational text before or after the JSON."""

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
        
        
        raw_response = response.choices[0].message.content
        
        
        clean_response = raw_response.replace("```json", "").replace("```", "").strip()
        
        
        return json.loads(clean_response)
        
    except Exception as e:
        print(f"Error during vision correction: {e}")
        
        return {"final_corrected_text": transcribed_text, "error_log": []}
    