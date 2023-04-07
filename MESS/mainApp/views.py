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
        if not models.Subscriber.objects.filter(email=email).exists():
            q=models.Subscriber(email=email)
            q.save()
            response={"status":"ok"}
        else:
            response={"status":"email already exist"}
            
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





    























