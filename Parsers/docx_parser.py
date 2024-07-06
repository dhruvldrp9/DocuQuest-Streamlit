import docx


class DocxParser:
    def get_docx_text(filename):
        doc = docx.Document(filename)
        fullText = [para.text for para in doc.paragraphs]
        return '\n'.join(fullText)
