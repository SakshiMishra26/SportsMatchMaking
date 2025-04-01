from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from django.core.mail import send_mail
import random
from .forms import CustomUserCreationForm  # Import the custom form
from django.contrib import messages  # Import messages

# def send_otp(request):
#     """ Handles OTP sending and storing it in session """
#     if request.method == 'POST':
#         email = request.POST.get('email')
        
#         if User.objects.filter(email=email).exists():
#             messages.error(request, "Email is already registered.")
#             return redirect('register')

#         otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
#         request.session['otp'] = str(otp)  # Store OTP in session as string
#         request.session['email'] = email  # Store email in session

#         send_mail(
#             'Your OTP for Registration',
#             f'Your OTP is {otp}. Please enter it to complete registration.',
#             'your-email@gmail.com',  # Replace with your email
#             [email],  # Receiver email
#             fail_silently=False,
#         )
#         messages.success(request, "OTP sent to your email!")
#         return render(request, 'registration.html', {'otp_sent': True, 'email': email})
#     return redirect('register')

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    
    # Ensure the UserProfile exists
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        profile.location = request.POST.get('location', profile.location)
        profile.sports = request.POST.get('sports', profile.sports)
        profile.skill_level = request.POST.get('skill_level', profile.skill_level)
        
        if 'profile_picture' in request.FILES:
            if profile.profile_picture:
                profile.profile_picture.delete(save=False)  # Delete old image before saving new one
            profile.profile_picture = request.FILES['profile_picture']
        
        profile.save()
        return redirect('profile', username=request.user.username)

    return render(request, 'profile.html', {'profile': profile, 'user': user})



@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        profile.location = request.POST.get('location', profile.location)
        profile.sports = request.POST.get('sports', profile.sports)
        profile.skill_level = request.POST.get('skill_level', profile.skill_level)

        if 'profile_picture' in request.FILES:
            if profile.profile_picture:
                profile.profile_picture.delete(save=False)  # ✅ Delete old image to prevent storage issues
            profile.profile_picture = request.FILES['profile_picture']

        profile.save()
        return redirect('profile', username=request.user.username)

    return render(request, 'profile.html', {'profile': profile})



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Use CustomUserCreationForm
        if form.is_valid():
            user = form.save()
            login(request, user)  
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('index')
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = CustomUserCreationForm()
        print('User not created')    
    return render(request, 'registration.html', {'form': form})

# def register(request):
#     if request.method == 'POST':
#         if 'send_otp' in request.POST:  # When user clicks "Send OTP"
#             email = request.POST.get('email')
            
#             if User.objects.filter(email=email).exists():
#                 messages.error(request, "Email is already registered.")
#                 return redirect('register')

#             otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
#             request.session['otp'] = str(otp)  # Store OTP in session
#             request.session['email'] = email  # Store email in session

#             send_mail(
#                 'Your OTP for Registration',
#                 f'Your OTP is {otp}. Please enter it to complete registration.',
#                 'your-email@gmail.com',  # Replace with your email
#                 [email],  # Receiver email
#                 fail_silently=False,
#             )
#             messages.success(request, "OTP sent to your email!")
#             return render(request, 'registration.html', {'otp_sent': True, 'email': email})

#         else:  # When user submits the registration form
#             entered_otp = request.POST.get('otp')
#             stored_otp = request.session.get('otp')
#             email = request.session.get('email')

#             if not stored_otp or entered_otp != stored_otp:
#                 messages.error(request, "Invalid OTP. Please try again.")
#                 return redirect('register')

#             form = CustomUserCreationForm(request.POST)
#             if form.is_valid():
#                 user = form.save(commit=False)
#                 user.email = email  # Assign verified email
#                 user.save()
#                 login(request, user)
#                 messages.success(request, "Registration successful! You can now log in.")
#                 del request.session['otp']  # Clear OTP from session
#                 return redirect('index')
#             else:
#                 for field, error_list in form.errors.items():
#                     for error in error_list:
#                         messages.error(request, f"{field.capitalize()}: {error}")

#     else:
#         form = CustomUserCreationForm()
#         print('User not created')    

#     return render(request, 'registration.html', {'form': form})

# def register(request):
#     if request.method == 'POST':
#         if 'send_otp' in request.POST:  # When user clicks "Send OTP"
#             email = request.POST.get('email')
            
#             if User.objects.filter(email=email).exists():
#                 messages.error(request, "Email is already registered.")
#                 return redirect('register')

#             otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
#             request.session['otp'] = str(otp)  # Store OTP in session
#             request.session['email'] = email  # Store email in session

#             try:
#                 send_mail(
#                     'Your OTP for Registration',
#                     f'Your OTP is {otp}. Please enter it to complete registration.',
#                     'your-email@gmail.com',  # Replace with your email
#                     [email],  # Receiver email
#                     fail_silently=False,
#                 )
#                 messages.success(request, "OTP sent to your email!")
#                 return render(request, 'registration.html', {'otp_sent': True, 'email': email, 'form': CustomUserCreationForm()})
#             except Exception as e:
#                 messages.error(request, f"Failed to send OTP: {str(e)}")
#                 return redirect('register')

#         else:  # When user submits the registration form
#             entered_otp = request.POST.get('otp')
#             stored_otp = request.session.get('otp')
#             email = request.session.get('email')

#             if not stored_otp or entered_otp != stored_otp:
#                 messages.error(request, "Invalid OTP. Please try again.")
#                 return render(request, 'registration.html', {'otp_sent': True, 'email': email, 'form': CustomUserCreationForm()})

#             form = CustomUserCreationForm(request.POST)
#             if form.is_valid():
#                 user = form.save(commit=False)
#                 user.email = email  # Assign verified email
#                 user.save()
#                 # Create UserProfile
#                 UserProfile.objects.create(
#                     user=user,
#                     location=form.cleaned_data['location'],
#                     sports=form.cleaned_data['sports'],
#                     skill_level=form.cleaned_data['skill_level']
#                 )
#                 login(request, user)
#                 messages.success(request, "Registration successful! You are now logged in.")
#                 del request.session['otp']  # Clear OTP from session
#                 del request.session['email']  # Clear email from session
#                 return redirect('index')
#             else:
#                 for field, error_list in form.errors.items():
#                     for error in error_list:
#                         messages.error(request, f"{field.capitalize()}: {error}")
#                 return render(request, 'registration.html', {'otp_sent': True, 'email': email, 'form': form})

#     else:
#         form = CustomUserCreationForm()
    
#     return render(request, 'registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'registration.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('index')