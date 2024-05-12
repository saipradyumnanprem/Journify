from . import apis, cloud
from .models import ImageEntry, JournalCounter
from django.http import HttpResponse
from . import apis
from . import cloud
from django.shortcuts import redirect, render
from .forms import SignupForm, UserCreationForm, loginForm, UserUpdateForm, UpdateProfileForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
import json
from .models import UserMoods, ImageEntry, JournalCounter
from .facialrecog import pred_emotion
from PIL import Image
import numpy as np
from django.templatetags.static import static


def home(request):
    return render(request, "Home/home.html")


def login_page(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("user_profile")
        else:
            return redirect("login_page")
    context = {}
    return render(request, "Home/login_page.html", context)


def signup_page(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            form.save()
            new_user = authenticate(username=username, password=password)
            new_user.save()
            if new_user is not None:
                login(request, new_user)
                return redirect("user_profile")
    else:
        form = SignupForm()
    context = {"form": form}
    return render(request, "Home/signup_page.html", context)


def logout_page(request):
    logout(request)
    return redirect("home")


@login_required
def details_page(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user, )
        p_form = UpdateProfileForm(request.POST,
                                   request.FILES,
                                   instance=request.user.userprofile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect("user_profile")

    else:

        u_form = UserUpdateForm(instance=request.user)
        p_form = UpdateProfileForm(instance=request.user.userprofile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, "Home/details.html", context)


def userprofile(request):

    data = list(cloud.get_data(
        username=request.user.username, user=request.user))

    # mood = request.user.usermoods.recent_mood
    # mood2 = request.user.usermoods.secondary_mood
    # image_mood = request.user.usermoods.image_mood

    mo = apis.ret_tips(request.user)

    context = {
        "data": json.dumps(data),
        "mood": mo
    }

    return render(request, 'Home/user_profile.html', context)


def journal_entry(request):
    if request.method == 'POST':
        journal_counter, created = JournalCounter.objects.get_or_create(
            user=request.user)

        temp_dict = {}
        temp_dict["journalId"] = journal_counter.journal_entry_count
        temp_dict["username"] = request.user.username
        temp_dict["journal_title"] = request.POST.get('journaltitle')
        temp_dict["content"] = request.POST.get('content')
        temp_dict["public"] = request.POST.get('public')
        temp_dict["mood"] = apis.classify(temp_dict["content"])

        if 'image_input' in request.FILES:
            img_file = request.FILES['image_input']
            img = Image.open(img_file)
            img_array = np.array(img)
            temp_dict["imageMood"] = pred_emotion(img_array)
            image_entry = ImageEntry(user=request.user, image=img_file)
            image_entry.journal_counter = journal_counter
            image_entry.username = request.user.username
            image_entry.save()

            UserMoods.objects.filter(user=request.user).update(
                recent_mood=temp_dict["mood"][0], secondary_mood=temp_dict["mood"][1], image_mood=temp_dict["imageMood"])

        UserMoods.objects.filter(user=request.user).update(
                recent_mood=temp_dict["mood"][0], secondary_mood=temp_dict["mood"][1], image_mood=temp_dict["imageMood"])

        cloud.add_entry(temp_dict)

        journal_counter.journal_entry_count += 1
        journal_counter.save()

        return redirect("user_profile")

    return render(request, 'Home/journal.html')


def get_journal_entries(request):

    context = {'data': list(cloud.get_data(
        username=request.user.username, user=request.user))}

    return render(request, 'Home/journalentries.html', context)


def get_public_journal_entries(request):

    context = {'data': list(cloud.get_public_data())}

    return render(request, 'Home/publicblog.html', context)


def profile(request):

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user, )
        p_form = UpdateProfileForm(request.POST,
                                   request.FILES,
                                   instance=request.user.userprofile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            return redirect("user_profile")

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UpdateProfileForm(instance=request.user.userprofile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, "Home/profile.html", context)
