from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cunto, Jimicsi, Profile, WeightLog

# 1. HOME VIEW
@login_required(login_url='login')
def home_view(request):
    cuntooyinka = Cunto.objects.filter(user=request.user).order_by('-id')[:5]
    jimicsiyada = Jimicsi.objects.filter(user=request.user).order_by('-id')[:5]
    
    context = {
        'cuntooyinka': cuntooyinka,
        'jimicsiyada': jimicsiyada,
    }
    return render(request, 'siisto/home.html', context)

# 2. HISTORY VIEW
@login_required(login_url='login')
def history(request):
    cuntooyinka = Cunto.objects.filter(user=request.user).order_by('-id')
    jimicsiyada = Jimicsi.objects.filter(user=request.user).order_by('-id')
    
    context = {
        'cuntooyinka': cuntooyinka,
        'jimicsiyada': jimicsiyada,
    }
    return render(request, 'siisto/history.html', context)

# 3. PROGRESS VIEW
@login_required(login_url='login')
def progress_view(request):
    total_meals = Cunto.objects.filter(user=request.user).count()
    total_workouts = Jimicsi.objects.filter(user=request.user).count()
    
    target = 14
    completed = total_meals + total_workouts
    percentage = min(int((completed / target) * 100), 100) if target > 0 else 0
    
    context = {
        'total_meals': total_meals,
        'total_workouts': total_workouts,
        'percentage': percentage,
    }
    return render(request, 'siisto/progress.html', context)

# 4. PROFILE VIEW
@login_required(login_url='login')
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST' and 'weight_submit' in request.POST:
        miisaanka_cusub = request.POST.get('miisaanka')
        if miisaanka_cusub:
            profile.miisaan_hadda = miisaanka_cusub
            profile.save()
            
            WeightLog.objects.create(user=request.user, miisaanka=miisaanka_cusub)
            messages.success(request, "Miisaankaaga si guul leh ayaa loo keydiyey!")
            return redirect('profile_page')
            
    weight_logs = WeightLog.objects.filter(user=request.user).order_by('-taariikhda')
    
    context = {
        'profile': profile,
        'weight_logs': weight_logs,
    }
    return render(request, 'siisto/profile.html', context)

# 5. SIGNUP VIEW
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        p_confirm = request.POST.get('password_confirm')
        
        if not u or not p:
            messages.error(request, "Fadlan buuxi dhamaan meelaha banaan.")
            return render(request, 'siisto/signup.html')
            
        if p != p_confirm:
            messages.error(request, "Labada password isuma dhigmaan!")
            return render(request, 'siisto/signup.html')
            
        if User.objects.filter(username=u).exists():
            messages.error(request, "Username-kan waa la qaatay, fadlan mid kale dooro.")
            return render(request, 'siisto/signup.html')
            
        try:
            user = User.objects.create_user(username=u, password=p)
            login(request, user)
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Khalad ayaa dhacay: {str(e)}")
            return render(request, 'siisto/signup.html')
            
    return render(request, 'siisto/signup.html')

# 6. LOGIN VIEW
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username ama Password khaldan!")
            
    return render(request, 'siisto/login.html')

# 7. LOGOUT VIEW
def logout_view(request):
    logout(request)
    return redirect('login')