import numpy as np
import sqlite3
import re

con = sqlite3.connect("cvAgentDB.db")
con.row_factory = sqlite3.Row
cur = con.cursor()
cur1 = con.cursor()
cur2 = con.cursor()

cur.execute("select * from Applicant where id = 1")
cur1.execute("select * from spD where id = 1")
cur2.execute("select * from cv where id = 1")

rows = cur.fetchall()
rows1 = cur1.fetchall()
rows2 = cur2.fetchall()

for row in rows:
    appName = row['name']
    appJT = row["jobT"]
    appEm = row["email"]
    appGPA = row["GPA"]
    appUni = row["uniOrSc"]
    appDe = row["degree"]
    appEx = row["jT"]
    appCom = row["company"]
    appEY = row["EYeras"]
    appS = row["hSkill"]
    appLan = row["lan"]
    appCer = row["certField"]
    appMaj = row["major"]
for row in rows1:
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
for row in rows2:
    cvName = row['name']
    cvEjt = row["eJT"]
    cvJ = row["jobT"]
    cvYear = row["yearEx"]
    cvCom = row["exCom"]
    cvUni = row["college"]
    cvS = row["skill"]
    cvDeg = row["deg"]
    cvGPA = row["GPA"]
    cvEm = row["email"]
    cvCert = row["cer"]
    cvLan = row["lan"]
    cvMaj = row["major"]

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
    appGPA = re.sub(r'[GPA:]', "", cvGPA)
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
    if appCom == rsCom:
        point = 1
    else:
        point = 0
    return point

def pointUni(appUni, rsUni):
    point = 0
    appUni = appUni.lower()
    rsUni = rsUni.lower()
    if appUni == rsUni:
        point = 1
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
    if appMj == rsMj:
        point = 1
    else:
        point = 0
    return point

def pointLan(appL, rsL):
    point = 0
    appL = appL.lower()
    rsL = rsL.lower()
    if appL == rsL:
        point = 1
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

print(pointSkill(cvS.lower(), rsS.lower()))
print(pointEx(cvEjt.lower(), cvJ.lower(), rsEx.lower()))
print(pointCom(cvCom.lower(), rsCom.lower()))
print(pointJT(cvJ.lower(), cvEjt.lower(), rsJT.lower()))
print(pointUni(cvUni.lower(), rsUni.lower()))
d = ConvertDeg(cvDeg.lower())
print(pointDe(ConvertDeg(cvDeg.lower()), rsDe))
print(pointExperienceYear(re.sub(r'[years of experience\+]|[year of experience\+]', "", cvYear), rsEY))
print(pointGPA(float(re.sub(r'[GPA]|:|=', "", cvGPA)), rsGPA))
print(pointCert(cvCert,rsCer))
print(pointMajor(cvMaj, rsMaj))
print(pointLan(cvLan, rsL))
cvSum = pointSkill(cvS.lower(), rsS.lower()) + pointEx(cvEjt.lower(), cvJ.lower(), rsEx.lower()) +pointCom(cvCom.lower(), rsCom.lower()) + pointJT(cvJ.lower(), cvEjt.lower(), rsJT.lower()) + pointUni(cvUni.lower(), rsUni.lower()) +pointDe(ConvertDeg(cvDeg.lower()), rsDe) + pointExperienceYear(re.sub(r'[years of experience\+]|[year of experience\+]', "", cvYear), rsEY) +pointGPA(float(re.sub(r'[GPA]|:|=', "", cvGPA)), rsGPA) + pointLan(cvLan, rsL) + pointMajor(cvMaj, rsMaj) + pointCert(cvCert,rsCer)
print(cvSum)
print('__________________________________________________________________________________')
print(pointSkill(appS, rsS))
print(pointEx(appEx.lower(), appJT.lower(), rsEx.lower()))
print(pointCom(appCom.lower(), rsCom.lower()))
print(pointJT(appJT.lower(), appEx.lower(), rsJT.lower()))
print(pointUni(appUni.lower(), rsUni.lower()))
print(pointDe(appDe, rsDe))
print(pointExperienceYear(appEY, rsEY))
print(pointGPA(appGPA, rsGPA))
print(pointLan(appLan, rsL))
print(pointMajor(appMaj, rsMaj))
print(pointCert(appCer, rsCer))
appSum = pointSkill(appS.lower(), rsS.lower()) + pointEx(appEx.lower(), appJT.lower(), rsEx.lower()) + \
         pointCom(appCom.lower(), rsCom.lower()) + pointJT(appJT.lower(), appJT.lower(), rsJT.lower()) + \
         pointUni(appUni.lower(), rsUni.lower()) + pointDe(appDe, rsDe) + pointExperienceYear(appEY, rsEY) + \
         pointGPA(appGPA, rsGPA) + pointCert(appCer, rsCer) + pointMajor(appMaj, rsMaj)+ pointLan(appLan, rsL)
print(appSum)

cur.execute("INSERT INTO Sort (email, score, name) VALUES(?,?,?)", (appEm, appSum,appName))
cur.execute("INSERT INTO Sort (email, score, name) VALUES(?,?,?)", (cvEm, cvSum, cvName))
con.commit()