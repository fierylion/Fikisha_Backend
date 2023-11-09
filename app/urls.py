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
               
            }
        )
    ),
    path(
        'customer/order/cancel/<str:order_id>', ClientView.as_view(
            {
                'get':'cancel_order',
               
            }
        )
    ),
    path(
        'customer/order/feedback', ClientView.as_view(
            {   
                'post':'receive_customer_feedback'
            }
        )
    ),
    path(
     'customer/orders/<str:state>', ClientView.as_view(
        {
            'get':'getAllOrders'
            }
    )),
    path(
     'customer/location', ClientView.as_view(
        {
            'post':'create_location'
            }
    )),
    path(
    'customer/location/<str:location_id>', ClientView.as_view(
        {
            'get':'get_single_location'
            }
    )
     
    ),
    path(
        'customer/locations/all', ClientView.as_view(
            {
                'get':'get_all_locations'
            }
        )
    ),

    
     path(
     'customer/order/<str:order_id>', ClientView.as_view(
        {
            'get':'getSingleOrder'
            }
    )),
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
     'agent/place_order/<str:order_id>', AgentView.as_view(
            {
                'post':'place_order'
            }
        )

     
    ),
    path('agent/order/pending', AgentView.as_view(
     {
      'get':'get_pending_order'
     }
    )),
    path(
        'agent/orders', AgentView.as_view(
            {
                'get':'get_orders'
            }
        )
    ),
    path(
        'agent/order/accept/<str:order_id>', AgentView.as_view(
            {
                'get':'accept_order',
               
            }
        )
    ),
    path('agent/transactions', AgentView.as_view(
     {
      'get':'get_payments'
     }
    )),
    path(
        'agent/order/deliver', AgentView.as_view(
            {
                'get':'get_accepted_orders',
            }
        )
    ),
    path('agent/orders/delivered', AgentView.as_view(
        {
        'get':'get_delivered_orders'
        }
    )),
    path(
     'agent/order/feedback', AgentView.as_view(
      {
         'post':'receive_agent_feedback'
      })
    ),

    
]