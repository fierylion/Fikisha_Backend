from django.urls import path
from .views import UserView, PaymentOperationView
app_urls = [
    path('register', UserView.as_view(
        {
            'post': 'create_single_user'
        }
    )),
    path(
        'login', UserView.as_view(
            {
                'post': 'login_single_user'
            }
        )
    ),
    path('user/details', UserView.as_view(
        {
            'post': 'save_details'
        }
    )),
    path('user/info', UserView.as_view(
        {
            'get': 'get_info'
        }
    )),
    path('user/send_email', UserView.as_view(
        {
            'post': 'send_email'
        }
    )),
    path('user/payment/generate', PaymentOperationView.as_view(
        {
            'post': 'create_payment_link'
        }
    )
    ),
    path('user/payment/callback', PaymentOperationView.as_view(
        {
            'post': 'receive_callback'
        }
    )),
    
]