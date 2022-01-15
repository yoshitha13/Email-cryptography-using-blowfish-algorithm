import imaplib
import email
from email.header import decode_header
from algo import decrypt_msg
import warnings
warnings.filterwarnings('ignore')
    
# account credentials
username = "receiverblowfish@gmail.com"
password = "Receiver@2021"

def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)
# create an IMAP4 class with SSL 
imap = imaplib.IMAP4_SSL("imap.gmail.com")
# authenticate
imap.login(username, password)
status, messages = imap.select("INBOX")
# number of top emails to fetch
N = 1
# total number of emails
messages = int(messages[0])
for i in range(messages, messages-N, -1):
    # fetch the email message by ID
    res, msg = imap.fetch(str(i), "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            # parse a bytes email into a message object
            msg = email.message_from_bytes(response[1])
            # decode the email subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                # if it's a bytes, decode to str
                subject = subject.decode(encoding)
            # decode email sender
            From, encoding = decode_header(msg.get("From"))[0]
            if isinstance(From, bytes):
                From = From.decode(encoding)
            print("Subject:", subject)
            print("From:", From)
            # if the email message is multipart
            if msg.is_multipart():
                # iterate over email parts
                for part in msg.walk():
                    # extract content type of email
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    try:
                        # get the email body
                        body = part.get_payload(decode=True).decode()
                    except:
                        pass
            else:
                # extract content type of email
                content_type = msg.get_content_type()
                # get the email body
                body = msg.get_payload(decode=True).decode()
                if content_type == "text/plain":
                    # print only text email parts
                    print("Received mail:", body)
                    print("----------------------------")
                    print("Decrypted message:", decrypt_msg(body))
                    print("----------------------------")
# close the connection and logout
print("MESSAGE DECRYPTED SUCCESSFULLY.", u'\u2713')
imap.close()
imap.logout()