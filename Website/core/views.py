from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from .models import otherDetails
from django.contrib.auth import authenticate, login, logout
from .forms import img
from django.contrib import messages
import numpy as np
from django.conf import settings
import pandas as pd
from saved_model import finalized_model.sav
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import CreateUserForm

import pathlib
PATH_TO_TEST_IMAGES_DIR = pathlib.Path('C:\\Users\\windows\\Desktop\\hackathon\\SPIT_HACKATHON\\Github\\Demand-Forecasting\\Website\\media\\imagesrec\\images')
TEST_IMAGE_PATHS = sorted(list(PATH_TO_TEST_IMAGES_DIR.glob("*.jpg")))
media_url = settings.MEDIA_URL

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('login')
    else:
        print(request.method)
        if request.method == 'POST':
            if 'login' in request.POST:
                username = request.POST.get('username')
                password = request.POST.get('password')

                user = authenticate(request, username=username, password=password)

                if user is not None:
                    login(request, user)
                    
                    return redirect('bulk')
                else:
                    messages.info(request, 'Username OR password is incorrect')
            elif 'register' in request.POST:
                if request.user.is_authenticated:
                    return redirect('login')
                else:
                    form = CreateUserForm()
                    if request.method == 'POST':
                        username = request.POST.get('username')
                        password = request.POST.get('password')
                        prodName = request.POST.get('prodName')
                        
                        user = User.objects.create_user(username=username, password=password)
                        # user.userprofile.user = authenticate(username=username, password=password)
                        user.save()
                        user = authenticate(username=username, password=password)
                        
                        profile = Profile()
                        profile.user = user
                        profile.prodName = prodName
                        profile.save()

                        login(request, user)
                        messages.success(request, 'Account was created')
                        print("Account was created")


                        return redirect('bulk')

        return render(request, 'index.html')
            
def logoutUser(request):
	logout(request)
	return redirect('login')

def bulk(request):
    if request.method == "POST":
        my_file = request.FILES.get("file")
        otherDetails.objects.create(image = my_file)
        return redirect("/bulk")
    else:
        form = img()
        return render(request, 'bulk.html')

def main(request):
    #global PATH_TO_LABELS
    global TEST_IMAGE_PATHS  
    global media_url
    filename="finalized_model.sav"
    loaded_model = pickle.load(open(filename, 'rb'))
    if request.method == "POST":
        print("helsslo")
        for file in TEST_IMAGE_PATHS:
            df=pd.read_csv(file)
            df=df.drop(['index'],axis=1)
            df["diagnosis"] = np.nan
            row_len=len(df)
            df_x=df.drop(['diagnosis'],axis=1)
            for row in range(0,row_len):
                row_vector = df_x.iloc(row)
                X_test=row_vector.to_numpy().reshape(1,-1)
                value=""
                if len(X_test)!=30:
                    df.iloc[row]['diagnosis']= "error"
                else:
                    Y_pred = loaded_model.predict(X_test)
                    if Y_pred==1:
                        value="Malignant"
                    else:
                        value="Benign"
                    df.iloc[row]['diagnosis']= value
            df.close()
    result_dic = {'zzz.jpg':[{'hide_and_seek': 16.828192794320884, 'oreo': 15.088242364541538, 'bourbon': 5.835317175046396},{'hide_and_seek': ['left', 'bottom'], 'oreo': ['middle', 'top'], 'bourbon': ['middle', 'bottom']}],'4.jpg':[{'hide_and_seek': 16.828192794320884, 'oreo': 15.088242364541538, 'bourbon': 5.835317175046396},{'hide_and_seek': ['left', 'bottom'], 'oreo': ['middle', 'top'], 'bourbon': ['middle', 'bottom']}]}

    return render(request, 'result.html',{'result_dic':result_dic})