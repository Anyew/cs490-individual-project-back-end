import mysql.connector

mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd = "Supermariobros.3",
	)

my_cursor = mydb.cursor()

my_cursor.execute("CREATE DATABASE sakila_test")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
	print(db)