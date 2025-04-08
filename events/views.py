from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .models import UserProfile

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.userprofile.user_type = form.cleaned_data['user_type']
            user.userprofile.save()
            login(request, user)  # Optional: log them in immediately
            return redirect('dashboard')  # Redirect to their dashboard later
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard(request):
    profile = request.user.userprofile
    return render(request, 'events/dashboard.html', {
        'profile': profile
    })
