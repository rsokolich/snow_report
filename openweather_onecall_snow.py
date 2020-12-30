
import requests, json
from requests import post
import config
from datetime import datetime

skiMountains = [    
    {'Mountain':'Windham', 'lat': '42.29514752427534', 'lon': '-74.25446876948166'},
    {'Mountain':'Belleayre', 'lat': '42.141549317730025', 'lon': '-74.50222551697323'},
    {'Mountain':'Jiminy Peak', 'lat': '42.55533833231327', 'lon': '-73.29216498627747'},
    {'Mountain':'Whiteface', 'lat': '44.366707860529445', 'lon': '-73.90294603235303'},        
    {'Mountain':'Mount Snow', 'lat': '42.96840868802465', 'lon': '-72.89452347305692'},
    {'Mountain':'Killington', 'lat': '43.626995266004', 'lon': '-72.79687808822811'},
    {'Mountain':'Stowe', 'lat': '44.530388407733454', 'lon': '-72.78136189972808'},
    {'Mountain':'Vale', 'lat': '39.606342762525685', 'lon': '-106.35490732866448'},
    {'Mountain':'Telluride', 'lat': '37.93671168130935', 'lon': '-107.84660984750525'},
    {'Mountain':'Park City', 'lat': '40.64513741009838', 'lon': '-111.49613343049562'},
    {'Mountain':'Squaw Valley', 'lat': '39.19786387248803', 'lon': '-120.23542469877086'}
    ] 

def querySnow(locations):
    
    raw_data = [] 

    for location in locations:    
        params = (
            ('lat', location['lat']),
            ('lon', location['lon']),
            ('units', 'imperial'),
            ('exclude', 'minutely,hourly'),
            ('appid', config.ow_api_key)
        )

        response = requests.get('https://api.openweathermap.org/data/2.5/onecall', params=params)
        weatherJson = json.loads(response.text)
        weatherData = weatherJson['daily']
        skiMountain = location['Mountain']


        for weather in weatherData:
            for snow in weather['weather']:                 
                if snow['main'] == 'Snow':
                    if snow['description'] != 'light snow':                        
                        accumulation = weather['snow'] / 25.4
                        if accumulation > 1:
                            date_time = datetime.fromtimestamp(weather['dt'])
                            date = date_time.strftime("%a %x")        
                            data_load = {'Date': date, 'skiMountain': skiMountain, 'Accumulation': str(round(accumulation, 2))}
                            raw_data.append(data_load)

    report = ('\n'.join(map(str, raw_data)))
    
    message = "This report lists the daily snow forecasted for the next seven days to be greater than an inch for ski mountains of interest:" + '\n'
    
    ifttt_webhook_url = 'https://maker.ifttt.com/trigger/%s/with/key/%s?value1=%s&value2=%s' % (config.ifttt_alert_name, config.ifttt_alert_key, message, report)
    print(message, report, post(ifttt_webhook_url))
    
querySnow(skiMountains)