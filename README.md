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
 
3. Create an order run from postman

curl --location --request POST 'http://localhost:4999/place-order' \
--header 'Content-Type: application/json' \
--header 'Cookie: session=.eJxFUF1vwjAM_CtWXldQ0m_6xgZDSOtAsMdJKDTWiNQmVZJuQ4j_PleM7c2-O9vnuzCFrf5Eh-ogA6sYi5g1SIUYK6fQHRQGqVvPqguTnR0MydKMcx4xJcMojXkcT3g-ESWIuEqSSmRTkZdlkdIOHbBboG-c7oO2huQbg9t28DDbwdwoZ7UC30kX-hNdnhJm6EiDCmrpgHaLKTyjDINDD_k0y96HmCcJKO37Vp4j2BvZKyc_rIGy4JCtoDnp3mOIYPQJ3fwERxkCOhLHWQ6rR_DB0gRGZHhsd_P61-qr7PDmsb95JLyzR92O6MNMlEkqRMpT_pfPWhGT8EzEcZHO0pIXfPy7l-cOTaitGicbClgHaKRT_9w-0FeUK3va1NuX5dtyQZy_g2sDvbMNes-ud_igjcJvVlH24cuO0bPrD2KdiOI.Yq14tA.H_CWW1NOo5ErPZ8r3RZBbYzcN4M' \
--data-raw '{
    "mobile": "+918341140401",
    "itemName": "Oneplus 9R",
    "amount": 45000,
    "itemDescription":"OnePlus 9R Android smartphone. Announced Mar 2021. Features 6.55″ display, Snapdragon 870 5G chipset, 4500 mAh battery, 256 GB storage, 12 GB RAM"
}'

4. In bot.py update the twilio access key and auth key of yours