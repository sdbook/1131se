from flask import Flask, render_template, request, session, redirect
import json
from functools import wraps
#from dbUtils import getList
import dbUtils as DB

# creates a Flask application, specify a static folder on /
app = Flask(__name__, static_folder='static',static_url_path='/')
#set a secret key to hash cookies
app.config['SECRET_KEY'] = '123TyU%^&'

#define a function wrapper to check login session
def login_required(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		loginID = session.get('loginID')
		if not loginID:
			return redirect('/loginPage.html')
		return f(*args, **kwargs)
	return wrapper

#another way to check login session
def isLogin():
	return session.get('loginID')
	

@app.route("/")
#check login with decorator function
@login_required
def hello(): 
	message = "Hello, World 1"
	return message

@app.route("/getAjaxData", methods=['POST'])
#取得網址作為參數
def getdata111():
    id=request.form['userID']
    name=request.form['userName']
    return f"I got your input: {id}, {name}"

@app.route("/test/<string:name>/<int:id>")
#取得網址作為參數
def useParam(name,id):
	#check login inside the function
	if not isLogin():
		return redirect('/loginPage.html')
	return f"got name={name}, id={id} "

@app.route("/secret")
#使用server side render: template 樣板
def showSecret():
    return "<img src='/dog.jpg' />";

@app.route("/edit")
#使用server side render: template 樣板
def h1():
	dat={
		"name": "大牛",
		"content":"內容說明文字"
	}
	#editform.html 存在於 templates目錄下, 將dat 作為參數送進 editform.html, 名稱為 data
	return render_template('editform.html', data=dat)

@app.route("/list")
#使用server side render: template 樣板
def h2():
	dat=[
		{
			"name": "大牛",
			"p":"愛吃瓜"
		},
		{
			"name": "小李",
			"p":"怕榴槤"
		},
		{
			"name": "",
			"p":"ttttt"
		},
		{
			"name": "老謝",
			"p":"來者不拒"
		}
	]
	return render_template('list.html', data=dat)

#取得使用者輸入之資料
@app.route('/input', methods=['GET', 'POST'])
def userInput():
	if request.method == 'POST':
		form =request.form
	else:
		form= request.args

	txt = form['txt']  # pass the form field name as key
	note =form['note']
	select = form['sel']
	msg=f"method: {request.method} txt:{txt} note:{note} sel: {select}"
	return msg

#call utils.py 之函數取得資料資料，再用template產生網頁傳給browser
@app.route("/listJob")
#使用server side render: template 樣板
def gl():
	dat=DB.getList()
	return render_template('todolist.html', data=dat)

#call utils.py 之函數取得資料資料，將資料包成JSON格式，傳給browser處理
@app.route("/getListJSON", methods=['POST'])
#使用server side render: template 樣板
def listJSON():

	dat=DB.getList()
	return json.dumps(dat)

#取得使用者指定的todo job，將資料包成JSON格式，傳給browser處理
@app.route("/getTodoJob", methods=['GET'])
#使用server side render: template 樣板
def jobJSON():
	jobID = request.args['id']
	dat=DB.getJob(jobID)
	return json.dumps(dat)



#handles login request
@app.route('/login', methods=['POST'])
def login():
	form =request.form
	id = form['ID']
	pwd =form['PWD']
	#validate id/pwd
	if id=='123' and pwd=='456':
		session['loginID']=id
		return redirect("/")
	else:
		session['loginID']=False
		return redirect("/loginForm")
