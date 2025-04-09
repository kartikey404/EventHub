## Register View to Redirect by Role
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from events.forms import CustomUserCreationForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.userprofile.user_type = form.cleaned_data['user_type']
            user.userprofile.save()
            login(request, user)

            # Redirect by role
            role = user.userprofile.user_type
            if role == 'artist':
                return redirect('artist_dashboard')
            elif role == 'manager':
                return redirect('manager_dashboard')
            else:
                return redirect('guest_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def role_redirect(request):
    print("Redirecting...")
    role = request.user.userprofile.user_type
    if role == 'artist':
        return redirect('artist_dashboard')
    elif role == 'manager':
        return redirect('manager_dashboard')
    else:
        return redirect('guest_dashboard')
