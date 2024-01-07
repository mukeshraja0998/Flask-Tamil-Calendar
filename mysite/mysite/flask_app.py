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

y=''
os.environ["TZ"] = "Asia/Calcutta"
time.tzset()
format = "%Y-%m-%d %H:%M:%S"
x=''

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
    return render_template("news.html",x=x,y=y)

@app.route('/all-calender',methods=['POST','GET'])
def all_calender():
    if request.method=='POST':
        session['date']=request.form['date']
        if session['date'][-2]=='0':
            y='https://www.tamildailycalendar.com/'+session['date'][0:4]+'/'+session['date'][-1]+session['date'][5:7]+session['date'][0:4]+'.jpg'
            return render_template("news.html",y=y)
        else:
            y='https://www.tamildailycalendar.com/'+session['date'][0:4]+'/'+session['date'][-2]+session['date'][-1]+session['date'][5:7]+session['date'][0:4]+'.jpg'
            return render_template("news.html",y=y)
    else:
        return render_template("all_cal.html")
    
@app.route('/astro',methods=["POST","GET"])
def astro():
    if request.method=="POST":
        session['astro']=request.form['astro']
        url='http://horoscope-api.herokuapp.com/horoscope/today/'+session['astro']
        url1='http://horoscope-api.herokuapp.com/horoscope/week/'+session['astro']
        url2='http://horoscope-api.herokuapp.com/horoscope/month/'+session['astro']
        url3='http://horoscope-api.herokuapp.com/horoscope/year/'+session['astro']
        r = requests.get(url)
        r1=requests.get(url1)
        r2=requests.get(url2)
        r3=requests.get(url3)
        data=r.json()
        d1=r1.json()
        d2=r2.json()
        d3=r3.json()
        data1=data['horoscope']
        data2=d1['horoscope']
        data3=d2['horoscope']
        data4=d3['horoscope']
        translator = Translator()
        result = translator.translate(data1, dest='ta')
        result1=translator.translate(data2, dest='ta')
        result2=translator.translate(data3, dest='ta')
        result3=translator.translate(data4, dest='ta')
        return render_template("astro.html",xx=y,x=x,y=data1,z=result.text,aa=result1.text,bb=result2.text,cc=result3.text,rasi=data['sunsign'])
    else:
        return render_template("astro_home.html")
    
    
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
        return render_template("news.html",y=finalUrl)
    else:
        return render_template("monthly-calendar.html")

if __name__ == '__main__':
    app.run(debug = True)

'''if __name__ == '__main__':
    app.run(host="192.168.1.13",debug = True)'''
