from app import app
from flask import request, session, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import re
import datetime
from time import sleep
from dateutil.parser import *
import uuid
import json
from twilio.rest import Client

import redis

redis = redis.Redis(
     host= 'localhost',
     port= '6379')

@app.before_first_request
def _run_on_start():
    print("before_first_request............")
    if session.get('status_index'):
        session.pop('status_index')
    if session.get('date'):
        session.pop('date')
    if session.get('orderPosition'):
        session.pop('orderPosition')
    if session.get('order_details'):
        session.pop('order_details')
    if(session.get('flag')):
        session.pop('flag')
    if(redis.get('order_details')):
        redis.delete('order_details')
    if(redis.get('flag')):
        redis.delete('flag')
    return ""

@app.route("/sample", methods=['GET','POST'])
def sample():
    print("request ")
    return jsonify({"message":"success"})

@app.route("/place-order", methods=['POST'])
def place_order():
    order_id=str(uuid.uuid4().int)[:15]
    body=json.loads(request.data)
    
    body['orderId']=order_id
    body['status']='In process'
    body['paymentMode']='credit card'
    body['paymentStatus']='COMPLETED'

    body['date']=str(datetime.datetime.now())
    redis.set('order_details', json.dumps(body))
    session['order_details']=body
    session['one']='1'
    order_response={}
    order_response['message']='Your order has been placed successfully'
    order_response['orderId']=body['orderId']
    order_response['orderDetails']=body
    sendWhatsappMessage(body)
    return jsonify(order_response)
    # return jsonify({"message":"Your Order has been placed successfully","orderId":body["orderId"]}),200


@app.route("/sms", methods=['POST'])
def sms_reply():

    resp = MessagingResponse()

    if redis.get('order_details') is None:
        resp.message("No orders found please make an order first")
        return str(resp)

    order_details=json.loads(redis.get('order_details'))

    print("aaaaaa ", order_details['status'])
    if(order_details['status']=='cancelled'):
        resp.message(f"Your Refund of order Id {order_details['orderId']} and amount {order_details['amount']} has been initiated on {order_details['date']} and It will be credited to you by 2 days in source account")
        return str(resp)

    print(order_details)
    # Get the message from form
    msg = request.form.get('Body').lower()

    print(request.form)
    print("message received "+msg)

    allowedString = 'Unable to understand your query\nPlease send us below keywords for better serve\n\n1. hi or hello\n2. status or order status\n3. order details or details or detail\n4.cancel my order or cancel or cancell or cancel my current order'

    if not session.get('delivered_at'):
        session['delivered_at']=''

    hiHello = ["hi", "hello"]
    order = ["status", "order status"]
    orderMatch = ["order details", "details", "detail"]
    cancelOrder = ["cancel my order", "cancel","cancell","cancel my current order","1","2","3"]

    status_array=['Inprocess', 'On the way', 'At your door step','Delivered on {}'.format(session.get('delivered_at'))]
    order_status=''
    order_date=''
    
    orderPosition = ''

    if not session.get('orderPosition'):
        session['orderPosition']=''

    print("orderPosition===> "+ session['orderPosition'])

    if any(x in msg for x in hiHello):
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
            request.form.get('ProfileName'), order_details['orderId'],status_array[session['status_index']] if session['status_index'] else status_array[0]))

    elif any(x in msg for x in orderMatch):
        session['orderPosition'] = 'details'

        resp.message("Hello Mr.{}\nYour order details are\nOrder Id: {}\nItem: {}\nDescription: {}\nAmount: {}\nStatus: {}".format(request.form.get(
            'ProfileName'), order_details['orderId'], order_details['itemName'],order_details['itemDescription'], order_details['amount'], order_details['status']))
        
        session['date']=datetime.datetime.now()

    elif any(x in msg for x in cancelOrder):
        session['orderPosition'] = 'cancelled'
        print("asssssss ", session.get('flag'))
        if(redis.get('flag') is None):
            reasongMsgs='Please select the reason for cancalletaion.\n1. Damaged\n2. Not fit\n3. Shipping address Changed'
            redis.set('flag','Some')
            resp.message(reasongMsgs)
        else:
            resp.message("Hello Mr.{} Your Order {} has been cancelled.".format(request.form.get('ProfileName'), order_details['orderId']))
            order_details['status']='cancelled'
            redis.set('order_details', json.dumps(order_details))
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


def sendWhatsappMessage(body):

    try:
        client = Client('ACd78e07066a3ae2422dfa53af9272d269', '4c1a08623659cb741d1df2219d539e11')
        message = client.messages.create(
                              from_='whatsapp:+14155238886',
                              body="Your order Id {} has been placed successfully on {} and it's in {} and We will let you know the status".format(body['orderId'],str(body['date']),body['status']),
                              to='whatsapp:{}'.format(body['mobile'])
                          )
        return "success"
    except Exception as e:
        raise Exception(str(e))

@app.errorhandler(Exception)
def exception_handler(e):
    return jsonify({'message': str(e)}), 400


        