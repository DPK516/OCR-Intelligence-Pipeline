import os
from docx import Document

def create_word_document(pages_data, output_filename):
    """
    Takes a list of cleaned text pages and stitches them into a final Microsoft Word Document.

    """
    print("\nStarting Document Assembly...")
    
    
    doc = Document()
    
    
    doc.add_heading('Digitized Document Extraction', 0)
    
    
    for index, page_text in enumerate(pages_data):
        page_number = index + 1
        print(f"Adding Page {page_number} to the document...")
        
        
        doc.add_heading(f'Page {page_number}', level=1)
        
        
        doc.add_paragraph(page_text)
        
        
        if page_number < len(pages_data):
            doc.add_page_break()
            
    
    output_dir = "data/output_docs"
    os.makedirs(output_dir, exist_ok=True) 
    final_path = os.path.join(output_dir, output_filename)
    
    
    doc.save(final_path)
    print(f"\nSUCCESS! Document saved at: {final_path}")