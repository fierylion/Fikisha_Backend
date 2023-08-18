from django.urls import path
from .views import ClientView, AgentView
app_urls = [
    path('register/customer', ClientView.as_view(
        {
            'post': 'create_single_user'
        }
    )),
    path(
        'login/customer', ClientView.as_view(
            {
                'post': 'login_single_user'
            }
        )
    ),
    path(
        'customer', ClientView.as_view(
            {
                'get':'get_details'
            }
        )
    ),
    path(
        'customer/order', ClientView.as_view(
            {
                'post':'create_order',
                'get':'get_orders'
            }
        )
    ),
    
    #Agent
    path('register/agent', AgentView.as_view(
        {
            'post': 'create_single_user'
        }
    )),
    path(
        'login/agent', AgentView.as_view(
            {
                'post': 'login_single_user'
            }
        )
    ),
     path(
        'agent', AgentView.as_view(
            {
                'get':'get_details'
            }
        )
    ),

    path(
        'agent/orders', AgentView.as_view(
            {
                'get':'get_orders'
            }
        )
    ),

    
]