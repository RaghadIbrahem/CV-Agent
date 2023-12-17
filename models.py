import sqlite3
from datetime import datetime

conn = sqlite3.connect('cvAgentDB.db')

conn.execute('CREATE TABLE account (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, email TEXT, passw TEXT)')
conn.execute('CREATE TABLE Applicant(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, jobT TEXT,'
             ' phoneNum TEXT NOT NULL UNIQUE, addr TEXT, linkedIn TEXT, twitter TEXT, uniOrSc TEXT, degree INTEGER, '
             'major TEXT, '
             'GPA INTEGER, sDate DateTime, eDate DateTime, certField TEXT, certScore INTEGER, jT TEXT, company TEXT,'
             'EYeras INTEGER, funAch TEXT, hSkill TEXT, lan TEXT, lanLe INTEGER,course TEXT, '
             'startD DateTime, endD DateTime, couAch TEXT, perAch TEXT)')
conn.execute('CREATE TABLE Sort(id INTEGER PRIMARY KEY, email TEXT, score INTEGER, name TEXT,pdfPath TEXT,'
             'FOREIGN KEY (id) REFERENCES Applicant(id))')
conn.execute('CREATE TABLE spD (id INTEGER PRIMARY KEY AUTOINCREMENT, job TEXT, numCand INTEGER,deg INTEGER, maj TEXT, '
             'uni TEXT, GPA INTEGER, certfi TEXT, skill TEXT, exper TEXT, company TEXT, minY INTEGER, lang TEXT)')
conn.execute('CREATE TABLE cv(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, jobT TEXT, eJT TEXT, yearEx TEXT, '
             'exCom TEXT,college TEXT, skill TEXT, deg TEXT, email TEXT, GPA TEXT, lan TEXT, major TEXT,'
             'cer TEXT)')
conn.execute('CREATE TABLE IF NOT EXISTS activePosition (id INTEGER PRIMARY KEY AUTOINCREMENT, job TEXT, '
             'numCand INTEGER,deg INTEGER, maj TEXT, '
             'uni TEXT, GPA INTEGER, certfi TEXT, skill TEXT, exper TEXT, company TEXT, minY INTEGER, lang TEXT,'
             ' FOREIGN KEY (id) REFERENCES spD(id))')
conn.execute('CREATE TABLE IF NOT EXISTS cvpdf(id INTEGER PRIMARY KEY, pdf TEXT)')
conn.close()