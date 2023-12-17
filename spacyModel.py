import spacy
from spacy.tokens import DocBin
from tqdm import tqdm
import sys, fitz
import sqlite3
import re
GPA_REG = re.compile(r'[GPA]+\:+[ ]+[0-9]+\.[0-9]+')
EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')
EXP_REG = re.compile(r'[0-9\+]+[ years of experience]')
nlp_ner = spacy.load("model-best")
# model = spacy.load("finalModel")
conn = sqlite3.connect("cvAgentDB.db")
cur = conn.cursor()
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = " "
    for page in doc:
        text = text + str(page.get_text())
        text = text.strip()
        text = ' '.join(text.split())
    return text

def extract_emails(resume_text):
    return re.findall(EMAIL_REG, resume_text)

def extract_GPA(resume_text):
    return re.findall(GPA_REG, resume_text)

def extract_Exp(resume_text):
    return re.findall(EXP_REG, resume_text)

text = extract_text_from_pdf('uploads/CV3.pdf')
doc = nlp_ner(text)
name = 'none'
jobT = []
eJT = 'none'
j = 'none'
yearEx = 'none'
exCom = 'none'
college = 'none'
gradY = 'none'
skill = 'none'
deg = 'none'
email = 'none'
GPA = 'none'
loc = 'none'
for ent in doc.ents:
    if ent.label_ == 'Name':
        name = ent.text
    if ent.label_ == 'Designation':
        jobT.append(ent.text)
    if ent.label_ == 'Companies worked at':
        exCom = ent.text
    if ent.label_ == 'College Name':
        college = ent.text
    if ent.label_ == 'Graduation Year':
        gradY = ent.text
    if ent.label_ == 'Skills':
        skill = ent.text
    if ent.label_ == 'Degree':
        deg = ent.text
    if ent.label_ == 'Location':
        loc = ent.text
    print(ent.text, "   ->>>>> ", ent.label_)
j = jobT[0]
eJT = jobT[1]
emails = extract_emails(text)
gp = extract_GPA(text)
ex = extract_Exp(text)
if emails:
    email = emails[0]
if gp:
     GPA = gp[0]
if ex:
    yearEx = ex[0]
cur.execute("INSERT INTO cv (name, jobT, eJT, yearEx, exCom, college, skill, deg, email, GPA, lan, lanL, cer)"
            " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (name, jobT, eJT, yearEx, exCom, college, skill, deg, email, GPA, lan, lanL, cert))
con.commit()
con.row_factory = sqlite3.Row
cur = con.cursor()
cur.execute("select * from cv")
rows = cur.fetchall();
for row in rows:
    print(row["name"])
    print(row["jobT"])
    print(row["eJT"])
    print(row["yearEx"])
    print(row["exCom"])
    print(row["college"])
    print(row["skill"])
    print(row["deg"])
    print(row["email"])
    print(row["GPA"])
    print(row["lan"])
    print(row["lanL"])
    print(row["cer"])

class model:
    nlp_ner = spacy.load("model-best")
    def extract_text_from_pdf(pdf_path):
        doc = fitz.open(pdf_path)
        text = " "
        for page in doc:
            text = text + str(page.get_text())
            text = text.strip()
            text = ' '.join(text.split())
        return text

    def extract_emails(resume_text):
        return re.findall(EMAIL_REG, resume_text)

    def extract_GPA(resume_text):
        return re.findall(GPA_REG, resume_text)

    def extract_Exp(resume_text):
        return re.findall(EXP_REG, resume_text)
    conn = sqlite3.connect("cvAgentDB.db")
    cur = conn.cursor()
    name = 'none'
    jobT = []
    eJT = 'none'
    j = 'none'
    yearEx = 'none'
    exCom = 'none'
    college = 'none'
    gradY = 'none'
    skill = 'none'
    deg = 'none'
    email = 'none'
    GPA = 'none'
    loc = 'none'
    text = extract_text_from_pdf('filename')
    doc = nlp_ner(text)
    for ent in doc.ents:
        if ent.label_ == 'Name':
            name = ent.text
        if ent.label_ == 'Designation':
            jobT.append(ent.text)
        if ent.label_ == 'Companies worked at':
            exCom = ent.text
        if ent.label_ == 'College Name':
            college = ent.text
        if ent.label_ == 'Graduation Year':
            gradY = ent.text
        if ent.label_ == 'Skills':
            skill = ent.text
        if ent.label_ == 'Degree':
            deg = ent.text
        if ent.label_ == 'Location':
            loc = ent.text
        print(ent.text, "   ->>>>> ", ent.label_)
    j = jobT[0]
    eJT = jobT[1]
    emails = extract_emails(text)
    gp = extract_GPA(text)
    ex = extract_Exp(text)
    if emails:
        email = emails[0]
    if gp:
        GPA = gp[0]
    if ex:
        yearEx = ex[0]
    cur.execute("INSERT INTO cv (name, jobT, eJT, yearEx, exCom, college, gradY, skill, deg, email, GPA, loc)"
                " VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                (name, j, eJT, yearEx, exCom, college, gradY, skill, deg, email, GPA, loc))
    conn.commit()
    conn.close()

