from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .serializers import CustomUserSerializer,  OrderPartiesModalSerializer, OrderLocationModalSerializer, OrderModalSerializer,OrderDeliveryModalSerializer, FeedbackModalSerializer,AgentPaymentModalSerializer, LocationModalSerializer
import json
from django.core import serializers

from .models import CustomUser, OrderLocationModal, OrderPartiesModal, OrderModal,FeedbackModal, OrderDeliveryModal, AgentPaymentModal, LocationModal
import os
import jwt
from django.forms.models import model_to_dict
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from json import JSONEncoder
from uuid import UUID
from django.db.models import Q
import json
import uuid
old_default = JSONEncoder.default

def new_default(self, obj):
    if isinstance(obj, UUID):
        return str(obj)
    return old_default(self, obj)

JSONEncoder.default = new_default



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
        phone = request.data.get("phone")
        password=request.data.get("password")
        if(phone):
            user=CustomUser.objects.filter(phone=phone).first()
            if(user):
                if(user.category!="client"):
                    return Response({"msg":"Email does not exist"}, status=status.HTTP_400_BAD_REQUEST)
                obtained_password = user.password
                if(password==obtained_password):
                    encoded_token = jwt.encode({"user_id":str(user.id) }, os.getenv("JWT_SECRET"), algorithm="HS256")
                    return Response({"customer":{
                        "id":str(user.id),
                        "phone":user.phone,
                        'name':user.name,
                        'category':user.category,

                    }, "token":encoded_token, "status":"success" }, status=status.HTTP_200_OK)
                return Response({"msg":"password is not correct!", "status":"failed"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"msg":"Email doesn\'t exist!", "status":"failed"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg":"Please provide email!"}, status=status.HTTP_400_BAD_REQUEST)
    @staticmethod
    def send_order_to_drivers(order_data):
        """
        Send an order to the "drivers_group" channel group.

        """
        channel_layer = get_channel_layer()
        try:
        
            async_to_sync(channel_layer.group_send)(
                "drivers_group",
                {
                    "type": "send_order",
                    "data": order_data,
                },
            )
        except Exception as e:
            print(e)
    def create_location(self, request):
        user = request.user_details
        location = request.data.get('location')
        phone= request.data.get('phone')
        name = request.data.get('name')
        extra = request.data.get('extra')

        if(not location):
            print(location, 'adfafaf')
            return Response({"msg":"Please provide location"}, status=status.HTTP_400_BAD_REQUEST)
        fkId ='FK'+ str(uuid.uuid4()).replace('-', '')[0:7]
        location_serializer = LocationModalSerializer(data={
            "location":location,
            "fkID":fkId,
            "phone":phone,
            "name":name,
            "extra":extra,
            "user_id":str(user.id)
        })
        if(location_serializer.is_valid()):
            location_serializer.save()
            return Response({"location":location_serializer.data, "status":"success"}, status=status.HTTP_201_CREATED)
     
        return Response({"msg":location_serializer.errors, "status":"failed"}, status=status.HTTP_400_BAD_REQUEST)
    def get_all_locations(self, request):
        locations = LocationModal.objects.filter(
            user_id = str(request.user_details.id)
        ).order_by('-created_at')
        data =[
            
        ]
        for location in locations:
            temp = model_to_dict(location)
            temp['location_id'] = location.id
            temp['created_at'] = location.created_at
            temp['updated_at'] = location.updated_at
            data.append(temp)

        
        return Response({"locations":data, "status":"success"}, status=status.HTTP_200_OK)
    def get_single_location(self, request, location_id):
        user = request.user_details
        location = LocationModal.objects.filter(
            fkID= location_id
        ).first()
        if(not location):
            return Response({"status":"failed"}, status=status.HTTP_400_BAD_REQUEST)
        temp = model_to_dict(location)
        temp['updated_at'] = location.updated_at
        temp['created_at']= location.created_at
        temp['id']=location.id
        return Response({"location":temp, "status":"success"}, status=status.HTTP_200_OK)
    


    
    def create_order(self, request):
        user = request.user_details
        data = request.data.get('request', {})
        client_id = user.id

        sender_info = data.get('senderInformation', {})
        receiver_info = data.get('receiverInformation', {})

        sender_location_data = sender_info.get('location', {})
        receiver_location_data = receiver_info.get('location', {})

        sender_location_serializer = OrderLocationModalSerializer(data=sender_location_data)
        receiver_location_serializer = OrderLocationModalSerializer(data=receiver_location_data)

        if not sender_location_serializer.is_valid() or not receiver_location_serializer.is_valid():
            errors = {
                'sender_location_errors': sender_location_serializer.errors,
                'receiver_location_errors': receiver_location_serializer.errors
            }
            return Response({'msg': errors}, status=status.HTTP_400_BAD_REQUEST)

        sender_location = sender_location_serializer.save()
        receiver_location = receiver_location_serializer.save()

        sender_party_serializer = OrderPartiesModalSerializer(data={
            "name": sender_info.get("name", ""),
            "phone": sender_info.get("phone", ""),
            "location_id": sender_location.id
        })

        receiver_party_serializer = OrderPartiesModalSerializer(data={
            "name": receiver_info.get("name", ""),
            "phone": receiver_info.get("phone", ""),
            "location_id": receiver_location.id
        })

        if not sender_party_serializer.is_valid() or not receiver_party_serializer.is_valid():
            errors = {
                'sender_party_errors': sender_party_serializer.errors,
                'receiver_party_errors': receiver_party_serializer.errors
            }
            return Response({'msg': errors}, status=status.HTTP_400_BAD_REQUEST)

        order_serializer = OrderModalSerializer(data={
            'user_id': client_id,
            "category": data.get("category", ""),
            "fee": request.data.get("fee", ""),
            "payment_means": request.data.get("payMeans", ""),
            "payment_method": request.data.get("payWith", ""),
            "companyFee": request.data.get('companyFee', ''),
            "distance": request.data.get('distance', ''),
            "duration": request.data.get('duration', ''),
            "payment_by": request.data.get("payBy", ""),
            "sender_id": sender_party_serializer.save().id,
            "receiver_id": receiver_party_serializer.save().id,
        })

        if order_serializer.is_valid():
            order_serializer.save()
            # serializing using json to overcome uuid serialization error
            sender_location = dict(sender_location_serializer.data)
            receiver_location = dict(receiver_location_serializer.data)
            sender_party = dict(sender_party_serializer.data)
            receiver_party = dict(receiver_party_serializer.data)
            order = dict(json.loads(json.dumps(order_serializer.data)))
            sender_party['location_id'] = json.loads(json.dumps(sender_location))
            receiver_party['location_id'] = json.loads(json.dumps(receiver_location))

            order['sender_id']= json.loads(json.dumps(sender_party))
            order['receiver_id']= json.loads(json.dumps(receiver_party))
            self.send_order_to_drivers({
                'type':'new_order'
            })
            return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
        

        return Response({'msg': order_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    def getAllOrders(self, request, state):
        
        user =request.user_details
        # All pending and accepted orders
        query = Q(status='pending') | Q(status='accepted')
        if(state=='completed'):
            query = Q(status='delivered') | Q(status='cancelled')
        

        orders = OrderModal.objects.select_related(
        'sender_id', 'receiver_id', 'sender_id__location_id', 'receiver_id__location_id').filter(query,  user_id=user.id )
        data = []
        
        for order in orders:
            temp =model_to_dict(order)
            temp['order_id'] = order.id
            temp['created_at'] = order.created_at
            temp['updated_at'] = order.updated_at
            temp['sender_id'] = model_to_dict(order.sender_id)
            temp['receiver_id'] = model_to_dict(order.receiver_id)
            temp['sender_id']['location_id'] = model_to_dict(order.sender_id.location_id)
            temp['receiver_id']['location_id'] = model_to_dict(order.receiver_id.location_id)
            data.append(temp)
        return Response({"orders":data, "status":"success"}, status=status.HTTP_200_OK) 
    def getSingleOrder(self, request, order_id):
        user=request.user_details
        order = OrderModal.objects.select_related(
        'sender_id', 'receiver_id', 'sender_id__location_id', 'receiver_id__location_id').filter(id=order_id).first()
        if(not order):
            return Response({"order":None, "status":"success"}, status=status.HTTP_200_OK)
        # order details
        temp =model_to_dict(order)
        temp['order_id'] = order.id
        temp['created_at'] = order.created_at
        temp['updated_at'] = order.updated_at
        temp['sender_id'] = model_to_dict(order.sender_id)
        temp['receiver_id'] = model_to_dict(order.receiver_id)
        temp['sender_id']['location_id'] = model_to_dict(order.sender_id.location_id)
        temp['receiver_id']['location_id'] = model_to_dict(order.receiver_id.location_id)
        delivery=None
        if(order.status=='accepted' or order.status=='delivered'):
            delTemp = OrderDeliveryModal.objects.select_related('agent_id').filter(order_id=order).first()
            delivery = model_to_dict(delTemp)
            delivery['agent_id']=model_to_dict(delTemp.agent_id)
            delivery['agent_id']['id'] = delTemp.agent_id.id
            delivery['delivery_id']=delTemp.id
        return Response({"details":{
            "order":temp,
            "delivery":delivery
        }, "status":"success"}, status=status.HTTP_200_OK)
    def cancel_order(self, request, order_id):
        user = request.user_details
        if(order_id):
            order=OrderModal.objects.filter(id=order_id).first()
            if(not order):
                return Response({"msg":"Order ID does not exist!", "status":"failed"}, status=status.HTTP_400_BAD_REQUEST)
            if(order.status=="pending"):
                order.status="cancelled"
                order.save()
                return Response({"status":"success"}, status=status.HTTP_201_CREATED)
            return Response({"msg":"Order already accepted!", "status":"failed"}, status=status.HTTP_400_BAD_REQUEST)

    def receive_customer_feedback(self, request):
        user = request.user_details
        user_id = user.id
        delivery_id = request.data.get('delivery_id', '')
        order_id = request.data.get('order_id', '')
        comment = request.data.get('comment', '')
        rating = request.data.get('rating', '') # no rating  equates to 0
        print(order_id, delivery_id)
        if(order_id):
            try:
                order= OrderModal.objects.get(id=order_id)
            except:
                print('invalid order id')
                Response({"msg":'Invalid delivery id'}, status=status.HTTP_400_BAD_REQUEST)
            delivered_serializer = OrderModalSerializer(order,data={
                
                "status":"delivered"
            }, partial=True)
            if delivered_serializer.is_valid():
                delivered_serializer.save()
            else:
                print(delivered_serializer.errors)
                return Response({"msg":delivered_serializer.errors, "status":"failed"}, status=status.HTTP_400_BAD_REQUEST)
            #payment
            #fetch payment details of delivery
            delivery= OrderDeliveryModal.objects.get(id=delivery_id)
            agent_payment = AgentPaymentModal.objects.filter(agent_id=delivery.agent_id).first()
            if(agent_payment):
                agent_payment.amount = agent_payment.amount + delivery.order_id.fee 
                agent_payment.fee= agent_payment.fee + delivery.order_id.companyFee
            else:
                AgentPaymentModal.objects.create(agent_id=user, amount=delivery.order_id.fee, fee=delivery.order_id.companyFee).save()
        return Response({"status":"success"}, status=status.HTTP_201_CREATED)
            
        
        #     serializer = FeedbackModalSerializer(data={
        #         "delivery_id":delivery_id,
        #         "user_id":user_id,
        #         "comment":comment,
        #         "rating":rating
        #     })
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response({"status":"success"}, status=status.HTTP_201_CREATED)
        #     print(serializer.errors)
        #     return Response({"msg":"Invalid request", "status":"failed"}, status=status.HTTP_400_BAD_REQUEST)
          
        # return Response({"msg":"Please provide delivery id and feedback!"}, status=status.HTTP_400_BAD_REQUEST)
                

      
    

            
                

        
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
        phone = request.data.get("phone")
        password=request.data.get("password")
        if(phone):
            user=CustomUser.objects.filter(phone=phone).first()
            if(user):
                if(user.category!="agent"):
                    return Response({"msg":"Email does not exist"}, status=status.HTTP_400_BAD_REQUEST)
                obtained_password = user.password
                if(password==obtained_password):
                    encoded_token = jwt.encode({"user_id":str(user.id) }, os.getenv("JWT_SECRET"), algorithm="HS256")
                    return Response({"agent":{
                        "id":str(user.id),
                        "phone":user.phone,
                        'name':user.name,

                        'category':user.category,

                    }, "token":encoded_token, "status":"success" }, status=status.HTTP_200_OK)
                return Response({"msg":"password is not correct!", "status":"failed"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"msg":"Email doesn\'t exist!", "status":"failed"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg":"Please provide email!"}, status=status.HTTP_400_BAD_REQUEST)
    def get_orders(self, request):
        # q: I want to get all orders from order modal with all the fields from order parties modal and order location modal
        # a: use select_related
        orders=OrderModal.objects.select_related('sender_id', 'receiver_id', 'sender_id__location_id', 'receiver_id__location_id').filter(status="pending")
        data = []
        
        for order in orders:
           
            temp =model_to_dict(order)
            temp['order_id'] = order.id
            temp['created_at'] = order.created_at
            temp['updated_at'] = order.updated_at
            temp['sender_id'] = model_to_dict(order.sender_id)
            temp['receiver_id'] = model_to_dict(order.receiver_id)
            temp['sender_id']['location_id'] = model_to_dict(order.sender_id.location_id)
            temp['receiver_id']['location_id'] = model_to_dict(order.receiver_id.location_id)
            data.append(temp)
        
        return Response({"orders":data, "status":"success"}, status=status.HTTP_200_OK) 
    @staticmethod
    def update_user_orders(user_id):
        """
        Send an order to the "drivers_group" channel group.

        """
        channel_layer = get_channel_layer()
        try:
        
            async_to_sync(channel_layer.group_send)(
                f"user_{user_id}",
                {
                    "type":'update_user_orders',
                   'data':'pending'
                },
            )
        except Exception as e:
            print(e)
    def place_order(self, request, order_id):
        user=request.user_details
        agent_id = user.id
        location =  json.dumps(request.data.get('location'))
       
      
        if(order_id):
            order=OrderModal.objects.filter(id=order_id).first()
            if(not order):
              
                return Response({"msg":"Order ID does not exist!", "status":"failed"}, status=status.HTTP_400_BAD_REQUEST)
            if(order.status=="pending"):
                order.status="accepted"
               
                serializer = OrderDeliveryModalSerializer(data={
                    "order_id":order_id,
                    "agent_id":agent_id,
                    "location":location,
                })
                if serializer.is_valid():
                    
                    serializer.save()
                    order.save()
                    user_id = str(order.user_id.id)
                    
                    self.update_user_orders(user_id)
                    return Response({"status":"success"}, status=status.HTTP_201_CREATED)
                return Response({"msg":"Invalid request", "status":"failed"}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({"msg":"Order already accepted!", "status":"failed"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg":"Please provide order id!"}, status=status.HTTP_400_BAD_REQUEST)
    
    def get_pending_order(self, request):
        user = request.user_details
        agent_id = user.id
        order = OrderDeliveryModal.objects.select_related('order_id', 'order_id__sender_id', 'order_id__receiver_id', 'order_id__sender_id__location_id', 'order_id__receiver_id__location_id').filter(agent_id=agent_id, order_id__status='accepted').first()
        print(order)
        if(not order):
            return Response({"order":None, "status":"success"}, status=status.HTTP_200_OK)
        temp = model_to_dict(order)
        temp['delivery_id'] = order.id
        temp['paymentWith'] = order.order_id.payment_method
        temp['order_id'] = order.order_id.id
        temp['created_at'] = order.order_id.created_at
        temp['updated_at'] = order.order_id.updated_at
        temp['sender_id'] = model_to_dict(order.order_id.sender_id)
        temp['receiver_id'] = model_to_dict(order.order_id.receiver_id)
        temp['sender_id']['location_id'] = model_to_dict(order.order_id.sender_id.location_id)
        temp['receiver_id']['location_id'] = model_to_dict(order.order_id.receiver_id.location_id)
            
        return Response({"order":temp, "status":"success"}, status=status.HTTP_200_OK)
    def get_payments(self, request):
        user = request.user_details
        agent_id = user.id
        payments = AgentPaymentModal.objects.filter(agent_id=agent_id)
        data = []
        for payment in payments:
            temp = model_to_dict(payment)
            temp['id'] = payment.id
            temp['created_at'] = payment.created_at
            temp['updated_at'] = payment.updated_at
            data.append(temp)
        return Response({"payments":data, "status":"success"}, status=status.HTTP_200_OK)
    def get_delivered_orders(self, request):
        user = request.user_details
        agent_id = user.id
        orders = OrderModal.objects.filter(status='delivered', order_delivery__agent_id=agent_id) 
        data = []
        for order in orders:
            temp = model_to_dict(order)
            temp['order_id'] = order.id
            temp['created_at'] = order.created_at
            temp['updated_at'] = order.updated_at
            temp['sender_id'] = model_to_dict(order.sender_id)
            temp['receiver_id'] = model_to_dict(order.receiver_id)
            temp['sender_id']['location_id'] = model_to_dict(order.sender_id.location_id)
            temp['receiver_id']['location_id'] = model_to_dict(order.receiver_id.location_id)
            data.append(temp)
        print(data)
        return Response({"orders":data, "status":"success"}, status=status.HTTP_200_OK)
    
    
       
    def receive_agent_feedback(self, request):
        user = request.user_details
        agent_id = user.id
        order_id = request.data.get('order_id', '')
        delivery_id = request.data.get('delivery_id', '')
        comment = request.data.get('comment', '')
        rating = request.data.get('rating', '') # no rating  equates to 0
    
        if(delivery_id and rating != ''):
            try:
                order= OrderModal.objects.get(id=order_id)
            except:
                print('invalid order id')
                Response({"msg":'Invalid delivery id'}, status=status.HTTP_400_BAD_REQUEST)
            delivered_serializer = OrderModalSerializer(order,data={
                
                "status":"delivered"
            }, partial=True)
            if delivered_serializer.is_valid():
                delivered_serializer.save()
            else:
                print(delivered_serializer.errors)
                return Response({"msg":delivered_serializer.errors, "status":"failed"}, status=status.HTTP_400_BAD_REQUEST)
            #payment
            #fetch payment details of delivery
            delivery= OrderDeliveryModal.objects.get(agent_id=agent_id, id=delivery_id)
            agent_payment = AgentPaymentModal.objects.filter(agent_id=user).first()
            if(agent_payment):
                agent_payment.amount = agent_payment.amount + delivery.order_id.fee 
                agent_payment.fee= agent_payment.fee + delivery.order_id.companyFee
                agent_payment.save()
            else:
                AgentPaymentModal.objects.create(agent_id=user, amount=delivery.order_id.fee, fee=delivery.order_id.companyFee).save()
            return Response({"status":"success"}, status=status.HTTP_201_CREATED)
            
            
        
            # serializer = FeedbackModalSerializer(data={
            #     "delivery_id":delivery_id,
            #     "user_id":agent_id,
            #     "comment":comment,
            #     "rating":rating
            # })
            # if serializer.is_valid():
            #     serializer.save()
            #     return Response({"status":"success"}, status=status.HTTP_201_CREATED)
            # return Response({"msg":"Invalid request", "status":"failed"}, status=status.HTTP_400_BAD_REQUEST)
          
        return Response({"msg":"Please provide delivery id and feedback!"}, status=status.HTTP_400_BAD_REQUEST)
                
                
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


