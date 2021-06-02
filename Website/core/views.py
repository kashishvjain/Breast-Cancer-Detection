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
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import CreateUserForm
import pickle
from django.contrib.staticfiles.storage import staticfiles_storage
import os
import glob
import pathlib
import json
from django.contrib.auth.decorators import login_required
import shutil
import numpy
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext

#TEST_IMAGE_PATHS = sorted(list(PATH_TO_TEST_IMAGES_DIR.glob("*.jpg")))
media_url = settings.MEDIA_URL
static_url = settings.STATIC_URL

def delete():
    folders=['media']
    for folder in folders :
        folder = folder
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                     shutil.rmtree(file_path)
            except Exception as e:
                print(e)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('bulk')
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
                        
                        user = User.objects.create_user(username=username, password=password)
                        # user.userprofile.user = authenticate(username=username, password=password)
                        user.save()
                        user = authenticate(username=username, password=password)
                        
                        profile = Profile()
                        profile.user = user
                        profile.save()

                        login(request, user)
                        messages.success(request, 'Account was created')
                        print("Account was created")


                        return redirect('bulk')

        return render(request, 'index.html')
            
def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required
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
    global media_url
    loaded_model = pickle.load(open('finalized_model.sav', 'rb'))
    if request.method == "POST":
        print("helsslo")
        print(os.listdir(settings.MEDIA_ROOT))
        files = os.listdir(settings.MEDIA_ROOT)
        df_total = pd.DataFrame()
        context = {}
        for file in files:
            df=pd.read_csv(settings.MEDIA_ROOT+'/'+file)
            #df=df.drop(['id'],axis=1)
            df["diagnosis"] = np.nan
            row_len=len(df)
            df_x=df.drop(['diagnosis'],axis=1)
            df_x=df_x.drop(['id'],axis=1)
            for row in range(0,row_len):
                row_vector = df_x.iloc[row]
                X_test=row_vector.to_numpy().reshape(1,-1)
                value=""
                if len(X_test[0])!=30:
                    df.iloc[row]['diagnosis']= "error"
                    print("Column Error")
                else:
                    Y_pred = loaded_model.predict(X_test)
                    if Y_pred==1:
                        # value="Malignant"
                        value = 1
                    else:
                        # value="Benign"
                        value = 0
                    print(value)
                   
                    df.at[row, 'diagnosis'] = value
                    print(df.iloc[row]['diagnosis'])
            # geeks_object = df.to_html()
            # return HttpResponse(geeks_object)
            df_total = pd.concat([df_total, df])

            print(df)
            # df.close()
            # df.to_csv('Predicted/'+file[:-4]+'_predicted.csv')
            # json_records = df.reset_index().to_json(orient ='records')
            # data = []
            # data = json.loads(json_records)
            # context[file] = data

        print(df_total)
        json_records = df_total.reset_index().to_json(orient ='records')
        data = []
        data = json.loads(json_records)
        context = {'d': data}
        print(context)
        delete()
        return render(request, 'table.html', context)



    return render(request, 'bulk.html')

def index(request):
    return redirect('login')

@csrf_protect
def single(request):
    if request.method == "POST":
        print("Post")
        loaded_model = pickle.load(open('finalized_model.sav', 'rb'))

        mean_radius = float(request.POST.get('mean_radius'))
        mean_texture = float(request.POST.get('mean_texture'))
        mean_perimeter = float(request.POST.get('mean_perimeter'))
        mean_area = float(request.POST.get('mean_area'))
        mean_smoothness = float(request.POST.get('mean_smoothness'))
        mean_compactness = float(request.POST.get('mean_compactness'))
        mean_concavity = float(request.POST.get('mean_concavity'))
        mean_concave_points = float(request.POST.get('mean_concave_points'))
        mean_symmetry = float(request.POST.get('mean_symmetry'))
        mean_fractal_dimension = float(request.POST.get('mean_fractal_dimension'))
        SE_radius = float(request.POST.get('SE_radius'))
        SE_texture = float(request.POST.get('SE_texture'))
        SE_perimeter = float(request.POST.get('SE_perimeter'))
        SE_area = float(request.POST.get('SE_area'))
        SE_smoothness = float(request.POST.get('SE_smoothness'))
        SE_compactness = float(request.POST.get('SE_compactness'))
        SE_concavity = float(request.POST.get('SE_concavity'))
        SE_concave_points = float(request.POST.get('SE_concave_points'))
        SE_symmetry = float(request.POST.get('SE_symmetry'))
        SE_fractal_dimension = float(request.POST.get('SE_fractal_dimension'))
        worst_radius = float(request.POST.get('worst_radius'))
        worst_texture = float(request.POST.get('worst_texture'))
        worst_perimeter = float(request.POST.get('worst_perimeter'))
        worst_area = float(request.POST.get('worst_area'))
        worst_smoothness = float(request.POST.get('worst_smoothness'))
        worst_compactness = float(request.POST.get('worst_compactness'))
        worst_concavity = float(request.POST.get('worst_concavity'))
        worst_concave_points = float(request.POST.get('worst_concave_points'))
        worst_symmetry = float(request.POST.get('worst_symmetry'))
        worst_fractal_dimension = float(request.POST.get('worst_fractal_dimension'))

        arr = [
            mean_radius,
            mean_texture,
            mean_perimeter,
            mean_area,
            mean_smoothness,
            mean_compactness,
            mean_concavity,
            mean_concave_points,
            mean_symmetry,
            mean_fractal_dimension,
            SE_radius,
            SE_texture,
            SE_perimeter,
            SE_area,
            SE_smoothness,
            SE_compactness,
            SE_concavity,
            SE_concave_points,
            SE_symmetry,
            SE_fractal_dimension,
            worst_radius,
            worst_texture,
            worst_perimeter,
            worst_area,
            worst_smoothness,
            worst_compactness,
            worst_concavity,
            worst_concave_points,
            worst_symmetry,
            worst_fractal_dimension,
        ]
        print(arr)
        X = numpy.array(arr)
        X = X.reshape(1, -1) 
        print("len",len(X))
        Y_pred = loaded_model.predict(X)
        value = 'Error'
        if Y_pred==1:
            value="Malignant"
        else:
            value="Benign"
        print(value)
        return render(request, 'single.html',{'predicted':value})

    print(1)
    return render(request, 'single.html')