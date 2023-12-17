import sqlite3
import smtplib
from email.message import EmailMessage
con = sqlite3.connect("cvAgentDB.db")
con.row_factory = sqlite3.Row
cur = con.cursor()
cur1 = con.cursor()
cur2 = con.cursor()
cur3 = con.cursor()

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
print(receiver_email_address1)

#########################################################################
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