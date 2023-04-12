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
    try:
        email=request.data["email"]
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if re.match(regex, email):
            if not models.Subscriber.objects.filter(email=email).exists() or True:
                q=models.Subscriber(email=email)
                Subject="به متاوا خوش آمدید"
                receiver_email=email
                emailresult=sendEmailMethod.sendMail(receiver_email,Subject,html)
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
         <p>مجله مجله مجله</p>
         <p>ماهنامه مجله اینههههه</p>
         <p>با عرض احترام</p>
         <p>امین</p>
      </main>
      <footer style="background-color: #75e645; padding: 10px; text-align: center;">
         <p style="font-size: 12px; margin: 0;">تمام حقوق متوا هست © 2023</p>
      </footer>
   </body>
</html>


    """


@api_view(['GET'])
#@permission_classes((IsAuthenticated, ))
def sendmailtoallsubs(request):
    response={}
    subscrubers = models.Subscriber.objects.all()

    totalsubscriber=len(subscrubers)
    successMail=0
    failedMail=0



    
    for subscruber in subscrubers:
        try:
            successMail+=1
            receiver_email=subscruber.email
            Subject="مجله متاوا | METAVA"
            emailresult=sendEmailMethod.sendMail(receiver_email,Subject,html)
            if  emailresult:
                response[subscruber.email]="ok"
        except:
            failedMail+=1
            response[subscruber.email]="error"

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
            
    return Response(response)


    























