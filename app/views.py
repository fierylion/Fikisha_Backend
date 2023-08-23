from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .serializers import CustomUserSerializer, ProductRegistrationModalSerializer, TransportRequestModalSerializer, TrackDeliveryModalSerializer, FeedbackModalSerializer

from .models import CustomUser, ProductRegistrationModal, TransportRequestModal, TrackDeliveryModal, FeedbackModal
import os
import jwt
from django.forms import model_to_dict



class ClientView(ViewSet):
    def create_single_user(self, request):
        request.data["category"]="client"
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data
            del user_data["password"]
            encoded_token=jwt.encode({"user_id":user_data["id"] }, os.getenv("JWT_SECRET"), algorithm="HS256")

            return Response({"customer":user_data, "token":encoded_token, "status":'success'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def login_single_user(self, request):
        email = request.data.get("email")
        password=request.data.get("password")
        if(email):
            user=CustomUser.objects.filter(email=email).first()
            if(user):
                if(user.category!="client"):
                    return Response({"msg":"Email does not exist"}, status=status.HTTP_400_BAD_REQUEST)
                obtained_password = user.password
                if(password==obtained_password):
                    encoded_token = jwt.encode({"user_id":str(user.id) }, os.getenv("JWT_SECRET"), algorithm="HS256")
                    return Response({"customer":{
                        "id":str(user.id),
                        "email":user.email,
                        'category':user.category,

                    }, "token":encoded_token, "status":"success" }, status=status.HTTP_200_OK)
                return Response({"msg":"password is not correct!", "status":"failed"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"msg":"Email doesn\'t exist!", "status":"failed"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg":"Please provide email!"}, status=status.HTTP_400_BAD_REQUEST)
    def get_details(self, request):
        user=request.user_details
        user_data=model_to_dict(user)
        #orders
        orders=ProductRegistrationModal.objects.filter(client_id=user).count()
        #successful orders
        successfull_orders = TransportRequestModal.objects.filter(client=user,  status='delivered').count()


        del user_data["password"]
        return Response({"customer":user_data, "successfull_orders":successfull_orders,"orders":orders,  "status":"success"}, status=status.HTTP_200_OK)
    def create_order(self, request):
        user=request.user_details
        request.data["client_id"]=user.id
        serializer = ProductRegistrationModalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"success"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get_orders(self, request):
        def get_transport_fields(item):
            try:
                return model_to_dict(item.transportrequestmodal)
            except Exception as err:
                return None
        
        user=request.user_details
        orders=ProductRegistrationModal.objects.select_related('transportrequestmodal').filter(client_id=user)
        data = []
        for item in orders:
            data.append({**model_to_dict(item),
            "transport":get_transport_fields(item)
                         })
        return Response({"orders": data, "status":"success"}, status=status.HTTP_200_OK)


                

        
class AgentView(ViewSet):
    def create_single_user(self, request):
        request.data["category"]="agent"
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data
            del user_data["password"]
            encoded_token=jwt.encode({"user_id":user_data["id"] }, os.getenv("JWT_SECRET"), algorithm="HS256")

            return Response({"agent":user_data, "token":encoded_token, "status":'success'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def login_single_user(self, request):
        email = request.data.get("email")
        password=request.data.get("password")
        if(email):
            user=CustomUser.objects.filter(email=email).first()
            if(user):
                if(user.category!="agent"):
                    return Response({"msg":"Email does not exist"}, status=status.HTTP_400_BAD_REQUEST)
                obtained_password = user.password
                if(password==obtained_password):
                    encoded_token = jwt.encode({"user_id":str(user.id) }, os.getenv("JWT_SECRET"), algorithm="HS256")
                    return Response({"agent":{
                        "id":str(user.id),
                        "email":user.email,
                        'category':user.category,

                    }, "token":encoded_token, "status":"success" }, status=status.HTTP_200_OK)
                return Response({"msg":"password is not correct!", "status":"failed"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"msg":"Email doesn\'t exist!", "status":"failed"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg":"Please provide email!"}, status=status.HTTP_400_BAD_REQUEST)
    def get_details(self, request):
        user=request.user_details
        user_data=model_to_dict(user)
       
        #orders
        orders=0
        #successful orders
        successfull_orders = TransportRequestModal.objects.filter(agent=user,  status='delivered').count()


        del user_data["password"]
        return Response({'id':user.id,"agent":user_data, "successfull_orders":successfull_orders,"orders":orders,  "status":"success"}, status=status.HTTP_200_OK)
    def accept_order(self, request, order_id):
        user=request.user_details
        
        if(order_id):
            order=TransportRequestModal.objects.filter(product=str(order_id)).first()
            if(not order):
                try:
                    trans =  TransportRequestModal.objects.create(product=ProductRegistrationModal.objects.get(id=order_id), agent=user, status="pending")
                    order = trans.save()
                    return Response({"status":"success", 'order':order}, status=status.HTTP_201_CREATED)
                except Exception as err:
                    print(err)
                    return Response({"msg":"Order ID does not exist!", "status":"failed"}, status=status.HTTP_400_BAD_REQUEST)
                
               
            return Response({"msg":"Order already exist!", "status":"failed"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg":"Please provide order id!"}, status=status.HTTP_400_BAD_REQUEST)

    def get_orders(self, request):
        user=request.user_details
        orders=ProductRegistrationModal.objects.all()
        serializer = ProductRegistrationModalSerializer(orders, many=True)
        return Response({"orders":serializer.data, "status":"success"}, status=status.HTTP_200_OK)
    def get_accepted_orders(self, request):
        user=request.user_details
        orders=TransportRequestModal.objects.filter(agent=user)
        serializer = TransportRequestModalSerializer(orders, many=True)
        return Response({"orders":serializer.data, "status":"success"}, status=status.HTTP_200_OK)
    