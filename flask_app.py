from flask import Flask,session
from flask.globals import request
from flask.templating import render_template
from datetime import datetime
import calendar
from pytz import timezone
from tzlocal import get_localzone
from pprint import pprint
import os
import json
import time
import requests
import re
import base64

y=''
os.environ["TZ"] = "Asia/Calcutta"
time.tzset()
format = "%Y-%m-%d %H:%M:%S"
x=''


def initial(url):
    headers = {
    'Host': 'www.tamildailycalendar.com',  # Usually not necessary to set manually
    'Referer': 'https://www.tamildailycalendar.com/tamil_daily_calendar.php',
    'User-Agent': 'Wget/1.21.2',
    'Accept': '*/*',
    'Accept-Encoding': 'identity',
    'Connection': 'Keep-Alive'
    }
    response = requests.get(url, headers=headers)
    return response



app=Flask(__name__)
app.secret_key = "calender"
@app.route('/')
def home():
    global y
    now_utc = datetime.now(timezone('UTC'))
    now_local = now_utc.astimezone(get_localzone())
    li=now_local.strftime(format)
    li=li.split(' ')
    cal=li[0].split('-')
    time=li[1]
    mon=calendar.month_name[int(cal[1])]
    year=cal[0]
    date=cal[2]
    x=mon+'-'+date+'-'+year
    today_calender()
    return render_template("index.html",x=x,yy=y)

@app.route('/today-calender')
def today_calender():
    global y
    now_utc = datetime.now(timezone('UTC'))
    now_local = now_utc.astimezone(get_localzone())
    li=now_local.strftime(format)
    li=li.split(' ')
    cal=li[0].split('-')
    time=li[1]
    mon=calendar.month_name[int(cal[1])]
    year=cal[0]
    date=cal[2]
    x=mon+'-'+date+'-'+year
    if cal[-1][0]=='0':
        cal[-1]=cal[-1][1::]
    y='https://www.tamildailycalendar.com/'+cal[0]+'/'+cal[2]+cal[1]+cal[0]+'.jpg'
    response=initial(y)
    if response.status_code == 200:
        # Encode the image in base64
        image_data = base64.b64encode(response.content).decode('utf-8')
        return render_template('DailyCal.html',x=x,y=image_data)
    return render_template("DailyCal.html",x=x,y=y)

@app.route('/all-calender',methods=['POST','GET'])
def all_calender():
    if request.method=='POST':
        session['date']=request.form['date']
        if session['date'][-2]=='0':
            y='https://www.tamildailycalendar.com/'+session['date'][0:4]+'/'+session['date'][-1]+session['date'][5:7]+session['date'][0:4]+'.jpg'
        else:
            y='https://www.tamildailycalendar.com/'+session['date'][0:4]+'/'+session['date'][-2]+session['date'][-1]+session['date'][5:7]+session['date'][0:4]+'.jpg'
        response=initial(y)
        if response.status_code == 200:
            image_data = base64.b64encode(response.content).decode('utf-8')
            return render_template('DailyCal.html',x=x,y=image_data)
        else:
            return render_template("index.html")
    else:
        return render_template("all_cal.html")
    
@app.route('/montly-calendar',methods=['POST','GET'])
def montlhy_calender():
    if request.method=='POST':
        session['monthYear']=request.form['monthYear'] #2023-11
        x = re.search(r"202[2-9]-(0[1-9]|1[0-2])", session['monthYear'])  #202[2-9]-(0[1-9]|1[0-2])
        if(x):
            try:
                month=session['monthYear'].split("-")[1]
                year=session['monthYear'].split("-")[0]
            except:
                month="11"
                year="2023"
        else:
            return render_template("monthly-calendar.html")
        finalUrl='https://www.tamildailycalendar.com/'+year+"_Monthly/"+month+"_Tamil_Monthly_Calendar_"+calendar.month_name[int(month)]+"_"+year+".jpg"
        response=initial(finalUrl)
        if response.status_code == 200:
            # Encode the image in base64
            image_data = base64.b64encode(response.content).decode('utf-8')
            return render_template('DailyCal.html',x=x,y=image_data)
        else:
            return render_template("monthly-calendar.html")
        
    else:
        return render_template("monthly-calendar.html")

if __name__ == '__main__':
    app.run(debug = True)

'''if __name__ == '__main__':
    app.run(host="192.168.1.13",debug = True)'''
