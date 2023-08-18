from django.http import JsonResponse
from rest_framework import status
import jwt
import os
from .models import CustomUser
def user_authentication_middleware(get_response):
    def middleware(request):
        if(request.path.startswith("/customer") or request.path.startswith("/agent") ):
            if 'Authorization' not in request.headers:
              return JsonResponse({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
            token = request.headers['Authorization'].split()[1]
            try:
                decoded_token = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
                user_id = decoded_token["user_id"]
                user = CustomUser.objects.filter(id=user_id).first()
                              
                if(user ):
                    if(request.path.startswith("/client") and user.category!="client"):
                        return JsonResponse({'error': 'Please login as agent, Not an client'}, status=status.HTTP_401_UNAUTHORIZED)
                    if(request.path.startswith("/agent") and user.category!="agent"):
                        return JsonResponse({'error': 'Please login as client, Not an agent!'}, status=status.HTTP_401_UNAUTHORIZED)
             
                    request.user_details=user                   
                    return get_response(request)
                return JsonResponse({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                return JsonResponse({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        return get_response(request)
    return middleware
