import os
import base64
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def encode_image(image_path):
    """Converts the image to base64 so Groq can process it."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def correct_text_with_vision(image_path, transcribed_text):
    """
    Analyzes the image to extract formatting (alignment, fonts, bold/italics),
    corrects layout errors, and guarantees a strict JSON output.
    """
    print(f"Analyzing formatting and layout for: {os.path.basename(image_path)}...")
    
    try:
        base64_image = encode_image(image_path)
        
        prompt = f"""You are an expert typography and document layout analysis engine. 
You are analyzing exactly ONE isolated page from a PDF (provided as an image). 

Review this raw draft text for context:
---
{transcribed_text}
---

Analyze the image carefully and output a strict JSON object mapping out the text blocks. 
You MUST follow this exact JSON structure:
{{
  "page_layout_corrected": [
    {{
      "type": "heading" or "paragraph" or "page_number" or "table",
      "alignment": "left" or "center" or "right",
      "font_style": "serif" or "sans-serif",
      "text_spans": [
        {{
          "text": "The actual text string",
          "bold": true or false,
          "italic": true or false
        }}
      ],
      "rows": [
        ["Column 1 text", "Column 2 text", "Column 3 text"]
      ]
    }}
  ]
}}

Rules:
1. Output ONLY valid JSON. 
2. Capture the exact text alignment (left, center, or right).
3. If you detect a grid, table of contents, or tabular data, you MUST use the "table" type and organize the data into the "rows" array. Leave "text_spans" empty for tables.
4. ANTI-HALLUCINATION RULE: If a table column or cell is empty or blank in the image, you MUST output the exact word "[BLANK]" in that JSON array position to maintain strict column alignment.
5. NO MATH FORMATTING: Never use LaTeX, fractions, or math formatting (like \\frac). Output plain text exactly as it appears on the page.
"""

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
            response_format={"type": "json_object"} 
        )
        
        raw_response = response.choices[0].message.content
        
        clean_response = raw_response.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_response)
        
    except Exception as e:
        print(f"Error during layout vision analysis: {e}")
        
        return {
            "page_layout_corrected": [{
                "type": "paragraph", 
                "alignment": "left", 
                "font_style": "sans-serif", 
                "text_spans": [{"text": "[Extraction Error]", "bold": False, "italic": False}]
            }]
        }