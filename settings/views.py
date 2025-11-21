from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json, uuid
from django.http import JsonResponse
from django.contrib.auth.models import User
from settings.models import UserProfile, Message
from dashboard.models import Transaction
from django.contrib import messages
from django.db.models import Q  # ✅ Import Q for flexible, case-insensitive search

# Create your views here.
def settings(request):
    
    return render(request, 'settings.html', {})


#The below user_id_page view, helps us when we click the user ID card, it redirects us to USER_ID.html...it makes that page visible for us users
def user_id_page(request):
    """Render the page with the SIM change modal"""
    return render(request, 'user_ID.html', {})

#This change user_id view, it makes the functionalities in user_id.html page work...it works silently in the background, if not for it, user_id view page won't work as expected
@csrf_exempt
def change_user_id(request):
    """Handle AJAX POST to update the SIM number and device ID"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            sim_number = data.get("sim_number")
            sim_type = data.get("sim_type")

            if not sim_number or not sim_type:
                return JsonResponse({"status": "error", "message": "Missing fields"})

            # Validate Safaricom number
            if not sim_number.startswith("07"):
                return JsonResponse({
                    "status": "error",
                    "message": "Failed to fetch your phone number. Not a Safaricom line."
                })

            # Generate new unique Device ID
            device_id = str(uuid.uuid4())
            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            profile.sim_number = sim_number
            profile.device_id = device_id
            profile.sim_type = sim_type
            profile.save()

            return JsonResponse({
                "status": "success",
                "message": f"Your User ID is set to: {sim_number}",
                "device_id": device_id
            })
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request"})

    #| Path               | Purpose              | Returns               | Triggered When                        |
# ------------------ | -------------------- | --------------------- | ------------------------------------- |
# `/user-id/`        | Shows modal UI       | HTML (`user_ID.html`) | When you click “User ID”              |
#| `/change-user-id/` | Processes SIM change | JSON                  | When you click “Confirm” in the modal |
#🌀 AJAX (Asynchronous JavaScript and XML)

#✅ Purpose:
#To send or receive data from the server without reloading the entire page.

#💡 In your project:
#When the user clicks “Confirm” in the modal, the JavaScript code sends the entered SIM info (sim_number, sim_type) to Django behind the scenes — instead of submitting a form and refreshing the page.

#👉 So the modal updates the User ID & Device ID instantly without a full page reload.

#📦 JSON (JavaScript Object Notation)

#✅ Purpose:
#A lightweight data format used to exchange information between the frontend (JavaScript) and backend (Django).

#💡 In your project:
#The JS side sends the SIM data as JSON:

#body: JSON.stringify({ sim_number: simNumber, sim_type: simType })


#And Django also responds with JSON:

#return JsonResponse({"status": "success", "message": "...", "device_id": device_id})


#So the browser and Django “talk” using JSON objects — simple and fast.

#⚙️ JsonResponse (Django shortcut)

#✅ Purpose:
#A Django helper that converts Python dictionaries into JSON HTTP responses.

#💡 In your project:
#You use:

#return JsonResponse({"status": "success", "message": "User ID updated"})


#instead of manually serializing data with json.dumps().

#It automatically sets the correct headers and formats the response, so your JS can easily read it.

#🧬 uuid (Universally Unique Identifier)

#✅ Purpose:
#To generate unique IDs that are practically impossible to duplicate.

#💡 In your project:
#You use:

#device_id = str(uuid.uuid4())


#to generate a unique device identifier each time a SIM is changed.
#That ensures no two devices share the same ID, even if they have similar SIM numbers.



def inbox(request):
    query = request.GET.get('q', '')  # Get search text from ?q= in the URL
    senders = {}

    # Base queryset: all messages for the logged-in user
    all_messages = Message.objects.filter(owner=request.user)

    # ✅ Apply search filter if a query is entered
    if query:
        all_messages = all_messages.filter(
            Q(sender__icontains=query) |  # search sender (e.g. name, number)
            Q(body__icontains=query)      # search message text
        )

    # ✅ Group by sender: keep only the latest message from each sender
    for msg in all_messages.order_by('-timestamp'):
        if msg.sender not in senders:
            senders[msg.sender] = msg

    return render(request, 'messages_inbox.html', {
        'threads': senders.values(),
        'query': query,
    })


def conversation(request, sender):
    messages = Message.objects.filter(owner=request.user, sender=sender).order_by('timestamp')
    Message.objects.filter(owner=request.user, sender=sender, is_read=False).update(is_read=True)
    return render(request, 'conversation.html', {'messages': messages, 'sender': sender})


@csrf_exempt
def delete_message(request):
    if request.method == "POST":
        data = json.loads(request.body)
        msg_id = data.get("id")
        try:
            msg = Message.objects.get(id=msg_id, owner=request.user)
            msg.delete()
            return JsonResponse({"status": "success"})
        except Message.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Message not found"})
    return JsonResponse({"status": "error", "message": "Invalid request"})

@csrf_exempt
def send_reply(request):
    if request.method == "POST":
        data = json.loads(request.body)
        sender = data.get("sender")
        text = data.get("message")

        if not sender or not text:
            return JsonResponse({"status": "error", "message": "Missing fields"})

        Message.objects.create(
            owner=request.user,
            sender=sender,
            body=text,
            sent_by_user=True,
            is_read=True
        )
        return JsonResponse({"status": "success", "message": "Reply sent!"})

    return JsonResponse({"status": "error", "message": "Invalid request"})


def inbox_transactions(request):
    """Shows category cards (e.g. MPESA, others)"""
    return render(request, 'inbox_transactions.html')


def mpesa_conversation(request):
    """Shows all MPESA messages"""
    mpesa_messages = Message.objects.filter(
        Q(sender__iexact='MPESA'),
        owner=request.user
    ).order_by('-timestamp')

    query = request.GET.get('q', '')
    if query:
        mpesa_messages = mpesa_messages.filter(
            Q(body__icontains=query) | Q(sender__icontains=query)
        )

    return render(request, 'mpesa_conversation.html', {
        'messages': mpesa_messages,
        'query': query,
    })



    