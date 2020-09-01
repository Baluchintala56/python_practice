# libraries to be imported
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import imaplib
from email.parser import BytesParser
from datetime import datetime, timedelta
from time import sleep


def send_fax(sender, pwd, receiver, sub, testcase_name):
    fromaddr = sender
    toaddr = receiver
    # instance of MIMEMultipart
    msg = MIMEMultipart()
    msg['From'] = fromaddr  # senders email address
    msg['To'] = toaddr  # receivers email address
    msg['Subject'] = sub  # subject
    body = "To:sta11\nCompany:uol\nRe:test\nMessage:\n//"  # the body of the mail
    msg.attach(MIMEText(body, 'plain'))  # attach body with the msg
    filename = "modified.pdf"  ## file to be sent
    attachment = open("/home/balu/Downloads/modified.pdf", "rb")
    p = MIMEBase('application', 'octet-stream')  ## instance of MIMEBase and named as p
    p.set_payload((attachment).read())  ## To change the payload into encoded form
    encoders.encode_base64(p)  ## encode into base64
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)  # attach the instance 'p' to instance 'msg'
    s = smtplib.SMTP('smtp.gmail.com', 587)  ## creates SMTP session
    s.starttls()  ## start TLS for security
    s.login(fromaddr, pwd)  # login to email
    text = msg.as_string()  # Converts the Multipart msg into a string
    s.sendmail(fromaddr, toaddr, text)  # sending the mail
    print("{}:sent fax to sender:{},sent to:{}, destination fax number:{}".format(testcase_name, sender, receiver, sub))
    s.quit()  # terminating the session


def get_fax_headers(email, password, days):
    EMAIL_ACCOUNT = email
    PASSWORD = password
    n_days = days

    mail_handle = imaplib.IMAP4_SSL('imap.gmail.com')
    mail_handle.login(EMAIL_ACCOUNT, PASSWORD)
    print(mail_handle.list())  # using this we can see list of folder in account
    print(mail_handle.select('"[Gmail]/All Mail"'))
    # mail_handle.search(['ALL'])
    result, data = mail_handle.uid('search', None, "ALL", "SINCE 27-Aug-2020")  # search all email and return uids
    if result == 'OK':
        print(data[0].split())

        for num in data[0].split():
            result, data = mail_handle.uid('fetch', num, '(RFC822)')
            if result == 'OK':
                email_message = BytesParser().parsebytes(data[0][1])  # raw email text including headers
                if "Your fax was delivered" in email_message['Subject'] and date_checker(email_message['Date'], n_days):
                    print('From:' + email_message['From'])
                    print('Sender:' + email_message['Sender'])
                    print('Date:' + email_message['Date'])  # condition
                    print('Subject:' + email_message['Subject'])
                    print('X-Mailgun-Tag:' + email_message['X-Mailgun-Tag'])
                    print('fax_id:' + email_message['fax_id'])
                    print('Reply-To:' + email_message['Reply-To'])
                    print("\n")
                # else:
                # print("No matched mails found in last {} days".format(n_days))
            else:
                print("unable to fetch the email headers from uid....")
    else:
        print("Unable to search required folder....")


def date_checker(email_time, n_days):
    tym = email_time
    N = n_days
    mail_to_get = datetime.strptime(tym, "%a, %d %b %Y %H:%M:%S %Z").strftime("%Y,%m,%d,%H,%M,%S")
    present = datetime.now() - timedelta(days=N)
    if present.strftime("%Y,%m,%d,%H,%M,%S") < mail_to_get:
        return True
    else:
        return False


# case1: send fax to correct destination
# send_fax("mjbhyd.dev@gmail.com", "Passw0rd1234", "fax_dev@magicjackforbusiness.com", "9999919066", "success fax case")
# case2:send fax to direct line number
# send_fax("mjbhyd.dev@gmail.com","Passw0rd1234","fax_dev@magicjackforbusiness.com","6787629195","sent fax to direct line number")
# case3: send fax to unknown number
# send_fax("mjbhyd.dev@gmail.com","Passw0rd1234","fax_dev@magicjackforbusiness.com","9898989898","sent fax to Unkown number")
# case4: send fax from unknown sender address(make sure that email should not associate to any fax account)
# send_fax("mjbtest@gmail.com","Passw0rd1234","fax_dev@magicjackforbusiness.com","9898989898","sent fax from Unkown sender email")

sleep(1200)

get_fax_headers("mjbhyd.dev@gmail.com", "Passw0rd1234", 7)
