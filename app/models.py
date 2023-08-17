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
    reference=models.CharField(max_length=400, null=True, blank=True)
    paid=models.BooleanField()

"""
q: for transaction models should have those fieldsamount
required
string
This is amount that will be charged from the given account.

currencyCode
required
string
Code of currency

merchantAccountNumber
required
string
This is the account number/MSISDN that consumer will provide. The amount will be deducted from this account.

merchantMobileNumber
required
string
Mobile number

merchantName
string or null
The name of consumer

otp
required
string
One time password

provider
required
string (BankProvider)
Enum: "CRDB" "NMB"
referenceId
string or null
This id belongs to the calling application. Maximum Allowed length for this field is 128 ascii characters
"""
#  {'message': 'SUCCESS', 'user': None, 'password': None, 'clientId': None, 'transactionstatus': 'success', 'operator': 'Halopesa', 'reference': 'b6aa2edd7fa34731938fa1deadb4e8b2', 'externalreference': 'b6aa2edd7fa34731938fa1deadb4e8b2', 'utilityref': '1234', 'amount': '1000', 'transid': 'b6aa2edd7fa34731938fa1deadb4e8b2', 'msisdn': '0628630936', 'mnoreference': 'c6cef289-e49e-45b2-807d-30d2aa1eae08', 'submerchantAcc': None, 'additionalProperties': {}}
# message, user, password, clientId, submerchantAcc, additionalProperties
class UserData(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name=models.CharField(max_length=128)
    surname=models.CharField(max_length=128)
    email=models.EmailField(blank=False,null=False, unique=True, error_messages={
        'unique':"Email already exists, Please enter another one!",
        "blank":"Email field can\'t be blank"
        })
    phone_number=models.CharField(max_length=20)
    college_name=models.CharField(max_length=128)
    course_name=models.CharField(max_length=128)
    date_of_birth=models.DateField()
    membership_no=models.CharField(max_length=128)
    gender=models.CharField(max_length=128)

class Transaction(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    transactionstatus=models.CharField(max_length=20)
    operator=models.CharField(max_length=20)
    reference=models.CharField(max_length=128)
    externalreference=models.CharField(max_length=128)
    utilityref=models.CharField(max_length=128)
    amount=models.FloatField()
    transid=models.CharField(max_length=128)
    msisdn=models.CharField(max_length=20)
    mnoreference=models.CharField(max_length=128)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


class TransactionRecords(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    transactionstatus=models.CharField(max_length=20)
    operator=models.CharField(max_length=20)
    reference=models.CharField(max_length=128)
    externalreference=models.CharField(max_length=128)
    utilityref=models.CharField(max_length=128)
    amount=models.FloatField()
    transid=models.CharField(max_length=128)
    msisdn=models.CharField(max_length=20)
    mnoreference=models.CharField(max_length=128)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

