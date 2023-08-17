from django.http import JsonResponse
from rest_framework import status
import jwt
import os
from .models import CustomUser
def user_authentication_middleware(get_response):
    def middleware(request):
        if(request.path.startswith("/user") and request.path !="/user/payment/callback" ):
            if 'Authorization' not in request.headers:
              return JsonResponse({'error': 'User not    authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
            token = request.headers['Authorization'].split()[1]
            try:
                decoded_token = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
                user_id = decoded_token["user_id"]
                user = CustomUser.objects.filter(id=user_id).first()
                              
                if(user ):
                    if(user.paid==False and request.path !="/user/payment/generate"):
                        return JsonResponse({'email':user.email, 'paid':False}, status=status.HTTP_200_OK)
             
                    request.user_details=user                   
                    return get_response(request)
                return JsonResponse({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                return JsonResponse({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        return get_response(request)
    return middleware
