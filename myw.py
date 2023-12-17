from flask import Flask, render_template, session, request, g, redirect, url_for, abort, send_from_directory, flash
import os
from werkzeug.utils import secure_filename
import sqlite3
import random
import re
import smtplib
from email.message import EmailMessage
import sys, fitz
import nltk


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.pdf']
app.config['UPLOAD_PATH'] = 'uploads'
app.secret_key = 'oiuytre34567890plkjhgfdcvbnjklp098765'
app.config['SESSION_TYPE'] = 'filesystem'
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


def extract_emails(resume_text):
    return re.findall(EMAIL_REG, resume_text)


def extract_GPA(resume_text):
    return re.findall(GPA_REG, resume_text)


def extract_Exp(resume_text):
    return re.findall(EXP_REG, resume_text)

def ConvertDeg(appDe):
    if appDe == 'primary':
        x = 1
    elif appDe == 'middle':
        x = 2
    elif appDe == 'high':
        x = 3
    elif appDe == 'associate':
        x = 4
    elif appDe == 'bachelor':
        x = 5
    elif appDe == 'master':
        x = 6
    elif appDe == 'doctorate':
        x = 7
    else:
        x = 0
    return x

def pointGPA(appGPA, rsGPA):
    point = 0
    i = float(rsGPA)
    appGPA = float(appGPA)
    if appGPA >= float(rsGPA):
        point = 0.5
        while i <= 5 and appGPA >= i:
            point = point + 0.1
            i = i + 0.1
    else:
        point = 0
    return point

def pointExperienceYear(appEY, rsEY):
    point = 0
    appEY = int(appEY)
    i = int(rsEY)
    if appEY >= int(rsEY):
        point = 1
        while i <= 30 and appEY > i:
            point = point + 0.1
            i = i + 1
    else:
        point = 0
    return point

def pointDe(appDe, rsDe):
    point = 0
    i = int(rsDe)
    appDe = int(appDe)
    if int(appDe) >= int(rsDe):
        point = 1
        while i <= 7 and appDe > i:
            point = point + 0.1
            i = i + 1
    else:
        point = 0
    return point

def pointJT(appJT, appExperienceJT, rsJT):
    point = 0
    appJT = appJT.lower()
    appExperienceJT = appExperienceJT.lower()
    rsJT = rsJT.lower()
    if appJT == rsJT or appExperienceJT == rsJT:
        point = 1
    else:
        point = 0
    return point

def pointCom(appCom, rsCom):
    point = 0
    appCom = appCom.lower()
    rsCom = rsCom.lower()
    if rsCom != 'none':
        if appCom == rsCom:
            point = 1
        else:
            point = 0
    else:
        point = 0
    return point

def pointUni(appUni, rsUni):
    point = 0
    appUni = appUni.lower()
    rsUni = rsUni.lower()
    if rsUni != 'none':
        if appUni == rsUni:
            point = 1
        else:
            point = 0
    else:
        point = 0
    return point

def pointSkill(appS, rsS):
    new_ap = re.sub(r'[^\w~^0-9]', " ", appS)
    ap = set(str(new_ap).lower().split())
    new_rs = re.sub(r'[^\w~^0-9]', " ", rsS)
    rs = set(str(new_rs).lower().split())
    commonWords = []
    point = 0
    for i in rs:
        if i in ap:
            point = point + 0.2
            commonWords.append(i)
    return point

def pointEx(appEx, appJT, rsEx):
    point = 0
    if appEx == rsEx or appJT == rsEx:
        point = 1
    else:
        point = 0
    return point

def pointMajor(appMj, rsMj):
    point = 0
    appMj = appMj.lower()
    rsMj = rsMj.lower()
    if rsMj != 'none':
        if appMj == rsMj:
            point = 1
        else:
            point = 0
    else:
        point = 0
    return point

def pointLan(appL, rsL):
    point = 0
    appL = appL.lower()
    rsL = rsL.lower()
    if rsL != 'none':
        if appL == rsL:
            point = 1
        else:
            point = 0
    else:
        point = 0
    return point

def pointCert(appCer, rsCer):
    point = 0
    appCer = appCer.lower()
    rsCer = rsCer.lower()
    if rsCer != 'none':
        if appCer == rsCer:
            point = 1
        else:
            point = 0
    else:
        point = 0
    return point


