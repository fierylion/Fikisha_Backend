from django.db import models
import uuid
# Create your models here.
class CustomUser(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email=models.EmailField(unique=True,blank=False,null=False, error_messages={
        'unique':"Email already exists, Please enter another one!",
        "blank":"Email field can\'t be blank"
    })
    password=models.CharField(max_length=400, null=False, blank=False)
    phone = models.CharField(max_length=20, null=False, blank=False, error_messages={
        "blank":"Phone field can\'t be blank",
        "null":"Phone field can\'t be null"
        })
    category = models.CharField(max_length=400, null=False, blank=False, choices=( ("client", "client"), ("agent", "agent") ), error_messages={
        "blank":"Category field can\'t be blank",
        "null":"Category field can\'t be null",
        "choices":"Category field can only be client or agent"
        })
    created_at=models.DateTimeField(auto_now_add=True)
#q: I am creating modals for a package delivery system

class ProductRegistrationModal(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client_id=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category=models.CharField(max_length=400, null=False, blank=False)
    senderName=models.CharField(max_length=400, null=False, blank=False)
    senderPhone=models.CharField(max_length=400, null=False, blank=False)
    receiverName=models.CharField(max_length=400, null=False, blank=False)
    receiverPhone=models.CharField(max_length=400, null=False, blank=False)
    senderLocation=models.TextField(null=False, blank=False)
    receiverLocation=models.TextField(null=False, blank=False)
    deliveryTime = models.CharField(max_length=400, null=False, blank=False)
    payer=models.CharField(max_length=400, null=False, blank=False)
    mode = models.CharField(max_length=400, null=False, blank=False)
    amount=models.CharField(null=False, blank=False, max_length=20)
    created_at=models.DateTimeField(auto_now_add=True)
    

class TransportRequestModal(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product=models.OneToOneField(ProductRegistrationModal, on_delete=models.CASCADE)
    
    agent=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="agent")
    status=models.CharField(max_length=400, null=False, blank=False, choices=( ("pending", "pending"),  ("delivered", "delivered") ), error_messages={
        "blank":"Status field can\'t be blank",
        "null":"Status field can\'t be null",
        "choices":"Status field can only be pending, accepted, rejected or delivered"
        })
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class TrackDeliveryModal(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transport_request=models.ForeignKey(TransportRequestModal, on_delete=models.CASCADE)
    location=models.TextField(null=False, blank=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class FeedbackModal(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transport_request=models.ForeignKey(TransportRequestModal, on_delete=models.CASCADE)
    rating=models.IntegerField(null=False, blank=False)
    comment=models.TextField(null=False, blank=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)