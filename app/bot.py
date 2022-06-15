from app import app
from flask import request, session, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import re
import datetime
from time import sleep
from dateutil.parser import *


order_details = {"id": "abcsdsad76ub767b77v", "mobile": "918341140401",
                 "itemName": "Oneplus 9R", "amount": 45000, "status": "Inprogress"}


@app.before_first_request
def _run_on_start():
    if session.get('status_index'):
        session.pop('status_index')
    if session.get('date'):
        session.pop('date')
    if session.get('orderPosition'):
        session.pop('orderPosition')
    return ""

@app.route("/sms", methods=['POST'])
def sms_reply():


    # Get the message from form
    msg = request.form.get('Body').lower()

    print(request.form)
    print("message received "+msg)

    allowedString = 'Unable to understand your query\nPlease send us below keywords for better serve\n\n1. hi or hello\n2. status or order status\n3. order details or details or detail'

    if not session.get('delivered_at'):
        session['delivered_at']=''

    resp = MessagingResponse()
    hiHello = ["hi", "hello"]
    order = ["status", "order status"]
    orderMatch = ["order details", "details", "detail"]
    cancelOrder = ["cancel my order", "cancel","cancell","cancel my current order"]

    status_array=['Inprocess', 'On the way', 'At your door step','Delivered on {}'.format(session.get('delivered_at'))]
    order_status=''
    order_date=''
    
    orderPosition = ''

    if not session.get('orderPosition'):
        session['orderPosition']=''

    print("orderPosition===> "+ session['orderPosition'])
    if session['orderPosition'] == 'cancelled':
        resp.message("Hello Mr.{} Your order has been cancelled you can make a new order".format(request.form.get('ProfileName')))
    elif any(x in msg for x in hiHello):
        session['orderPosition'] = 'hiHello'
        resp.message("Hello Mr.{} How can I help you".format(request.form.get('ProfileName')))

    elif any(x in msg for x in order):
        session['orderPosition'] = 'status'
        # print("-----> ", str(session['date']))

        if not session.get('date'):
            session['date']=datetime.datetime.now()
        
        if not session.get('status_index'):
            session['status_index']=0

        
        print("startDate "+str(session['date']))
        now=datetime.datetime.now()
        print("now ", str(now))
        minutes=dateTimeDiffIn(session.get('date'), datetime.datetime.now())
        print("minutes ", minutes)
        
        if(minutes>=1):
            
            session['status_index']=session['status_index']+1
            session['date']=datetime.datetime.now()
        else:
            print("!=")

        if(session['status_index']>=3):
            session['delivered_at']=datetime.datetime.now()

        print("status_index", session['status_index'])
        resp.message("Hello Mr.{} Your Order id is {} is {}. We will let you know the status of the current order".format(
            request.form.get('ProfileName'), order_details['id'],status_array[session['status_index']] if session['status_index'] else status_array[0]))

    elif any(x in msg for x in orderMatch):
        session['orderPosition'] = 'details'

        resp.message("Hello Mr.{}\nYour order details are\nOrder Id: {}\nItem: {}\nAmount: {}\nStatus: {}".format(request.form.get(
            'ProfileName'), order_details['id'], order_details['itemName'], order_details['amount'], order_details['status']))
        
        session['date']=datetime.datetime.now()

    elif any(x in msg for x in cancelOrder):
        session['orderPosition'] = 'cancelled'
        resp.message("Hello Mr.{} Your Order {} has been cancelled.".format(request.form.get('ProfileName'), order_details['id']))
    else:
        session['orderPosition'] = 'notUnderstand'
        print("Unable to understand your query")
        resp.message(allowedString)

    print('orderPosition {}'.format(session['orderPosition']))
    return str(resp)

def dateTimeDiffIn(start_date, end_date):
    diff = end_date.replace(tzinfo=None)  - start_date.replace(tzinfo=None) 
    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return minutes
