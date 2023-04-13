from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import serializers
from . import models
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from . import email as sendEmailMethod
import re
from multiprocessing import Pool



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
            if not models.Subscriber.objects.filter(email=email).exists() :
                q=models.Subscriber(email=email)
                
                receiver_email=email
                emailresult=sendEmailMethod.sendMail_new_user(receiver_email)
                if emailresult:
                    q.save()
                    response={"status":"ok"}
                else:
                    response={"status":"errror in sending invite mail"}    
            else:
                response={"status":"email already exist"}
        else:
            response={"status":"Invalid Email"}

    except:
        response={"status":"unknown error during inserting"}
    
    return Response(response)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def getSubs(request):
    allSubscribers=models.Subscriber.objects.all()

    Serializer = serializers.SubscriberSerializer(allSubscribers,many=True)
    #Serializer = Serializer.data
    #content = JSONRenderer().render(serializer.data)

    return Response(Serializer.data)

    
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
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
    #code goes here...
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


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def sendmailtoallsubs_paraler(request):

    subscrubers = models.Subscriber.objects.all()

    receiver_emails=[]
    for subscruber in subscrubers:
        receiver_emails+=[subscruber.email]

    emailresult=sendEmailMethod.send_paraler_mail(receiver_emails)
    
    return Response(emailresult)
























