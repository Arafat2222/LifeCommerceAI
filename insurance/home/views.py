import os
import time
from django.http import HttpResponse
from django.shortcuts import render,redirect
import joblib
import pandas as pd
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout as django_logout
from django.views.decorators.cache import never_cache
from django.contrib.sessions.models import Session
from django.utils.cache import patch_cache_control
# from insurance.insurance.settings import BASE_DIR
model = joblib.load('static/random_forest_regressor')
heart_pred = joblib.load('static/logistic_regression_model_heart')
liver_pred = joblib.load('static/Voting_Classifier_liverDisease')

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import ContactForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import *
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd  # Ensure you import pandas if you're using it for predictions
import openai
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai

from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat

from django.utils import timezone







@csrf_protect
def contact(request):
    if request.method == 'POST':
        # Get data from the POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Save data to the Contact model
        Contact.objects.create(name=name, email=email, phone=phone, message=message)

        # Display success message
        messages.success(request, 'Your message has been sent successfully.')

        # Redirect to the same contact page or another page after success
        return redirect('contact')  # Ensure this redirects to the correct URL

    # Handle the GET request by rendering the contact form
    return render(request, 'contact.html')

@csrf_protect
def registerPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match. Please try again.')
            return render(request, 'signup.html')

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken. Please choose a different username.')
            return render(request, 'signup.html')

        # Create the user if everything is valid
        user = User.objects.create_user(username=username, email=email, password=password)

        # Authenticate and log the user in
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'You have successfully signed up!')
            return redirect('login')

    return render(request, 'signup.html')

@csrf_protect
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
           # messages.success(request, 'You have successfully logged in!')
            return redirect('home')  # Redirect to home after successful login
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')  # Stay on login page if authentication fails

    return render(request, 'login.html')



def homepage(request):
    return render(request, 'homePage.html')

  
def logout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You must be logged in")
        return redirect('login')
    django_logout(request)
    return redirect('homepage')  
   
   

def index(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You must be logged in")
        return redirect('login')
    return render(request, 'index.html')

def about(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You must be logged in")
        return redirect('login')
    return render(request, 'about.html')
@csrf_protect
def prediction(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You must be logged in")
        return redirect('login')
    if request.method == 'POST':
        age = int(request.POST.get('age'))
        sex = int(request.POST.get('sex'))
        bmi = float(request.POST.get('bmi'))
        children = int(request.POST.get('children'))
        smoker = int(request.POST.get('smoker'))
        region = request.POST.get('region')
        print(age,sex,bmi,smoker,region)
        pred = round(model.predict([[age,sex,bmi,children,smoker,region]])[0])
        print(pred)
        output = {"output":pred}
        return render(request, 'prediction.html',output)
        
    return render(request, 'prediction.html')


@csrf_protect
def heart_disease(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You must be logged in")
        return redirect('login')
    return render(request, 'heart-disease.html')




@csrf_protect
def heart_disease_prediction(request):
    if request.method == 'POST':
        name = str(request.POST.get('name')).strip()
        # Converting form data to appropriate data types
        age = int(request.POST.get('age'))
        sex = int(request.POST.get('sex'))
        cp = int(request.POST.get('cp'))
        trestbps = int(request.POST.get('trestbps'))
        chol = int(request.POST.get('chol'))
        fbs = int(request.POST.get('fbs'))
        restecg = int(request.POST.get('restecg'))
        thalach = int(request.POST.get('thalach'))
        exang = int(request.POST.get('exang'))
        oldpeak = float(request.POST.get('oldpeak'))
        slope = int(request.POST.get('slope'))
        ca = int(request.POST.get('ca'))
        thal = int(request.POST.get('thal'))

        # Organize data into a DataFrame for prediction
        input_data = {
            'age': age,
            'sex': sex,
            'cp': cp,
            'trestbps': trestbps,
            'chol': chol,
            'fbs': fbs,
            'restecg': restecg,
            'thalach': thalach,
            'exang': exang,
            'oldpeak': oldpeak,
            'slope': slope,
            'ca': ca,
            'thal': thal
        }
        
        # Convert to DataFrame for prediction model
        data = pd.DataFrame([input_data])  # Keep this as it is
        # Here you would call your prediction model
        try:
            result = heart_pred.predict(data)  # Ensure this works as expected
            #print(result[0])  # Debugging output
        except Exception as e:
            print(f"Prediction error: {e}")  # Capture any errors for debugging
            return render(request, 'heart_disease_predi.html', {'error': 'Prediction failed.'})
        
        input_data.update({'name':name}),  
        if result[0] > 0:
            input_data.update({'heart_disease': "Positive"})
        else:
            input_data.update({'heart_disease': "Negative"})      
        # Prepare output data for rendering
        output_data = {
           
            "input_data": input_data,
            "prediction_result": result[0]  # Assuming result is an ndarray or similar
        }

        # Render the appropriate template with output data
        return render(request, 'heart_disease_predi.html', output_data)

    # Render the form page for GET requests
    return render(request, 'heart-disease.html')
@csrf_protect
def liver_disease(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You must be logged in")
        return redirect('login')
    if request.method == 'POST':
        name = str(request.POST.get('name')).strip()
        # Converting form data to appropriate data types
        # Collect form data
        age = int(request.POST.get('age'))
        gender = int(request.POST.get('gender'))
        bmi = float(request.POST.get('bmi'))
        alcohol = float(request.POST.get('alcohol'))
        smoking = int(request.POST.get('smoking'))
        genetic_risk = int(request.POST.get('geneticRisk'))
        physical_activity = float(request.POST.get('physicalActivity'))
        diabetes = int(request.POST.get('diabetes'))
        hypertension = int(request.POST.get('hypertension'))
        liver_function_test = float(request.POST.get('liverFunctionTest'))

        # Organize data into a DataFrame for prediction
        input_data = {
            'age': age,
            'gender': gender,
            'bmi': bmi,
            'alcohol': alcohol,
            'smoking': smoking,
            'genetic_risk': genetic_risk,
            'physical_activity': physical_activity,
            'diabetes': diabetes,
            'hypertension': hypertension,
            'liver_function_test': liver_function_test
        }

        print(input_data)

        
        # Convert to DataFrame for prediction model
        data = pd.DataFrame([input_data])  # Keep this as it is
        # Here you would call your prediction model
        try:
            result = liver_pred.predict(data)  # Ensure this works as expected
            #print(result[0])  # Debugging output
        except Exception as e:
            print(f"Prediction error: {e}")  # Capture any errors for debugging
            return render(request, 'heart_disease_predi.html', {'error': 'Prediction failed.'})
        
        input_data.update({'name':name}),  
        if result[0] > 0:
            input_data.update({'heart_disease': "Positive"})
        else:
            input_data.update({'heart_disease': "Negative"})      
        # Prepare output data for rendering
        output_data = {
           
            "input_data": input_data,
            "prediction_result": result[0]  # Assuming result is an ndarray or similar
        }
        print(output_data['prediction_result'])

        # Render the appropriate template with output data
        return render(request, 'liver_disease_pred.html', output_data)

    # Render the form page for GET requests
    return render(request, 'liver-disease.html')

