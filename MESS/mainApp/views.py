#rest framework
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings


#3rd party
from multiprocessing import Pool
import base64
import re
import os
import threading


#local
from . import email as sendEmailMethod
from . import serializers
from . import models
from . import telegram


class HomeView(APIView):
    permission_classes = (IsAuthenticated, )   
    def get(self, request):
        content = {'message': 'Welcome to the JWT Authentication page using React Js and Django!'}  
        return Response(content)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):  
        try:               
            refresh_token = request.data["refresh_token"]               
            token = RefreshToken(refresh_token)               
            token.blacklist()               
            return Response(status=status.HTTP_205_RESET_CONTENT)          
        except Exception as e:               
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def addSubscriber(request):
    response=''

    try:
        email=request.data["email"]
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if re.match(regex, email):
            if not models.Subscriber.objects.filter(email=email).exists() or True :
                q=models.Subscriber(email=email)
                emailtemplate=models.HtmlTeplates.objects.get(name='newuseremail')

                receiver=email
                Subject=emailtemplate.Subject
                htmlEncoded=emailtemplate.htmlEncoded

                #send mail to new user
                # emailresult=sendSingleMail(receiver,Subject,htmlEncoded)
                # Create a thread for the background function with parameters
                background_thread = threading.Thread(sendSingleMail=sendSingleMail, args=(receiver,Subject,htmlEncoded))
                # Start the thread
                background_thread.start()
                # Continue with the rest of your code


                if emailresult or True:
                    q.save()
                    response={"status":"ok"}
                    telegram.send_msg_to_telegram("new user regrestrd named "+str(email))
                    #notife me on telegram
                    # try:
                    #     telegram.send_msg_to_telegram("new user regrestrd named "+str(email))
                    # except:
                    #     pass
                else:
                    response={"status":"errror in sending invite mail"}    
            else:
                response={"status":"email already exist"}
        else:
            response={"status":"Invalid Email"}

    except Exception as e:
        response={"status":"error",
                    "error":str(e)
        }
    
    return Response(response)

@api_view(['GET'])
#@permission_classes((IsAuthenticated, ))
def getSubs(request):
    allSubscribers=models.Subscriber.objects.all()

    Serializer = serializers.SubscriberSerializer(allSubscribers,many=True)
    #Serializer = Serializer.data
    #content = JSONRenderer().render(serializer.data)

    return Response(Serializer.data)
    
@api_view(['POST'])
#@permission_classes((IsAuthenticated, ))
def delSubs(request):
    id=request.data["id"]
    response=''
    if models.Subscriber.objects.filter(id=id).exists():
        try:
            models.Subscriber.objects.filter(id=id).delete()
            response={"status":"ok"}
        except:
            response={"status":"unknown error during inserting"}
    else:
        response={"status":"404"}
    
    return Response(response)

def updateDB(paremail):
    response={}
    totalsubscriber=len(subscrubers)
    successMail=0
    failedMail=0

    try:
        successMail+=1
        receiver_email=paremail
        Subject="مجله متاوا | METAVA"
        emailresult=sendEmailMethod.sendMail(receiver_email,Subject,html)
        if  emailresult:
            response[paremail]="ok"
    except:
        failedMail+=1
        response[paremail]="error"

    totalMail=successMail+failedMail
    successMailPercent=successMail/totalMail
    successMailPercent*=100

    response={
        "total subscribers":totalsubscriber,
        "toal email":totalMail,
        "success email":successMail,
        "failed email":failedMail,
        "email success percent":successMailPercent,
    }
    print(str(response))
    return response

@api_view(['POST'])
#@permission_classes((IsAuthenticated, ))
def sendmailtoallsubs_paraler(request):
    subscrubers = models.Subscriber.objects.all()
    receiver_emails=[]
    Subject=request.data["Subject"]
    #html=request.data["html"]
    htmlEncoded=request.data["html"]
    htmlDecoded=base64.b64decode(htmlEncoded).decode('utf-8')

    for subscruber in subscrubers:
        receiver_emails+=[subscruber.email]

    emailresult=sendEmailMethod.send_paraler_mail(receiver_emails,Subject,htmlDecoded)
    
    return Response(emailresult)

@api_view(['POST'])
#@permission_classes((IsAuthenticated, ))
def sendtstmail(request):
    receiver = request.data["receiver"]
    Subject=request.data["Subject"]
    htmlEncoded=request.data["html"]
    
    emailresult=sendSingleMail(receiver,Subject,htmlEncoded)
    return Response(emailresult)

def sendSingleMail(receiver,Subject,html):
    receiver_emails=[]
    subscruber = receiver
    receiver_emails.append(subscruber)
    Subject=Subject
    htmlEncoded=html
    htmlDecoded=base64.b64decode(htmlEncoded).decode('utf-8')
    emailresult=sendEmailMethod.send_paraler_mail(receiver_emails,Subject,htmlDecoded)

    return Response(emailresult)


@api_view(['GET'])
def send_db_in_telegram(request,telid):
    telegram_id=telid


    db_dile = os.path.join(settings.BASE_DIR, "db.sqlite3")

    
    responce=telegram.send_file_to_telegram(telegram_id,db_dile)

    return Response({'status':responce})


















