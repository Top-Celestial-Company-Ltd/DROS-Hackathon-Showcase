import zipfile

md_file = r'E:\vscode\AI知識庫\DROS-Hackathon-Showcase\黑客松-DROS-Team.md'
docx_file = r'E:\vscode\AI知識庫\DROS-Hackathon-Showcase\黑客松-DROS-Team.docx'

with open(md_file, 'r', encoding='utf-8') as f:
    text = f.read()

print("Markdown Length:", len(text))
