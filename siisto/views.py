from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.utils import timezone
from .models import Cunto, Jimicsi, Routine90, Profile, WeightLog
from .forms import CuntoForm, JimicsiForm, WeightLogForm, ProfileForm

# 1. SIGN UP VIEW
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        cp = request.POST.get('confirm_password')
        
        if User.objects.filter(username=u).exists():
            messages.error(request, 'Username already exists.')
            return redirect('signup')
        if p != cp:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')
        
        user = User.objects.create_user(username=u, password=p)
        Profile.objects.create(user=user)  # U abuur Profile si toos ah
        login(request, user)
        messages.success(request, 'Account created successfully!')
        return redirect('home')
    return render(request, 'siisto/signup.html')

# 2. LOGIN VIEW
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    return render(request, 'siisto/login.html')

# 3. LOGOUT VIEW
def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('login')

# 4. HOME VIEW (WATA CALORIES-KA)
@login_required(login_url='login')
def home(request):
    latest_food = Cunto.objects.filter(user=request.user).order_by('-id').first()
    latest_workout = Jimicsi.objects.filter(user=request.user).order_by('-id').first()
    
    # Nidaamka Auto-ga ee 90 Days Challenge
    first_routine = Routine90.objects.filter(user=request.user).order_by('id').first()
    if first_routine:
        maanta = timezone.now().date()
        maalintii_hore = first_routine.created_at.date() if hasattr(first_routine, 'created_at') else maanta
        days_passed = (maanta - maalintii_hore).days + 1
        current_day = min(days_passed, 90)
    else:
        current_day = 0

    if request.method == 'POST':
        if 'cunto_submit' in request.POST:
            form = CuntoForm(request.POST)
            if form.is_valid():
                cunto = form.save(commit=False)
                cunto.user = request.user
                cunto.save()
                if not first_routine:
                    Routine90.objects.create(user=request.user, maalinta=1)
                messages.success(request, 'Meal logged successfully!')
                return redirect('home')
        
        elif 'jimicsi_submit' in request.POST:
            jimicsi_form = JimicsiForm(request.POST)
            if jimicsi_form.is_valid():
                jimicsi = jimicsi_form.save(commit=False)
                jimicsi.user = request.user
                jimicsi.save()
                if not first_routine:
                    Routine90.objects.create(user=request.user, maalinta=1)
                messages.success(request, 'Workout logged successfully!')
                return redirect('home')

    form = CuntoForm()
    jimicsi_form = JimicsiForm()

    context = {
        'cunto': latest_food,
        'jimicsi': latest_workout,
        'current_day': current_day,
        'form': form,
        'jimicsi_form': jimicsi_form,
    }
    return render(request, 'siisto/home.html', context)

# 5. HISTORY VIEW
@login_required(login_url='login')
def history_view(request):
    context = {
        'dhammaan_cuntooyinka': Cunto.objects.filter(user=request.user).order_by('-id'),
        'dhammaan_jimicsiyada': Jimicsi.objects.filter(user=request.user).order_by('-id'),
    }
    return render(request, 'siisto/history.html', context)

# 6. DELETE VIEWS
@login_required(login_url='login')
def tirtir_cunto(request, cunto_id):
    try:
        cunto = Cunto.objects.get(id=cunto_id, user=request.user)
        cunto.delete()
        messages.warning(request, 'Meal log deleted.')
    except Cunto.DoesNotExist:
        pass
    return redirect('history')

@login_required(login_url='login')
def tirtir_jimicsi(request, jimicsi_id):
    try:
        jimicsi = Jimicsi.objects.get(id=jimicsi_id, user=request.user)
        jimicsi.delete()
        messages.warning(request, 'Workout log deleted.')
    except Jimicsi.DoesNotExist:
        pass
    return redirect('history')

# 7. PROGRESS VIEW
@login_required(login_url='login')
def progress_view(request):
    total_meals = Cunto.objects.filter(user=request.user).count()
    total_workouts = Jimicsi.objects.filter(user=request.user).count()
    
    last_week = timezone.now().date() - timedelta(days=7)
    meals_this_week = Cunto.objects.filter(user=request.user, taariikhda__gte=last_week).count()
    
    total_logs_this_week = meals_this_week + total_workouts
    target = 14
    
    if total_logs_this_week >= target:
        percentage = 100
    elif total_logs_this_week > 0:
        percentage = int((total_logs_this_week / target) * 100)
    else:
        percentage = 0

    context = {
        'total_meals': total_meals,
        'total_workouts': total_workouts,
        'percentage': percentage,
    }
    return render(request, 'siisto/progress.html', context)

# 8. PROFILE & WEIGHT TRACKER VIEW (Cusub!)
@login_required(login_url='login')
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    weight_logs = WeightLog.objects.filter(user=request.user).order_by('-taariikhda')
    
    if request.method == 'POST':
        if 'profile_submit' in request.POST:
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('profile_page')
        
        elif 'weight_submit' in request.POST:
            weight_form = WeightLogForm(request.POST)
            if weight_form.is_valid():
                weight_log = weight_form.save(commit=False)
                weight_log.user = request.user
                weight_log.save()
                
                # Sidoo kale u cusboonaysii miisaanka hadda ee profile-ka
                profile.miisaan_hadda = weight_log.miisaanka
                profile.save()
                
                messages.success(request, 'New weight logged!')
                return redirect('profile_page')

    p_form = ProfileForm(instance=profile)
    w_form = WeightLogForm()
    
    context = {
        'profile': profile,
        'weight_logs': weight_logs,
        'p_form': p_form,
        'w_form': w_form,
    }
    return render(request, 'siisto/profile.html', context)