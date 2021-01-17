
import requests, json
from requests import post
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from datetime import datetime
import time
import schedule
import config

skiMountains = [    
    {'Mountain':'Windham', 'lat': '42.29514752427534', 'lon': '-74.25446876948166'},
    {'Mountain':'Belleayre', 'lat': '42.141549317730025', 'lon': '-74.50222551697323'},
    {'Mountain':'Jiminy Peak', 'lat': '42.55533833231327', 'lon': '-73.29216498627747'},
    {'Mountain':'Gore', 'lat': '43.6734333798601', 'lon': '-74.00642707699728'},
    {'Mountain':'Whiteface', 'lat': '44.366707860529445', 'lon': '-73.90294603235303'},        
    {'Mountain':'Mount Snow', 'lat': '42.96840868802465', 'lon': '-72.89452347305692'},
    {'Mountain':'Okemo', 'lat': '43.40515537722277', 'lon': '-72.71732402745563'},
    {'Mountain':'Killington', 'lat': '43.626995266004', 'lon': '-72.79687808822811'},
    {'Mountain':'Stowe', 'lat': '44.530388407733454', 'lon': '-72.78136189972808'},
    {'Mountain':'Vale', 'lat': '39.606342762525685', 'lon': '-106.35490732866448'},
    {'Mountain':'Telluride', 'lat': '37.93671168130935', 'lon': '-107.84660984750525'},
    {'Mountain':'Park City', 'lat': '40.64513741009838', 'lon': '-111.49613343049562'},
    {'Mountain':'Squaw Valley', 'lat': '39.19786387248803', 'lon': '-120.23542469877086'}
    ] 

reportAccummulation = '.5'

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
        try:
            response = requests.get('https://api.openweathermap.org/data/2.5/onecall', params=params)             
            weatherJson = json.loads(response.text)
            weatherData = weatherJson['daily']
            skiMountain = location['Mountain']
            for weather in weatherData:
                for snow in weather['weather']:                 
                    if snow['main'] == 'Snow':                                               
                        accumulation = weather['snow'] / 25.4
                        if accumulation > float(reportAccummulation):
                            date_time = datetime.fromtimestamp(weather['dt'])
                            date = date_time.strftime("%a %x")        
                            data_load = {'Date': date, 'skiMountain': skiMountain, 'Accumulation': str(round(accumulation, 2))}
                            raw_data.append(data_load)       
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print("Unable to query api.openweathermap.org\n%s" % e)                                    
    # print(raw_data)
    # report = ('\n'.join(map(str, raw_data)))
    # print(report)
    

    if len(raw_data) == 0:                
        message = "Unfortunately there is no snow greater than " + reportAccummulation + " inches in this forecast ):"
        # print(message)
        try:            
            ifttt_webhook_url = 'https://maker.ifttt.com/trigger/%s/with/key/%s?value1=%s' % (config.ifttt_alert_name, config.ifttt_alert_key, message)
            print(message, post(ifttt_webhook_url))
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print("Unable to query maker.ifttt.com\n%s" % e)  
    else:
        report = []                       
        for d in raw_data:            
            report.append("***On %s in %s it will snow %s inches.***" % (d['Date'], d['skiMountain'], d['Accumulation']))                   
        report = '\n'.join(report)
        print(report)
        message = "This report lists the daily snow forecasted to be greater than " + reportAccummulation + " inches for the next seven days in the following ski mountains of interest:" + '\n'
        try:            
            ifttt_webhook_url = 'https://maker.ifttt.com/trigger/%s/with/key/%s?value1=%s&value2=%s' % (config.ifttt_alert_name, config.ifttt_alert_key, message, report)
            print(message, report, post(ifttt_webhook_url))
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print("Unable to query maker.ifttt.com\n%s" % e)  
        

schedule.every().day.at("08:00").do(querySnow, skiMountains)
# schedule.every(1).minutes.do(querySnow, skiMountains)
# schedule.every(5).seconds.do(querySnow, skiMountains)

while True:
    schedule.run_pending()
    time.sleep(300)

# querySnow(skiMountains)