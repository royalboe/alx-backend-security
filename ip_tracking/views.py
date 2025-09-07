# ip_tracking/views.py
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.response import Response
from rest_framework import status

class LoginAnonThrottle(AnonRateThrottle):
    rate = '5/minute'

class LoginUserThrottle(UserRateThrottle):
    rate = '10/minute'

@api_view(['POST'])
@throttle_classes([LoginAnonThrottle, LoginUserThrottle])
def login_view(request):
    # Your login logic here
    return Response({"message": "Login attempt processed."}, status=status.HTTP_200_OK)


# Create your views here.
