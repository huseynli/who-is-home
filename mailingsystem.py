# Importing libraries 
import imaplib, email
import subprocess
import sys
import io
import os.path
import emailconf
import smtplib 
from email.message import EmailMessage
#SMTP STUFF FOR SENDING EMAILS
def gondergetsin():
    #2 commented lines below are for SMTP, Yandex uses SMTP_SSL. If you need SMTP with port 587, uncomment lines bvelow.
    #and comment the following line: session = smtplib.SMTP_SSL(emailconf.smtp_url, emailconf.smtp_port)
    #session = smtplib.SMTP(emailconf.smtp_url, emailconf.smtp_port)  
    #session.starttls() 
    session = smtplib.SMTP_SSL(emailconf.smtp_url, emailconf.smtp_port)
    session.login(emailconf.user, emailconf.password)
    with open("log.txt", "r") as fhand:
        message = EmailMessage()
        message.set_content(fhand.read())
    message['Subject'] = "Reply to your request"
    message['From'] = emailconf.user
    message['To'] = emailconf.incomingfrom
    session.send_message(message)
    session.quit()
#SMTP STUFF ENDED

# gets the content of email 
def get_body(msg): 
    if msg.is_multipart(): 
        return get_body(msg.get_payload(0)) 
    else: 
        return msg.get_payload(None, True) 
  
# searches per key, value
def search(key, value, con):  
    result, data = con.search(None, key, '"{}"'.format(value)) 
    return data 
  
# gets emails under the label. for example: Inbox
def get_emails(result_bytes): 
    msgs = []
    for num in result_bytes[0].split(): 
        typ, data = con.fetch(num, '(RFC822)') 
        msgs.append(data) 
  
    return msgs

def yoxla(decoded):
    for mesaj in msgs[-1][0]:
        decoded = mesaj.decode("UTF-8")
        startpoint = decoded.find(emailconf.incomingfrom)
        messagestart = decoded.find("Content-Type: text/plain; charset=\"UTF-8\"", startpoint)
        endpoint = decoded.find("Content-Type: text/html; charset=\"UTF-8\"")
        datestart = decoded.find("Date", startpoint)
        dateend = decoded.find("+", datestart)-1
        with open("lastread.txt", "w") as file:
            file.truncate(0)
            file.write(decoded[datestart:dateend])
        if emailconf.triggermessage in decoded[messagestart:endpoint]:
            print("Keyword was found, but message might be old. If email is sent, next line will tell it.")
            if os.path.isfile("lastsent.txt") == True:
                fhand = open("lastsent.txt", "r+")
                if decoded[datestart:dateend] not in fhand.read():
                    print("emailsent")
                    #send email line below
                    gondergetsin()
                fhand.truncate(0)
                fhand.seek(0)
                fhand.write(decoded[datestart:dateend])
                fhand.close() 
            else:
                with open("lastsent.txt", "w") as fhand2:
                    fhand2.truncate(0)
                    fhand2.write(decoded[datestart:dateend])
                print("file created, email sent")
                #send email line below.
                gondergetsin()
con = imaplib.IMAP4_SSL(emailconf.imap_url)  
con.login(emailconf.user, emailconf.password)  
con.select(emailconf.label)  
msgs = get_emails(search('FROM', emailconf.incomingfrom, con))