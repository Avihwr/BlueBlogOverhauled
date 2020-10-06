from django.contrib.auth.decorators import user_passes_test
from .forms import RegisterForm
from django.shortcuts import render, redirect
from django.contrib import messages
from blog.models import Profile
from blog.models import Blog

# Help from TECH WITH TIM


# Create your views here.
@user_passes_test(lambda user: not user.username, login_url='/profile/', redirect_field_name=None)
def register(request):
    index1 = Blog.objects.all().order_by('-time')[0]
    if request.method == "POST":
        form = RegisterForm(request.POST or None)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            Profile.objects.create(user=new_user)
            messages.success(request, "Your BlueBlog Account Has Been Successfully Created, You Can Now Log In")
        else:
            messages.warning(request, "Account Creation Failed. Try Again or Contact Us")
            return redirect('/register/')

        return redirect("/login/")
    else:
        form = RegisterForm()

    return render(request, "register/register.html", {"form": form, 'index1': index1})
