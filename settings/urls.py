from django.urls import path
from settings.views import settings, change_user_id, user_id_page, inbox, conversation, delete_message, send_reply, inbox_transactions, mpesa_conversation

urlpatterns = [
    path('', settings, name='settings'),

    path('change-user-id/', change_user_id, name='change_user_id'),  # AJAX endpoint
    path('user-id/', user_id_page, name='user_id_page'),  # The page with modal (change-user-id url connects with user-id url)

    path('inbox/', inbox, name='inbox'),
    path('inbox/<str:sender>/', conversation, name='conversation'),
    path('message/delete/', delete_message, name='delete_message'),
    path('message/reply/', send_reply, name='send_reply'),

    path('inbox/transactions/', inbox_transactions, name='inbox_transactions'),#inbox_transactions; exactly how you have named this, its exactly how you should name it in your views.py
    path('inbox/transactions/mpesa/', mpesa_conversation, name='mpesa_conversation'),


    


]
#URL Patterns Explained: urls patterns clusted together as a pair, means they work together...and the top of them all is the center, without it, the others don't matter