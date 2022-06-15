## Setup

###### Steps

1. Create twilio whatsapp sandbox account by going these https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox?frameUrl=%2Fconsole%2Fsms%2Fwhatsapp%2Fsandbox%3Fx-target-region%3Dus1

2. Install ngrok or localhost.run

Run
```
ngrok http 5000
```

Or

```
ssh -R 80:localhost:8080 nokey@localhost.run
```

3. Add the twilio displayed contact number to your whatsapp

4. Configure WHEN A MESSAGE COMES IN twilio with https://ngrok_url/sms

###### Application run

1. install required dependencies by applying following commands

```
pip3 install -r requirements.txt
```

2. Run your app

```
flask run
```