def rsTable():
    con = sqlite3.connect("cvAgentDB.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from spD where id = 1")
    rows = cur.fetchall()
    for row in rows:
        rsJT = row["job"]
        rsDe = row["deg"]
        rsMaj = row["maj"]
        rsUni = row["uni"]
        rsGPA = row["GPA"]
        rsCer = row["certfi"]
        rsS = row["skill"]
        rsEx = row["exper"]
        rsCom = row["company"]
        rsEY = row["minY"]
        rsL = row["lang"]
    return rsJT, rsDe, rsMaj, rsUni, rsGPA, rsCer, rsS, rsEx, rsCom, rsEY, rsL


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/Create_account')
def Create_account():
    return render_template('Create_account.html')


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        nm = request.form['username']
        em = request.form['email']
        passw = request.form['Password']
        con = sqlite3.connect("cvAgentDB.db")
        cur = con.cursor()
        cur.execute("INSERT INTO account (name,email,passw) VALUES(?, ?, ?)", (nm, em, passw))
        con.commit()
        con.rollback()

    return render_template("AccountC.html")
    con.close()


@app.route('/database')
def database():
    con = sqlite3.connect("cvAgentDB.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from account")

    rows = cur.fetchall()
    return render_template("database.html", rows=rows)


@app.route('/AccountC')
def AccountC():
    return render_template('AccountC.html')


