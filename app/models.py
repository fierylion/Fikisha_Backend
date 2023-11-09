from django.db import models
import uuid
# Create your models here.
class CustomUser(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    
    password=models.CharField(max_length=400, null=False, blank=False)
    name=models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)
    phone= models.CharField(max_length=15, null=False, blank=False, unique=True)
    
    profile_complete=models.BooleanField(default=False)
   
    category = models.CharField(max_length=400, null=False, blank=False, choices=( ("client", "client"), ("agent", "agent") ), error_messages={
        "blank":"Category field can\'t be blank",
        "null":"Category field can\'t be null",
        "choices":"Category field can only be client or agent"
        })
    created_at=models.DateTimeField(auto_now_add=True)
class AgentPaymentModal(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent_id=models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name='agent_payment')
    amount=models.FloatField(null=False, blank=False)
    fee=models.FloatField(null=False, blank=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
# class CustomUserExtra(models.Model):
#     first_name=models.CharField(max_length=40)
#     last_name = models.CharField(max_length=40)
#     phone= models.CharField(max_length=15)
#     user_id = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name="user_profile") 
    
#q: I am creating modals for a package delivery system
class OrderPartiesModal(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField(max_length=400, null=False, blank=False)
    phone=models.CharField(max_length=15, null=False, blank=False)
    location_id=models.ForeignKey("OrderLocationModal", on_delete=models.CASCADE)


class OrderLocationModal(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    geocode=models.CharField(max_length=400, null=False, blank=False)
    latitude=models.FloatField(null=False, blank=False)
    longitude=models.FloatField(null=False, blank=False)
    latitudeDelta=models.FloatField(null=False, blank=False)
    longitudeDelta=models.FloatField(null=False, blank=False)
    extra=models.TextField(null=True, blank=True)





class OrderModal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category=models.CharField(max_length=20, null=False, blank=False)
    fee=models.IntegerField()
    user_id=models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    
    
    payment_means=models.CharField(
        max_length=20, null=False, blank=False, choices=( ("instant", "instant"), ("sharing", "sharing") ), error_messages={
        "blank":"Payment means field can\'t be blank",
        "null":"Payment means field can\'t be null",
        "choices":"Payment means field can only be instant or sharing"
        })
    payment_method = models.CharField(max_length=20, null=False, blank=False, choices=( ("cash", "cash"), ("digital", "digital") ), error_messages={
        "blank":"Payment method field can\'t be blank",
        "null":"Payment method field can\'t be null",
        "choices":"Payment method field can only be cash or digital"
        })
    payment_by=models.CharField(
        max_length=20, null=False, blank=False, choices=( ("sender", "sender"), ("receiver", "receiver") ), error_messages={
        "blank":"Payment by field can\'t be blank",
        "null":"Payment by field can\'t be null",
        "choices":"Payment by field can only be sender or receiver"
        })
    sender_id=models.ForeignKey("OrderPartiesModal", on_delete=models.CASCADE, related_name="sender")
    receiver_id=models.ForeignKey("OrderPartiesModal", on_delete=models.CASCADE, related_name="receiver")
    status = models.CharField(
        max_length=20,
        default='pending',
        choices=(('pending', 'pending'), ('cancelled', 'cancelled'), ('accepted', 'accepted'),  ('delivered', 'delivered')),
        error_messages={
            "blank": "Status field can\'t be blank",
            "null": "Status field can\'t be null",
            "choices": "Status field can only be pending, accepted, rejected or delivered"
        },
    )
    companyFee= models.IntegerField()
    distance=models.CharField(max_length=20, null=False, blank=False)
    duration = models.CharField(max_length=20, null=False, blank=False)
    created_at=models.DateTimeField( auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class OrderDeliveryModal(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
   
    order_id=models.OneToOneField(
        "OrderModal", on_delete=models.CASCADE, related_name="order_delivery"
    )
    agent_id=models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    location=models.CharField(max_length=400, default='')
    status=models.CharField(max_length=20, null=False, blank=False, default='pending',choices=( ("pending", "pending"), ("delivered", "delivered") ), error_messages={
        "blank":"Status field can\'t be blank",
        "null":"Status field can\'t be null",
        "choices":"Status field can only be pending or delivered"
        })
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
class LocationModal(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id=models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    fkID=models.CharField(max_length=20, null=False, blank=False)
    name=models.CharField(max_length=80, null=False, blank=False)
    phone=models.CharField(max_length=15, null=False, blank=False)
    extra=models.TextField(null=True, blank=True)
    location=models.TextField(null=False, blank=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
class DeliveryFeeModal(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    delivery_id=models.OneToOneField("OrderDeliveryModal", on_delete=models.CASCADE)
    fee=models.FloatField(null=False, blank=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
class FeedbackModal(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    delivery_id=models.OneToOneField("OrderDeliveryModal", on_delete=models.CASCADE)
    user_id=models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    rating=models.FloatField(null=False, blank=False)
    comment=models.TextField(null=False, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)




    

# class ProductRegistrationModal(models.Model):
#     id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     client_id=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     category=models.CharField(max_length=400, null=False, blank=False)
#     senderName=models.CharField(max_length=400, null=False, blank=False)
#     senderPhone=models.CharField(max_length=400, null=False, blank=False)
#     receiverName=models.CharField(max_length=400, null=False, blank=False)
#     receiverPhone=models.CharField(max_length=400, null=False, blank=False)
#     senderLocation=models.TextField(null=False, blank=False)
#     receiverLocation=models.TextField(null=False, blank=False)
#     deliveryTime = models.CharField(max_length=400, null=False, blank=False)
#     payer=models.CharField(max_length=400, null=False, blank=False)
#     mode = models.CharField(max_length=400, null=False, blank=False)
#     amount=models.CharField(null=False, blank=False, max_length=20)
#     created_at=models.DateTimeField(auto_now_add=True)
    

# class TransportRequestModal(models.Model):
#     id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     product=models.OneToOneField(ProductRegistrationModal, on_delete=models.CASCADE)
    
#     agent=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="agent")
#     status=models.CharField(max_length=400, null=False, blank=False, choices=( ("pending", "pending"),  ("delivered", "delivered") ), error_messages={
#         "blank":"Status field can\'t be blank",
#         "null":"Status field can\'t be null",
#         "choices":"Status field can only be pending, accepted, rejected or delivered"
#         })
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)

# class TrackDeliveryModal(models.Model):
#     id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     transport_request=models.ForeignKey(TransportRequestModal, on_delete=models.CASCADE)
#     location=models.TextField(null=False, blank=False)
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)

# class FeedbackModal(models.Model):
#     id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     transport_request=models.ForeignKey(TransportRequestModal, on_delete=models.CASCADE)
#     rating=models.IntegerField(null=False, blank=False)
#     comment=models.TextField(null=False, blank=False)
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)