#!/usr/local/bin/python
# Connect to MariaDB Platform
import mysql.connector #mariadb

try:
	#連線DB
	conn = mysql.connector.connect(
		user="root",
		password="",
		host="localhost",
		port=3306,
		database="test"
	)
	#建立執行SQL指令用之cursor, 設定傳回dictionary型態的查詢結果 [{'欄位名':值, ...}, ...]
	cursor=conn.cursor(dictionary=True)
except mysql.connector.Error as e: # mariadb.Error as e:
	print(e)
	print("Error connecting to DB")
	exit(1)


def add(data):
	sql="insert into todo (jobName,jobContent) VALUES (%s,%s);"
	param=(data['jobName'],data['jobContent'])
	cursor.execute(sql,param)
	conn.commit()
	return
	
def delete(id):
	sql="delete from todo where id=%s;"
	cursor.execute(sql,(id,))
	conn.commit()
	return

def update(id,data):
	sql="update todo set jobName=%s,jobContent=%s where id=%s;"
	param=(data['jobName'],data['jobContent'],id)
	cursor.execute(sql,param)
	conn.commit()
	return
	
def getList():
	sql="select * from todo;"
	#param=('值',...)
	cursor.execute(sql)
	return cursor.fetchall()

def checkLogin(id,pwd):
	sql="select role, id,name from user where id=%s and pwd=%s;"
	cursor.execute(sql,(id,pwd))
	rs=cursor.fetchone()
	return rs
	
	