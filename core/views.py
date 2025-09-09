from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.db.models import Count, Avg
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from gateway.models import APIKey, RequestLog

def interface_view(request):
    return render(request, "pages/interface.html")

def documentation_view(request):
    return render(request, "pages/docs.html")

@login_required(login_url='')
def dashboard_view(request):
    user_keys = APIKey.objects.filter(owned_by=request.user)
    user_logs = RequestLog.objects.filter(key__in=user_keys).order_by('-timestamp')
    key_stats = user_keys.annotate(request_count=Count('requestlog'))
    avg_duration = user_logs.aggregate(avg=Avg('duration'))['avg']
    successful_requests = user_logs.filter(status_code__lt=300).count()
    blocked_requests = user_logs.filter(status_code__gte=400).count()
    total_requests = user_logs.count()

    return render(request, 'pages/dashboard.html', {
        'user_keys': user_keys,             # raw key objects
        'user_logs': user_logs,             # full request logs
        'key_stats': key_stats,             # request counts per key
        'avg_duration': avg_duration,       # average duration across logs
        'total_requests': total_requests,   # total number of requests
        'successful_requests': successful_requests, # successfull requests
        'blocked_requests': blocked_requests, # blocked requests
    })

def register_view(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already registered and logged in.")
        return redirect('interface')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, "Account created successfully!"
            )
            return redirect('login')
        else:
            messages.error(
                request, "There was an error with your registeration"
            )
    else:
        form = CustomUserCreationForm()

    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('interface')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.warning(
                request, 'Please enter both username and password.')
            return render(request, 'auth/login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('interface-page')
            else:
                messages.warning(
                    request, 'Your account is inactive. Please contact support.')
        else:
            messages.error(request, 'Invalid username or password.')

    else:
        if request.user.is_authenticated:
            messages.info(request, 'You are already logged in.')
            return redirect('interface-page')

    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    return redirect('interface-page')