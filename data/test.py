from data import db_session
from data.books import Book
from flask import send_from_directory
from requests import delete, get, post
import os

os.chdir('C:/Users')
listdir = os.listdir()
uselessdir = ['All Users', 'Default', 'Default User', 'desktop.ini', 'Public', 'Все пользователи']
for elem in uselessdir:
    del listdir[listdir.index(elem)]
os.chdir(f'C:/Users/{listdir[0]}/Downloads')
print(os.getcwd())
print(os.listdir())



print(get('http://localhost:5000/api/book/1').json())


