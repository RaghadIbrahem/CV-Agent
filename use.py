import re
import fitz

def extract_Exp(resume_text):
    return re.findall(GPA_REG, resume_text)
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = " "
    for page in doc:
        text = text + str(page.get_text())
        text = text.strip()
        text = ' '.join(text.split())
    return text
text = extract_text_from_pdf('uploads/Raghad Ibrahim.pdf')
GPA_REG = re.compile(r'GPA:\d.\d|GPA: \d.\d|GPA\d.\d|GPA \d.\d|GPA=\d.\d|GPA= \d.\d|GPA =\d.\d|GPA = \d.\d|GPA: \d|'
                     r'GPA:\d|GPA\d|GPA \d|GPA=\d|GPA= \d|GPA =\d|GPA = \d')
ex = extract_Exp('My GPA: 4.5')
if ex:
    yearEx = ex[0]
    print(yearEx)
    print(float(re.sub(r'[GPA]|:|=', "", yearEx)))
print(float(re.sub(r'[GPA]|:|=', "", '0')))