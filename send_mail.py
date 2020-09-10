#!/usr/bin/python3
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep
import argparse

# Construct object fot the argument parser
ap = argparse.ArgumentParser()
# sender,pwd,receiver,sub,testcase_name
# Add the arguments to the parser
ap.add_argument("-s", "--Sender", required=True,
                help="give sender address to send fax")
ap.add_argument("-p", "--password", required=True,
                help="password of sender to login to client")
ap.add_argument("-sub", "--subject", required=True,
                help="destination  fax number")
ap.add_argument("-f", "--attachment", required=False,
                help="make sure to file in present dir modified.pdf ")
ap.add_argument("-e", "--Env", required=True,
                help="which env to test dev/sta/prod")
args = vars(ap.parse_args())

if args['Env'] == "dev":
    to = "fax_dev@magicjackforbusiness.com"
elif args['Env'] == "sta":
    to = "fax_sb@magicjackforbusiness.com"
else:
    to = "fax@magicjackforbusiness.com"


def get_domain(email):
    str = email.split('@')
    if "gmail" in str[1]:
        return "smtp.gmail.com"
    elif "corp" in str[1]:
        return "smtp-mail.outlook.com"
    elif "yahoo" in str[1]:
        return "smtp.mail.yahoo.com"


# instance of MIMEMultipart
msg = MIMEMultipart()
msg['From'] = args['Sender']  # senders email address
msg['To'] = to  # receivers email address
msg['Subject'] = args['subject']  # subject
domain = get_domain(args['Sender'])
body = "To:sta11\nCompany:uol\nRe:test\nMessage:\n//"  # the body of the mail
msg.attach(MIMEText(body, 'plain'))  # attach body with the msg
filename = args['attachment']  ## file to be sent
print("file size:{}Kb".format(round(os.stat(filename).st_size / 1024)))
attachment = open(filename, "rb")
p = MIMEBase('application', 'octet-stream')  ## instance of MIMEBase and named as p
p.set_payload(attachment.read())  ## To change the payload into encoded form
encoders.encode_base64(p)  ## encode into base64
p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
msg.attach(p)  # attach the instance 'p' to instance 'msg'
print("creating SMTP session to:",domain)
s = smtplib.SMTP(domain, 587)  ## creates SMTP session
s.starttls()  ## start TLS for security
if s.login(args['Sender'], args['password']):  # login to email
    print("login success to:", args['Sender'])
text = msg.as_string()  # Converts the Multipart msg into a string
for i in range(1, 2):
    s.sendmail(args['Sender'], to, text)  # sending the mail
    print("No:{}:sent fax to sender:{},sent to:{}, destination fax number:{}".format(i,
                                                                                     args['Sender'], to,
                                                                                     args['subject']))
    sleep(3)
s.quit()  # terminating the session
