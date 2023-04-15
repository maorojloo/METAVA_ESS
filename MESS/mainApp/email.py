from multiprocessing import Pool
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import dotenv
from django.conf import settings
from itertools import repeat


 
dotenv_file = os.path.join(settings.BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)


port = os.environ['port']
smtp_server = os.environ['smtp_server']
login =  os.environ['login']
password = os.environ['password']

def sendMail(receiver_email,Subject,html):
   Subject=Subject

   result={}
   try:
      sender_email = "ma.farahbakhsh@srbiau.ac.ir"
      receiver_email = receiver_email
      Subject= Subject
      html = html

      message = MIMEMultipart("alternative")
      message["Subject"] = Subject
      message["From"] = sender_email
      message["To"] = receiver_email

      part2 = MIMEText(html, "html")
      message.attach(part2)

      with smtplib.SMTP(smtp_server, port) as server:
         server.login(login, password)
         server.sendmail(sender_email, receiver_email, message.as_string())

      result={
         "receiver_email":receiver_email,
         "status":"ok",
      }
   except:
      result={
         "status":"error",
      }

    message = MIMEMultipart("alternative")
    message["Subject"] = Subject
    message["From"] = sender_email
    message["To"] = receiver_email

    part2 = MIMEText(html, "html")
    message.attach(part2)

    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    result={
        "receiver_email":receiver_email,
        "status":"ok",
    }
#    except:
#       result={
#          "status":"error",
#       }

    return result



def send_paraler_mail(recelist,Subject,html):
    result=[]
    with Pool(7) as p:
       # result += p.map(sendMail,recelist)
        result += p.starmap(sendMail, zip(recelist, repeat(Subject), repeat(html)))
    return result


def sendMail_new_user(receiver_email):
    Subject="به متاوا خوش آمدید"
    html="""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>مجله متاوا</title>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                </head>
                <body style="background-color: #5fdec9; font-family: Arial, sans-serif; font-size: 14px; line-height: 1.5; margin: 0; padding: 0;">
                    <header style="float: none; background-color: #5fdec9; padding: 10px; ">
                        <h1 style="font-size: 24px; margin: 0;">مجله متاوا</h1>
                    </header>
                    <main style="background-color: #5fdec9; padding: 20px;">
                        <p>سلام</p>
                        <p>به سامانه دریافت مجله متاوا خوش امدید</p>
                        <p>با عرض احترام</p>
                        <p>امین</p>
                    </main>
                    <footer style="background-color: #75e645; padding: 10px; text-align: center;">
                        <p style="font-size: 12px; margin: 0;">تمام حقوق متوا هست © 2023</p>
                    </footer>
                </body>
                </html>
        """
    result={}
    try:
        sender_email = login
        receiver_email = receiver_email
        Subject= Subject
        html = html

        message = MIMEMultipart("alternative")
        message["Subject"] = Subject
        message["From"] = sender_email
        message["To"] = receiver_email

        part2 = MIMEText(html, "html")
        message.attach(part2)

        with smtplib.SMTP(smtp_server, port) as server:
            server.login(login, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        result={
            "receiver_email":receiver_email,
            "status":"ok",
        }
    except:
        result={
            "status":"error",
        }

    return result
