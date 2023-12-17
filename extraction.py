import nltk
import fitz
import sqlite3
import re
import spacy
import en_core_web_sm
from spacy.matcher import Matcher
nlp = en_core_web_sm.load()
matcher = Matcher(nlp.vocab)
con = sqlite3.connect("cvAgentDB.db")
con.row_factory = sqlite3.Row

cur = con.cursor()
cur.execute("select * from spD where id = 1")

rows = cur.fetchall()
for row in rows:
    rsJT = row["job"]
    rsMaj = row["maj"]
    rsUni = row["uni"]
    rsCer = row["certfi"]
    rsS = row["skill"]
    rsCom = row["company"]
    rsEx = row["exper"]
    rsL = row["lang"]
GPA_REG = re.compile(r'GPA:\d.\d|GPA: \d.\d|GPA\d.\d|GPA \d.\d|GPA=\d.\d|GPA= \d.\d|GPA =\d.\d|GPA = \d.\d|GPA: \d|'
                     r'GPA:\d|GPA\d|GPA \d|GPA=\d|GPA= \d|GPA =\d|GPA = \d')
EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')
EXP_REG = re.compile(r'\d years of experience|\d year of experience|.. years of experience')

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = " "
    for page in doc:
        text = text + str(page.get_text())
        text = text.strip()
        text = ' '.join(text.split())
    return text
def extract_name(resume_text):
    nlp_text = nlp(resume_text)

    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

    matcher.add('NAME', [pattern])

    matches = matcher(nlp_text)

    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text

def extract_emails(resume_text):
    return re.findall(EMAIL_REG, resume_text)

def extract_GPA(resume_text):
    return re.findall(GPA_REG, resume_text)

def extract_Exp(resume_text):
    return re.findall(EXP_REG, resume_text)

def extract_entity(input_text, skill):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(input_text)
    filtered_tokens = [w for w in word_tokens if w not in stop_words]
    filtered_tokens = [w for w in word_tokens if w.isalpha()]
    bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))
    found_entity = set()
    for token in filtered_tokens:
        if token.lower() in skill:
            found_entity.add(token)
    for ngram in bigrams_trigrams:
        if ngram.lower() in skill:
            found_entity.add(ngram)

    return found_entity

text = extract_text_from_pdf('uploads/cv.pdf')


con = sqlite3.connect("cvAgentDB.db")
con.row_factory = sqlite3.Row
cur = con.cursor()
name = 'none'
jobT = 'none'
eJT = 'none'
yearEx = 'none'
exCom = 'none'
college = 'none'
skill = 'none'
deg = 'none'
email = 'none'
GPA = 'none'
lan= 'none'
maj = 'none'
cert = 'none'
emails = extract_emails(text)
gp = extract_GPA(text)
ex = extract_Exp(text)
if emails:
    email = emails[0]
if gp:
     GPA = gp[0]
else:
    GPA = 0
if ex:
    yearEx = ex[0]
s = rsS.lower()
a = s.split(sep=',')
skill = extract_entity(text, a)
skill = ' '.join(skill)
j = rsJT.lower()
b = j.split(sep=',')
jobT = extract_entity(text, b)
jobT = ' '.join(jobT)
ej = rsEx.lower()
c = ej.split(sep=',')
eJT = extract_entity(text, c)
eJT = ' '.join(eJT)
ec = rsCom.lower()
d = ec.split(sep=',')
exCom = extract_entity(text, d)
exCom = ' '.join(exCom)
col = 'King Saud University,King Abdulaziz University,King Abdullah University of Science Technology,' \
    'King Fahd University of Petroleum Minerals,Imam Abdulrahman Bin Faisal University,Taif University,' \
    'King Khalid University,Umm Al Qura University,Prince Sattam bin Abdulaziz University,Taibah University,' \
    'Qassim University,Princess Nourah Bint Abdulrahman University,Majmaah University,Prince Sultan University,' \
    'Al Imam Muhammad Ibn Saud Islamic University,Al Jouf University,Jazan University,University of Jeddah,' \
    'King Saud bin Abdulaziz University for Health Sciences,University of Haail,Alfaisal University,' \
    'Prince Mohammad Bin Fahd University,Najran University,College of Nursing and Allied Health Sciences,' \
    'Al Baha University,King Faisal University,Shaqra University,Saudi Electronic University,' \
    'University of Northern Border,Islamic University of Al Madinah,Bisha University,University of Hafr Al Batin,' \
    'Effat University,Almaarefa University,Royal Commission Yanbu Colleges Institutes,Jubail Industrial College,' \
    'Dar Al Uloom University,Al Yamamah University,Riyadh Colleges of Dentistry and Pharmacy,' \
    'Prince Sultan Military College of Health Sciences,University of Prince Mugrin,Institute of Public Administration,' \
    'University of Business and Technology,Ibn Sina National College for Medical Studies,Batterjee Medical College,' \
    'Naif Arab University for Security Sciences,Fahad Bin Sultan University,Arab Open University Saudi Arabia,' \
    'Fakeeh College of Medical Sciences,Vision Colleges,Dar Al Hekma University,College of Technology at Riyadh,' \
    'Madinah Institute for Leadership and Entrepreneurship,Jubail Technical Institute,Sulaiman Alrajhi Colleges,' \
    'Arab East Colleges,Gulf Colleges,Colleges Farabi,Mustaqbal University Buraydah,Dammam Community College,' \
    'Jeddah International College,Ibn Rushd College for Management Sciences,Buraydah Private Colleges,' \
    'Imsimbi Training,Prince Sultan Aviation Academy,Applied Engineering College,' \
    'Saad College of Nursing Allied Health Sciences'.lower()
e = col.split(sep=',')
college = extract_entity(text, e)
college = ' '.join(college)
de = 'Primary School,Middle School,High School,Associate,Bachelor,Master,Doctorate'.lower()
f = de.split(sep=',')
deg = extract_entity(text, f)
deg = ' '.join(deg)
la = rsL.lower()
g = la.split(sep=',')
lan = extract_entity(text, g)
lan = ' '.join(lan)
mj = rsMaj.lower()
h = maj.split(sep=',')
maj = extract_entity(text, h)
maj = ' '.join(maj)
cee = rsCer.lower()
i = cee.split(sep=',')
cert = extract_entity(text, i)
cert = ' '.join(cert)
#name = extract_name(text)

cur.execute("INSERT INTO cv (name, jobT, eJT, yearEx, exCom, college, skill, deg, email, GPA, lan, major, cer)"
                " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (name, jobT, eJT, yearEx, exCom, college, skill, deg, email, GPA, lan, maj, cert))
con.commit()
con.close()