@app.route('/log', methods=['POST', 'GET'])
def log():
    con = sqlite3.connect("cvAgentDB.db")
    con.row_factory = sqlite3.Row
    if request.method == 'POST':
        try:
            em = request.form['name']
            passw = request.form['passw']
            con = sqlite3.connect("cvAgentDB.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute('SELECT * from account where email=? and passw=?', (em, passw))
            rows = cur.fetchall()
            for row in rows:
                if (em == row[2] and passw == row[3]):
                    session['logedin'] = True
                    session['email'] = em
                    return redirect(url_for("Account"))
        except:
            con.rollback()
            flash("Incorrect email/password!")

    return render_template("log.html")
    con.clos()


@app.route('/fPass')
def fPass():
    return render_template('fPass.html')


@app.route('/Account')
def Account():
    return render_template('Account.html')


@app.route('/Applicant')
def Applicant():
    return render_template('Applicant.html')


@app.route('/cvSub')
def cvSub():
    return render_template('cvSub.html')

@app.route('/About')
def about():
    return render_template('About.html')

@app.route('/UploadCV')
def UploadCV():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('UploadCV.html', files=files)


@app.route('/UploadCV', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
    if file_ext not in app.config['UPLOAD_EXTENSIONS']:
        abort(400)
    filepath = os.path.join(app.config['UPLOAD_PATH'], uploaded_file.filename)
    # uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    x = 'uploads/' + uploaded_file.filename
    print(x)
    uploaded_file.save(filepath)
    con = sqlite3.connect("cvAgentDB.db")
    cur = con.cursor()
    cur.execute("INSERT INTO cvpdf(pdf) VALUES(?)", [(uploaded_file.filename)])
    con.commit()
    con = sqlite3.connect("cvAgentDB.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from cvpdf WHERE pdf=?", [(uploaded_file.filename)])
    rows = cur.fetchall()
    con.commit()

    name = 'none'
    jobT = 'none'
    eJT = 'none'
    yearEx = 'none'
    exCom = 'none'
    college = 'none'
    skill = 'none'
    deg = 'none'
    email = 'none@gmail.com'
    GPA = 'none'
    lan = 'none'
    maj = 'none'
    cert = 'none'
    text = extract_text_from_pdf(x)
    #name = extract_name(text)
    emails = extract_emails(text)
    gp = extract_GPA(text)
    ex = extract_Exp(text)
    if emails:
        email = emails[0]
    else:
        email = 'none@gmail.com'
    if ex:
        yearEx = ex[0]
    else:
        yearEx = '0'
    if gp:
        GPA = gp[0]
    else:
        GPA = '0'
    print(GPA)
    rsJT, rsDe, rsMaj, rsUni, rsGPA, rsCer, rsS, rsEx, rsCom, rsEY, rsL = rsTable()
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
    h = mj.split(sep=',')
    maj = extract_entity(text, h)
    maj = ' '.join(maj)
    cee = rsCer.lower()
    i = cee.split(sep=',')
    cert = extract_entity(text, i)
    cert = ' '.join(cert)
    con = sqlite3.connect("cvAgentDB.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("INSERT INTO cv (name, jobT, eJT, yearEx, exCom, college, skill, deg, email, GPA, lan, major, cer)"
                " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (name, jobT, eJT, yearEx, exCom, college, skill, deg, email, GPA, lan, maj, cert))
    con.commit()
    cvSum = pointSkill(skill.lower(), rsS.lower()) + pointEx(eJT.lower(), jobT.lower(), rsEx.lower()) +\
            pointCom(exCom.lower(), rsCom.lower()) + pointJT(jobT.lower(), eJT.lower(), rsJT.lower()) + \
            pointUni(college.lower(), rsUni.lower()) +pointDe(ConvertDeg(deg.lower()), rsDe) + \
            pointExperienceYear(re.sub(r'[years of experience\+]|[year of experience\+]', "", yearEx), rsEY) +\
            pointGPA(float(re.sub(r'[GPA]|:|=', "", GPA)), rsGPA) + pointLan(lan, rsL) + pointMajor(maj, rsMaj) + \
            pointCert(cert,rsCer)
    print(cvSum)
    cur.execute("INSERT INTO Sort (email, score, name,pdfPath) VALUES(?,?,?,?)", (email, cvSum, name, x))
    con.commit()

    return render_template('cvSub.html')
    con.close()


@app.route('/uploads/<x>')
def upload(x):
    con = sqlite3.connect("cvAgentDB.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select pdfPath from Sort where pdfPath=?", ([x]))
    rows = cur.fetchall()
    return send_from_directory(app.config['UPLOAD_PATH'], x)


@app.route('/displayCV/<pdf>', methods=['POST', 'GET'])
def displayCV(pdf):
    con = sqlite3.connect("cvAgentDB.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from cvpdf where pdf=?", ([pdf]))
    rows = cur.fetchall()
    return render_template('displayCV.html', rows=rows)


@app.route('/database7')
def database7():
    con = sqlite3.connect("cvAgentDB.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from cv")

    rows = cur.fetchall()
    return render_template("database7.html", rows=rows)


@app.route('/ApF1')
def ApF1():
    return render_template('ApF1.html')


@app.route('/addrec1', methods=['POST', 'GET'])
def addrec1():
    con = sqlite3.connect("cvAgentDB.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    if request.method == 'POST':
        try:
            nm = request.form['fullName']
            em = request.form['email']
            job = request.form['job']
            phn = request.form['phoneNum']
            adr = request.form['address']
            linI = request.form['linkedIn']
            tw = request.form['twitter']
            uOrS = request.form['uniOrSc']
            deg = request.form['degree']
            maj = request.form['major']
            GPA = request.form['GPA']
            sD = request.form['StartDate']
            eD = request.form['EndDate']
            cN = request.form['certificateField']
            cS = request.form['certificateScore']
            jT = request.form['jobTitle']
            co = request.form['companyName']
            eY = request.form['Eyear']
            fA = request.form['funAch']
            hSk = request.form['hSkill']
            lan = request.form['lan']
            lanL = request.form['lanLevel']
            cou = request.form['course']
            startD = request.form['StartDate']
            endD = request.form['EndDate']
            couDes = request.form['desOrAch']
            perAch = request.form['perAchievements']

            cur.execute(
                "INSERT INTO Applicant (name,email,jobT,phoneNum, addr,linkedIn,twitter, uniOrSc, degree, major, GPA, sDate, eDate, certField, certScore, jT, company, EYeras, funAch,hSkill, lan, lanLe, course, startD, endD, couAch, perAch) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (nm, em, job, phn, adr, linI, tw, uOrS, deg, maj, GPA, sD, eD, cN, cS, jT, co, eY, fA, hSk, lan, lanL,
                 cou, startD, endD, couDes, perAch))

            con.commit()
            rsJT, rsDe, rsMaj, rsUni, rsGPA, rsCer, rsS, rsEx, rsCom, rsEY, rsL = rsTable()
            appSum = pointSkill(hSk.lower(), rsS.lower()) + pointEx(jT.lower(), job.lower(), rsEx.lower()) + \
                     pointCom(co.lower(), rsCom.lower()) + pointJT(job.lower(), jT.lower(), rsJT.lower()) + \
                     pointUni(uOrS.lower(), rsUni.lower()) + pointDe(deg, rsDe) + pointExperienceYear(eY, rsEY) + \
                     pointGPA(GPA, rsGPA) + pointCert(cN, rsCer) + pointMajor(maj, rsMaj) + pointLan(lan,rsL)
            cur.execute("INSERT INTO Sort (email, score, name) VALUES(?,?,?)", (em, appSum, nm))

            cur.execute("select * from Applicant where phoneNum=?", ([phn]))
            rows = cur.fetchall()
            con.commit()
            return render_template("FormSubcv.html", rows=rows)

        except:
            con.rollback()
            flash("The phone number already used in this position")
    return render_template("ApF1.html")
    con.close()

    # else:
    # con.rollback()
    #         flash("The phone number already used in this position")
    # return render_template("ApF1.html")
    # con.close()


@app.route('/createCV/<id>', methods=['POST', 'GET'])
def createCV(id):
    con = sqlite3.connect("cvAgentDB.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Applicant where id=?", ([id]))
    rows = cur.fetchall()
    return render_template('createCV.html', rows=rows)


@app.route('/database1')
def database1():
    con = sqlite3.connect("cvAgentDB.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from Applicant")

    rows = cur.fetchall()
    return render_template("database1.html", rows=rows)


@app.route('/ActiveP')
def ActiveP():
    con = sqlite3.connect("cvAgentDB.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from activePosition")
    rows = cur.fetchall()
    return render_template('ActiveP.html', rows=rows)


@app.route('/activePosition/<id>', methods=['POST', 'GET'])
def activePosition(id):
    con = sqlite3.connect("cvAgentDB.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('SELECT * FROM activePosition WHERE id = ?', (id))
    rows = cur.fetchall()
    con.close()
    return render_template('activePosition.html', rows=rows)


@app.route('/deActiveForm/<id>', methods=['POST', 'GET'])
def deActiveF(id):
    con = sqlite3.connect("cvAgentDB.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("DELETE from activePosition WHERE id=?", (id))
    con.commit()
    return render_template("deActiveForm.html")


@app.route('/addrec7/<id>', methods=['POST', 'GET'])
def addrec7(id):
    if request.method == 'POST':
        try:
            nm = request.form['job']
            caNum = request.form['CandidateNum']
            de = request.form['deg']
            maj = request.form['maj']
            un = request.form['uni']
            GPA = request.form['GPA']
            cee = request.form['certificateField']
            skill = request.form['skill']
            exp = request.form['exp']
            eCo = request.form['expCom']
            minY = request.form['minY']
            lang = request.form['lang']
            with sqlite3.connect("cvAgentDB.db") as con:
                cur = con.cursor()

                cur.execute("UPDATE spD SET job=?, numCand=?, deg=?, maj=?, uni=?, GPA=?, certfi=?, skill=?,"
                            "exper=?,company=?, minY=?, lang=? WHERE id=?",
                            (nm, caNum, de, maj, un, GPA, cee, skill, exp, eCo, minY, lang, id))

                cur.execute("INSERT INTO activePosition (job, numCand, deg, maj, uni, GPA, certfi,skill, exper,company, minY,lang) "
                            "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)",
                            (nm, caNum, de, maj, un, GPA, cee,skill, exp, eCo, minY,lang))
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("existingForm.html", msg=msg)
            con.close()


@app.route('/existingPosition/<id>', methods=['POST', 'GET'])
def existingPosition(id):
    con = sqlite3.connect("cvAgentDB.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('SELECT * from spD WHERE id=?', (id))
    rows = cur.fetchall()
    con.close()
    return render_template('existingPosition.html', rows=rows)


@app.route('/SetP')
def SetP():
    return render_template('SetP.html')


@app.route('/SetPD')
def SetPD():
    return render_template('SetPD.html')


@app.route('/addrec6', methods=['POST', 'GET'])
def addrec6():
    if request.method == 'POST':
        try:
            nm = request.form['job']
            caNum = request.form['CandidateNum']
            de = request.form['deg']
            maj = request.form['maj']
            un = request.form['uni']
            GPA = request.form['GPA']
            cert = request.form['certificateField']
            skill = request.form['skill']
            exp = request.form['exp']
            eCo = request.form['expCom']
            minY = request.form['minY']
            la = request.form['lan']
            with sqlite3.connect("cvAgentDB.db") as con:
                cur = con.cursor()

                cur.execute("INSERT INTO spD (job, numCand, deg, maj, uni, GPA, certfi, skill, exper,company, minY, "
                            "lang) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (nm, caNum, de, maj, un, GPA, cert, skill, exp, eCo, minY, la))

                cur.execute(
                    "INSERT INTO activePosition (job, numCand, deg, maj, uni, GPA, certfi, skill, exper,company,"
                    " minY, lang) "
                    "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (nm, caNum, de, maj, un, GPA, cert, skill, exp, eCo, minY, la))
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("pCreated.html", msg=msg)
            con.close()


@app.route('/database6')
def database6():
    con = sqlite3.connect("cvAgentDB.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from spD")

    rows = cur.fetchall()
    return render_template("database6.html", rows=rows)


@app.route('/UseEP')
def UseEP():
    con = sqlite3.connect("cvAgentDB.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from spD")
    rows = cur.fetchall()
    return render_template('UseEP.html', rows=rows)


@app.route('/existingForm')
def existingForm():
    return render_template('existingForm.html')


@app.route('/deForm/<id>', methods=['POST', 'GET'])
def removePosition(id):
    con = sqlite3.connect("cvAgentDB.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("DELETE from spD WHERE id=?", (id))
    con.commit()
    return render_template("deForm.html")


@app.route('/FormSub')
def FormSub():
    return render_template('FormSub.html')


@app.route('/ConfirmPL')
def ConfirmPL():
    return render_template('ConfirmPL.html')


@app.route('/pCreated')
def pCreated():
    return render_template('pCreated.html')


@app.route('/Sort')
def sort():
    con = sqlite3.connect("cvAgentDB.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from Sort")
    rows = cur.fetchall()
    return render_template("Sort.html", rows=rows)


@app.route('/CandL')
def CandL():
    con = sqlite3.connect("cvAgentDB.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur1 = con.cursor()
    cur2 = con.cursor()
    cur3 = con.cursor()
    cur4 = con.cursor()
    cur.execute("select * from spD where id = 1")
    rows = cur.fetchall()
    for row in rows:
        numCand = row["numCand"]
    cur1.execute("select * from Sort ORDER by score DESC LIMIT ?", (numCand,))
    rows1 = cur1.fetchall()
    receiver_email_address = []
    for row in rows1:
        em = row["email"]
        receiver_email_address.append(em)
    cur2.execute("select * from Sort")
    rows2 = cur2.fetchall();
    x = len(rows2)
    cur3.execute("select * from Sort ORDER by score DESC LIMIT ? OFFSET ?", (x, numCand))
    rows3 = cur3.fetchall()
    receiver_email_address1 = []
    for row in rows3:
        em1 = row["email"]
        receiver_email_address1.append(em1)
    email_subject = "Respond to your application"
    sender_email_address = "CvAgent.4@gmail.com"
    email_password = "wnzxrmryqxogdszu"
    email_smtp = "smtp.gmail.com"
    server = smtplib.SMTP(email_smtp, '587')
    server.ehlo()
    server.starttls()
    server.login(sender_email_address, email_password)
    message = EmailMessage()
    message['Subject'] = email_subject
    message['From'] = sender_email_address
    message['To'] = ', '.join(receiver_email_address + receiver_email_address1)
    for i in range(3):
        message.set_content("Dear applicant, Thank you for your interest in applying to our company, we are pleased to"
                            " inform you that we selected you for the job interview. We will inform you about the "
                            "interview details soon.")
    server.send_message(message, sender_email_address, receiver_email_address)
    receiver_email_address.pop(0)
    i += 1
    for i in range(3):
        message.set_content(
            "Dear applicant, Thank you for your interest in applying to our company; we are sorry to inform you that we did"
            " not select you for the interview. We wish you all the best in your job search and future professional "
            "endeavors.")
    server.send_message(message, sender_email_address, receiver_email_address1)
    receiver_email_address1.pop(0)
    i += 1
    server.quit()
    cur4.execute("select * from Sort ORDER by score DESC LIMIT ?", (numCand,))
    rows = cur4.fetchall()
    return render_template('CandL.html', rows=rows)
    con.close()


if __name__ == '__main__':
    app.run(debug=True)
