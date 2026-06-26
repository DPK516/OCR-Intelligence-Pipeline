import os
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK 
from docx.shared import Pt

def create_word_document(pages_structured_data, output_filename):
    print("\nStarting Advanced Layout-Aware Document Assembly...")
    doc = Document()
    
    for index, page_data in enumerate(pages_structured_data):
        page_number = index + 1
        print(f"Assembling Page {page_number} with advanced formatting...")
        
        for block in page_data.get("page_layout_corrected", []):
            p = doc.add_paragraph()
            
            
            alignment = block.get("alignment", "left")
            if alignment == "center":
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif alignment == "right":
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                
           
            text_spans = block.get("text_spans", [])
            for span in text_spans:
                run = p.add_run(span.get("text", ""))
                
                
                if span.get("bold", False):
                    run.bold = True
                if span.get("italic", False):
                    run.italic = True
                    
                
                if block.get("font_style") == "serif":
                    run.font.name = 'Times New Roman'
                else:
                    run.font.name = 'Arial'
                    
        
        if page_number < len(pages_structured_data):
            if 'p' in locals():
                p.add_run().add_break(WD_BREAK.PAGE)
            else:
                doc.add_page_break()
            
    output_dir = "data/output_docs"
    os.makedirs(output_dir, exist_ok=True)
    final_path = os.path.join(output_dir, output_filename)
    
    try:
        doc.save(final_path)
        print(f"\nSUCCESS! Visually matched document saved at: {final_path}")
    except PermissionError:
        print(f"\n ERROR: Cannot save. Please close '{output_filename}' in Microsoft Word.")