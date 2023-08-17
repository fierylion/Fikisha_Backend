from django.contrib import admin
from .models import CustomUser, Transaction, TransactionRecords, UserData
admin.site.register(CustomUser)
admin.site.register(Transaction)
admin.site.register(TransactionRecords)
admin.site.register(UserData)
# Register your models here.
