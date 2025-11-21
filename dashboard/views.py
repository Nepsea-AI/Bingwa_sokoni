from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.core.paginator import Paginator
from dashboard.models import Transaction, Token
from django.db.models import Q
import datetime
from dashboard.forms import SignUpForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from settings.models import UserProfile
import json, uuid

# Create your views here.
def dashboard(request):
    total_received = Transaction.objects.count()
    total_completed = Transaction.objects.filter(status='completed').count()
    total_pending = Transaction.objects.filter(status='pending').count()
    total_failed = Transaction.objects.filter(status='failed').count()

    # Airtime balance placeholder (later fetched from DB)
    airtime_balance = None  # means it’ll show “****” in the template


    return render(request, 'dashboard.html', {'total_received': total_received,'total_completed': total_completed,'total_pending': total_pending,'total_failed': total_failed, 'airtime_balance': airtime_balance})




def airtime(request):
    balance = 0  # default balance
    return render(request, 'airtime.html', {'balance': balance})


def commission(request):
    return render(request, 'commission.html', {})



def failed_transactions(request):
    #get the failed transaction
    failed_list = Transaction.objects.filter(status='failed').order_by('-created_at')
    #grab date and time
    now = datetime.datetime.now()

    #inserting the insensitive search bar functionality
    query = request.GET.get('q')
    if query:
        failed = failed.filter(
            Q(phone_number__icontains=query) |
            Q(customer_name__icontains=query) |
            Q(transaction_id__icontains=query)
        )

    #adding pagination
    paginator = Paginator(failed_list, 10)
    page = request.GET.get('page')
    transactions = paginator.get_page(page)
    return render(request, 'failed_transactions.html', {'transactions': transactions ,'query': query})

def completed_transactions(request):
    #get the completed transactions
    completed = Transaction.objects.filter(status='completed').order_by('-created_at')
    #grab date and time
    now = datetime.datetime.now()

    #inserting the insensitive search bar functionality
    query = request.GET.get('q')
    if query:
        completed = completed.filter(
            Q(phone_number__icontains=query) |
            Q(customer_name__icontains=query) |
            Q(transaction_id__icontains=query)
        )

    #adding pagination
    paginator = Paginator(completed, 10)
    page = request.GET.get('page')
    transactions = paginator.get_page(page)
    return render(request, 'completed_transactions.html', {'transactions': transactions, 'query': query,})

def pending_transactions(request):
    #get the pending transactions
    pending = Transaction.objects.filter(status='pending').order_by('-created_at')
    #grab date and time
    now = datetime.datetime.now()

    #inserting the insensitive search bar functionality
    query = request.GET.get('q')
    if query:
        pending = pending.filter(
            Q(phone_number__icontains=query) |
            Q(customer_name__icontains=query) |
            Q(transaction_id__icontains=query)
        )

    #adding pagination
    paginator = Paginator(pending, 10)
    page = request.GET.get('page')
    transactions = paginator.get_page(page)
    return render(request, 'pending_transactions.html', {'transactions': transactions ,'query': query})

#The below token view, helps us when we click the token card, it redirects us to tokens.html...it makes that page visible for us users
def tokens(request):
    token_list = Token.objects.all()
    print("Loaded Tokens:", token_list)  # optional debug check
    return render(request, 'tokens.html', {'tokens': token_list})

#This process token view, it makes the functionalities in token.html page work...it works silently in the background, if not for it, token view page won't work as expected
@csrf_exempt
@login_required
def process_token_purchase(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            product = data.get("product")
            price = data.get("price")
            number = data.get("number")

            if not number.startswith("07"):
                return JsonResponse({"status": "error", "message": "Only Safaricom numbers are supported."})

            # Get or create user profile
            profile, _ = UserProfile.objects.get_or_create(user=request.user)

            # If the user’s SIM number != paying number, require a separate token purchase
            if profile.sim_number and profile.sim_number != number:
                return JsonResponse({
                    "status": "error",
                    "message": f"This account is already linked to {profile.sim_number}. "
                               f"You must purchase new tokens for {number} to use services."
                })

            # Generate new device token per number (anti-bypass). After and before purchase, the following information down below is considered by the DB so as to avoid anti-bypass to another number that hasn't purchased the tokens

            device_id = str(uuid.uuid4())
            profile.sim_number = number
            profile.device_id = device_id
            profile.save()

            # Here, integrate M-Pesa STK push logic
            return JsonResponse({
                "status": "success",
                "message": f"Purchase confirmed for {number}. Ksh {price} will be charged.",
                "device_id": device_id
            })

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request."})

def logout_view(request):
    logout(request)  # Fix: Use lowercase 'logout'
    messages.success(request, "You have successfully logged out!")
    return redirect('dashboard')

def transaction_detail(request, pk):
    tx = get_object_or_404(Transaction, pk=pk)
    origin = request.GET.get('from', '')  # default to blank if not set
    return render(request, 'transaction_detail.html', {'tx': tx , 'origin': origin})


def received_transactions(request):
    #get all transactions
    all_transactions = Transaction.objects.all().order_by('-created_at')
    #grab date and time
    now = datetime.datetime.now()

    #inserting the insensitive search bar functionality
    query = request.GET.get('q')
    if query:
        all_transactions = all_transactions.filter(
            Q(phone_number__icontains=query) |
            Q(customer_name__icontains=query) |
            \
            Q(transaction_id__icontains=query)
        )

    #adding pagination
    paginator = Paginator(all_transactions, 10)
    page = request.GET.get('page')
    transactions = paginator.get_page(page)
    return render(request, 'received_transactions.html', {'transactions': transactions, 'query': query})

def login_view(request):
    return redirect('social:begin', backend='google-oauth2')

def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def register_view(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # login the user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Username Created, please fill out your User Info Below...")
            return redirect('custom_login')
        else:
            # ✅ Add this to see the real problem
            print(form.errors)  
            messages.error(request, f"There was a problem in registering: {form.errors}")
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})

def purchase_airtime(request):
    if request.method == 'POST':
        receiving_number = request.POST.get('receiving_number')
        amount = request.POST.get('amount')
        paying_number = request.POST.get('paying_number')

        # Later: Add logic to process payment
        messages.success(request, f"Airtime of Ksh {amount} sent to {receiving_number} successfully!")
        return redirect('airtime')