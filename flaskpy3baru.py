#!D:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64\python.exe

import os
import cgi
import smtplib
import requests
import urllib.request
import json
import pymysql
from datetime import timedelta
from flask import Flask, request, render_template,session,redirect


app = Flask(__name__)
app.secret_key ='string'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)


@app.route("/")
def index():
	return render_template("index.html")

@app.route("/cek/", methods=['GET', 'POST'])
def cek():
	if request.method == 'POST':
		db = pymysql.connect("localhost","root","","tos")
		cursor = db.cursor()
		sql = "SELECT * FROM users WHERE username='"+request.form['username']+"' AND password='"+request.form['password']+"'"
		row = cursor.execute(sql)
		if row == 0:
			return render_template("index.html")
		else:
			session['username'] = request.form['username']
			#session.permanent = True
			return render_template("weather.html")
	else:
		return "You are probably using GET"

@app.route("/result/", methods=['GET', 'POST'])
def result():
	if request.method == 'POST':
		if 'username' in session:
			city = request.form['inputcity']
			city = city.capitalize()
			geourl = "http://api.apixu.com/v1/current.json?key=3cde047cd6a04bb6b3225401190106&q="+city+""
			try: 
				response = urllib.request.urlopen(geourl)
			except:
				return render_template("weather.html")
			content = response.read()
			data = json.loads(content.decode("utf8"))
			tanggal = data['location']['localtime']
			tanggal = tanggal[0:10]
			jam = data['location']['localtime']
			jam = jam[11:16]
			pilih = data['current']['condition']['text'].lower()
			if pilih.find('cloudy') != -1:
				hari = data['current']['is_day']
				if hari == 1:
					gambar = 'https://drive.google.com/file/d/1CyO6YY8IB7o_MX6h605UkNx2IJUVesg8/preview'
				else:
					gambar = 'https://drive.google.com/file/d/1Au7IgILjLXXd9RFEKfkHRXNaC-mqii_Z/preview'
			elif pilih.find('blizzard') != -1:
				hari = data['current']['is_day']
				if hari == 1:
					gambar = 'https://drive.google.com/file/d/1QncJMob8nX14dLcQrZYQIawV609HnoNh/preview'
				else:
					gambar = 'https://drive.google.com/file/d/1pLCx6uor0CyR5IBIW64H5NcXKy3McgP7/preview'
			elif pilih.find('drizzle') != -1:
				hari = data['current']['is_day']
				if hari == 1:
					gambar = 'https://drive.google.com/file/d/1wYlQpeU7StDP21uIAzwLWPEC8nMpXf3m/preview'
				else:
					gambar = 'https://drive.google.com/file/d/1h_n_nyJlKgTgSqwOhiH15CcnmXrMYQbg/preview'
			elif pilih.find('fog') != -1:
				hari = data['current']['is_day']
				if hari == 1:
					gambar = 'https://drive.google.com/file/d/13yGgBZS0Q1kGVh_8yN-8zthOEDMUK8bo/preview'
				else:
					gambar = 'https://drive.google.com/file/d/1pqQ6fTvo0e9MOSVUXVx63SZJKr7pM6gD/preview'
			elif pilih.find('mist') != -1:
				hari = data['current']['is_day']
				if hari == 1:
					gambar = 'https://drive.google.com/file/d/1__xOec8ryo3PDRNvOhZPSLti3vbzTMwe/preview'
				else:
					gambar = 'https://drive.google.com/file/d/1yAWuF427gGSc6sp4EW7tGQuYH08LANvG/preview'
			elif pilih.find('overcast') != -1:
				hari = data['current']['is_day']
				if hari == 1:
					gambar = 'https://drive.google.com/file/d/1xQqXNJ_NSjbP_zxg0oxxUiL7k40grND7/preview'
				else:
					gambar = 'https://drive.google.com/file/d/1l3njkljCwCH8fFvdplOPQsjSlC6QcXGR/preview'
			elif pilih.find('rain') != -1:
				hari = data['current']['is_day']
				if hari == 1:
					gambar = 'https://drive.google.com/file/d/1wZWwJmpbTNhR-sRtBMW_6rysRO6zh11q/preview'
				else:
					gambar = 'https://drive.google.com/file/d/1d0uOwQ2zMbRPUJL0T8hR8x3pH71DMZyY/preview'
			elif pilih.find('sleet') != -1:
				hari = data['current']['is_day']
				if hari == 1:
					gambar = 'http://lkmm-td.petra.ac.id/gambar/weathering/sleet-day.jpg'
				else:
					gambar = 'http://lkmm-td.petra.ac.id/gambar/weathering/sleet-night.jpg'
			elif pilih.find('snow') != -1:
				hari = data['current']['is_day']
				if hari == 1:
					gambar = 'http://lkmm-td.petra.ac.id/gambar/weathering/snow-day.jpg'
				else:
					gambar = 'http://lkmm-td.petra.ac.id/gambar/weathering/snow-night.jpg'
			elif pilih.find('thundery') != -1:
				hari = data['current']['is_day']
				if hari == 1:
					gambar = 'http://lkmm-td.petra.ac.id/gambar/weathering/thundery-day.jpg'
				else:
					gambar = 'http://lkmm-td.petra.ac.id/gambar/weathering/thundery-night.jpg'
			elif pilih.find('clear') != -1:
				gambar = 'http://lkmm-td.petra.ac.id/gambar/weathering/clear.jpg'
			elif pilih.find('sunny') != -1:
				gambar = 'http://lkmm-td.petra.ac.id/gambar/weathering/sunny.jpg'
			else:
				gambar = 'http://lkmm-td.petra.ac.id/gambar/slide-1.jpg'
			return render_template("result.html", results=data, tanggal=tanggal, jam=jam,hai=gambar)
		else:
			return render_template("index.html")
	else:
		return "You are probably using GET"
		
@app.route("/signup/", methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		db = pymysql.connect("localhost","root","","tos")
		cursor = db.cursor()
		sql = "INSERT INTO users(`username`, `password`) VALUES ('"+request.form['username']+"','"+request.form['password']+"')"
		row = cursor.execute(sql)
		db.commit()
		return render_template("index.html")
	else:
		return "You are probably using GET"

@app.route("/cekk/", methods=['GET', 'POST'])
def cekk():
	if 'username' in session:
		return render_template("weather.html")
	else:
		return render_template("index.html")

@app.route("/logout/", methods=['GET', 'POST'])
def log():
	session.pop('username',None)
	return render_template("index.html")

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=7051, debug=True)
