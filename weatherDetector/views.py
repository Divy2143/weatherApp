from django.shortcuts import render
import json
import urllib.request
# Create your views here.

def index(request) :
    if request.method == 'POST' :
        city = request.POST['city']
        res = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+city+'&appid=ac90f5e86885780b15ee13535e6aa100').read()
        # res = urllib.request.urlopen('http://api.openweathermap.org/geo/1.0/direct?q='+city+'&appid=ac90f5e86885780b15ee13535e6aa100').read()
        json_data = json.loads(res)  
        data = {
            'country_code' : str(json_data['sys']['country']),
            'coordinate' : 'Lat : ' + str(json_data['coord']['lat']) + ', ' + 'Lon : ' + str(json_data['coord']['lon']),
            'temp' : str(json_data['main']['temp']) + 'k',
            'pressure' : str(json_data['main']['pressure']),
            'humidity' : str(json_data['main']['humidity']),
        }

    else :
        data = {}
        city = {}
    return render(request, 'index.html', {'city' : city, 'data' : data})
    # data = {'country_code' : True}
    # city = {}
    # return render(request, 'index.html', {'data' : data, 'city' : city})