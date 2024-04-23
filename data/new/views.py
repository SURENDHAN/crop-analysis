from django.shortcuts import render,redirect
from .forms import DistrictForm,YearForm,InputDataForm
from .statee import statee,yeare
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
import pandas as pd
def home(request):
    return render(request,'new/home.html')

def plot_state_graph(request):
    if request.method == 'POST':
        form = DistrictForm(request.POST)
        if form.is_valid():
            selected_state = form.cleaned_data['district']
            plot = statee(selected_state)
            return render(request, 'new/state.html', {'plot': plot, 'selected_state': selected_state})
    else:
        form = DistrictForm()
    return render(request, 'new/select.html', {'form': form})
def login_or_signup_view(request):
    if request.method == 'POST':
        if request.POST.get('action') == 'login':
            login_form = AuthenticationForm(request, request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home/')
            return render(request,'new/error.html')
    else:
        login_form = AuthenticationForm()
    return render(request, 'new/login.html', {'login_form': login_form})
def plot_crop_distribution(request):
    if request.method == 'POST':
        form = YearForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            plot_base64 = yeare(year)
            context = {'plot_base64': plot_base64}
            return render(request, 'new/crop_distribution.html', context)
    else:
        form = YearForm()
    return render(request, 'new/input_year.html', {'form': form})
import pickle
def predict_output(request):
    output = None
    form = InputDataForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        area = form.cleaned_data['area']
        production = form.cleaned_data['production']
        try:
            with open('C:/Users/nithi/Downloads/yield.pkl', 'rb') as f:
                model = pickle.load(f)
            input_data = pd.DataFrame({'Area': [area], 'Production': [production]})
            output = model.predict(input_data)
        except Exception as e:
            output = f"Prediction error: {str(e)}"
    return render(request, 'new/input_data.html', {'form': form, 'output': output})