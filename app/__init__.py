


from flask import Flask
app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'
from app import bot
from app import aadhar
from app import example
from app import sample