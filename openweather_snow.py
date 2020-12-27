
import requests, json
from requests import post
import config

zipCodes = ['10536,us','12853,us','12496,us', '01237,us', '05751,us', '05672,us', '81435,us']

skiMountains = {
    'North Creek': 'Gore',
    'Lanesborough': 'Jiminy Peak'
}

def querySnow(zipCodes):

    report = []  

    for zipCode in zipCodes:
        zipCode = str(zipCode)
 
        params = (
            ('zip', zipCode),
            ('units', 'imperial'),
            ('appid', config.ow_api_key)
        )

        response = requests.get('https://api.openweathermap.org/data/2.5/forecast', params=params)
        weatherData = json.loads(response.text)
        w = weatherData['list']
        city = weatherData['city']['name']
        country = weatherData['city']['country']        

        for weather in w:            
            for snow in weather['weather']:
                if snow['main'] == 'Snow':
                    if snow['description'] != 'light snow':                                                                     
                        accumulation = weather['snow']['3h'] / 25.4
                        if city in skiMountains:
                            skiMountain = skiMountains.get(city)                            
                            data = {'Date':weather['dt_txt'], 'Mountain':skiMountain, 'Accumulation':str(round(accumulation, 2))}
                            report.append(data)
                        else:                            
                            data = {'Date':weather['dt_txt'], 'Mountain':city, 'Accumulation':str(round(accumulation, 2))}
                            report.append(data)                       

    finalReport = ('\n'.join(map(str, report)))
    #print(*report, sep = "\n") 
    
    message = "This report details the forecasted snowfall in inches:" + '\n'
    
    ifttt_webhook_url = 'https://maker.ifttt.com/trigger/%s/with/key/%s?value1=%s' % (config.ifttt_alert_name, config.ifttt_alert_key, finalReport)
    print(message, finalReport, post(ifttt_webhook_url))

querySnow(zipCodes)


