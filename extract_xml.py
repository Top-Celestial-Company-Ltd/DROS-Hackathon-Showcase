import zipfile
import xml.etree.ElementTree as ET

docx_path = r'E:\vscode\AI知識庫\DROS-Hackathon-Showcase\temp_team.docx'

with zipfile.ZipFile(docx_path) as z:
    xml_content = z.read('word/document.xml')
    root = ET.fromstring(xml_content)
    
    paragraphs = []
    for p in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
        p_texts = [t.text for t in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text]
        if p_texts:
            paragraphs.append(''.join(p_texts))

output_path = r'E:\vscode\AI知識庫\DROS-Hackathon-Showcase\extracted_team_doc.txt'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(paragraphs))

print("DONE_XML_EXTRACT")
