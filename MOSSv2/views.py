from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .forms import UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . import similarity

def index(request):
    return render(request, "MOSSv2/index.html", {"title": "Home"})


@login_required
def special(request):
    return HttpResponse("You are logged in!")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("moss:index"))

@login_required
def upload(request):
    return render(request, "MOSSv2/upload.html", {"title": "Upload"})


def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if "profile_pic" in request.FILES:
                print("found profile picture")
                profile.profile_pic = request.FILES["profile_pic"]
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(
        request,
        "MOSSv2/registration.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "registered": registered,
            "title": "Register",
        },
    )


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("moss:user_login"))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Invalid username: {} or password: {}".format(username, password))
            return render(request, "MOSSv2/login.html", {"username":username, 
            "password":password,
            "title": "Login",
            "error_msg" : "Invalid login details"})
    else:
        return render(request, "MOSSv2/login.html", {"title": "Login"})

@login_required
def upload_files(request):
    if request.method == "POST":
        file_list = [x.name for x in request.FILES.getlist('file')]
        files = request.FILES.getlist('file')
        print("{} files received.".format(len(file_list)))
        similarity_matrix = similarity.check_gensim_similarity(files)

    return render(request, "MOSSv2/upload.html", {"msg":"Files Uploaded",
    "title": "Upload",
    "file_list": file_list})