from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate
from django.contrib import messages

def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, "Hey, your account was created successfully")
            
            # Corrected authentication using email as username
            new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            
            login(request, new_user)
            return redirect("core:index")
    else:
        print("The user cannot be registered")

    form = UserRegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'userauths/sign-up.html', context)
