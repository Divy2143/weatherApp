from django.shortcuts import render

# Create your views here.

def index(request) :
    if request.method == 'POST' :
        city = request.POST['city'] 
    else :
        city = {}
    return render(request, 'index.html', {'city' : city})
    # data = {'country_code' : True}
    # city = {}
    # return render(request, 'index.html', {'data' : data, 'city' : city})