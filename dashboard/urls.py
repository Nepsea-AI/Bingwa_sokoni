from django.urls import path
from dashboard.views import dashboard,airtime,commission,completed_transactions,failed_transactions, pending_transactions, tokens, logout_view, transaction_detail, received_transactions, login_view,custom_login_view, register_view, purchase_airtime, process_token_purchase

urlpatterns = [
    path('', dashboard, name='dashboard'),
    
    path('tokens/', tokens, name='tokens'),
    path('tokens/purchase/', process_token_purchase, name='process_token_purchase'),

    path('airtime/', airtime, name='airtime'),
    path('airtime/purchase/', purchase_airtime, name='purchase_airtime'),

    path('commission/', commission, name='commission'),

    path('transactions/completed/', completed_transactions, name='completed_transactions'),
    path('transactions/pending/', pending_transactions, name='pending_transactions'),
     path('transactions/failed/', failed_transactions, name='failed_transactions'),
    path('transactions/<int:pk>/', transaction_detail, name='transaction_detail'),
     path('transactions/received/', received_transactions, name='received_transactions'),

    path('logout/', logout_view, name='logout'),

    path('login/google/', login_view, name='google_login'),  # optional, for clean redirect
    path('login/', custom_login_view, name='custom_login'),  # if you're building your own form'

    path('register/', register_view, name='register'),
    
    
]
#URL Patterns Explained: urls patterns clusted together as a pair, means they work together...and the top of them all is the center, without it, the others don't matter
