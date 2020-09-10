import imaplib
from email.parser import BytesParser


def get_fax_headers(email, password):
    mailgun_count = aws_count = mails_count = 0
    domain=domain2=''
    EMAIL_ACCOUNT = email
    PASSWORD = password

    mail_handle = imaplib.IMAP4_SSL('imap.gmail.com')
    mail_handle.login(EMAIL_ACCOUNT, PASSWORD)
    mail_handle.list()  # using this we can see list of folder in account
    mail_handle.select('"[Gmail]/All Mail"')
    result, data = mail_handle.uid('search', None, "ON 04-Sep-2020","FROM fax@magicjackforbusiness.com")  # search all email and return uids
    if result == 'OK':
        for num in data[0].split():
            result, data = mail_handle.uid('fetch', num, '(RFC822)')
            if result == 'OK':
                email_message = BytesParser().parsebytes(data[0][1])  # raw email text including headers
                #if "You've received a fax from magicJack for BUSINESS" or "Your fax was delivered" or "Something went wrong" in email_message[
                   # 'Subject']:
                if "Something went wrong" in email_message['Subject']:

                    mails_count += 1
                    for st in email_message.items():
                        if ".magicjack.com" in st[1]:
                            domain = st[1][5:27]
                            # aws.append(st[1][:27])
                            aws_count = aws_count + 1
                            print()
                        elif "mailgun.net" in st[1]:
                            domain2 = st[1][5:23]
                            mailgun_count = mailgun_count + 1

        print("total fax mails sent:", mails_count)
        print("mails sent from aws {} :{}".format(domain, aws_count))
        print("mails sent from mailgun {} :{}".format(domain2, mailgun_count))


get_fax_headers("mjbhyd.dev@gmail.com", "Passw0rd1234")
