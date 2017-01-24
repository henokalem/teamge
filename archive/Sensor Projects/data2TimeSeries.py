import requests
import websocket
import csv
import json
import time
import datetime
import sys
from sys import platform as _platform

class SendData():
    def __init__(self):
        self.uaa_uri 		        = 'https://2d172ee0-dc4e-4599-b1df-3c424515270c.predix-uaa.run.aws-usw02-pr.ice.predix.io/oauth/token'
        self.timeseries_ingest_uri 	= 'wss://gateway-predix-data-services.run.aws-usw02-pr.ice.predix.io/v1/stream/messages'
        self.timeseries_query_uri 	= 'https://time-series-store-predix.run.aws-usw02-pr.ice.predix.io/v1/datapoints'
        self.timeseries_zone_id 	= 'c6c65ab7-cd41-4e2d-9b62-a081f08632c8'
        self.client_credentials 	= 'bXZwM19yZWZfYXBwOm12cDNyZWZAcHA='

        self.headers    		= { 'Authorization': 'Basic {0}'.format(self.client_credentials), 
           		                    'Predix-Zone-Id': self.timeseries_zone_id,
           		                    'Content-Type':  'application/x-www-form-urlencoded'}
        self.params                     = { 'client_id':     'mvp3_ref_app', 
           		                    'grant_type':    'client_credentials',
           		                    'client_secret': 'mvp3_ref_app'}
           
        #csvfile	= open('humiture.csv', 'r')
        #jsonfile	= open('payload_output.json', 'w')

    def formatAndSendData(self, obj):
        fieldnames	= ("datetime","sensorid","humidity","temperature")
        messageId	= "PETTMIKE2016"
        assetId		= "compressor-2015"
        tempName	= "PETT-2016:Temperature"
        humidName	= "PETT-2016:Humidity"

        try:
                resp = requests.post(url = self.uaa_uri, headers = self.headers, data = self.params)
                data = resp.json()

                if data['access_token']:
                        client_token = data['access_token']
                        headers      = {'Authorization': 'Bearer {0}'.format(client_token), 'Predix-Zone-Id': self.timeseries_zone_id}
                        ws           = websocket.create_connection(self.timeseries_ingest_uri, header = headers)
                        #reader      = csv.DictReader(csvfile, fieldnames)
                        row = obj.split(',')
                        #print ("r0: ", reader[0])
                        #print ("r1: ", reader[1])
                        #print ("r2: ", reader[2])
                        #print ("r3: ", reader[3])
                        #r0:  07/29/2016 18:13:02
                        #r1:  001
                        #r2:  99104.00
                        #r3:  22.10

                        #for row in reader:
                        #strDT = str(row['datetime'])
                        strDT = str(row[0])
                        print ("strDT: ", strDT)
                        #print ("row-datatime: ", str(row['datetime']))
                        #print ("row-sensorid: ", str(row['sensorid']))
                        #print ("row-humidity: ", str(row['humidity']))
                        #print ("row-temperature: ", str(row['temperature']))

                        if strDT != "0":
                            #row['datetime'] = int(time.mktime(datetime.datetime.strptime(strDT, "%m/%d/%Y %H:%M:%S").timetuple())* 1000)
                            row[0] = int(time.mktime(datetime.datetime.strptime(strDT, "%m/%d/%Y %H:%M:%S").timetuple())* 1000)
			
                            #payload = {"messageId": messageId,"body": [{"name": tempName, "datapoints": [[row['datetime'],row['temperature'],3]], "attributes": {"assetId": assetId, "sensorId": row['sensorid']}},{"name": humidName,"datapoints": [[row['datetime'],row['humidity'],3]],"attributes": {"assetId": assetId, "sensorId": row['sensorid']}}]}
                            payload = {"messageId": row[0],"body": [{"name": tempName, "datapoints": [[row[0],row[3],3]], "attributes": {"assetId": assetId, "sensorId": row[1]}},{"name": humidName,"datapoints": [[row[0],row[2],3]],"attributes": {"assetId": assetId, "sensorId": row[1]}}]}
			    
                            jsonPayload = json.dumps(payload)
                            #jsonfile.write('\n')
			
                            print (jsonPayload)
                            ws.send(jsonPayload)
                            result = ws.recv()
                            print (result)

                            ws.close()
                            #csvfile.close()
                            #jsonfile.close()
                            #f.close()
                else:
                        print("\nNo access token,\nResponse = " + resp)
        except:
	        e = sys.exc_info()[0]
	        f = sys.exc_info()[1]
	
	        print ("\nError: %s" % e)
	        print ("%s" % f)

        return

    def queryTSData(self):
        global timeseries_query_uri
        global headers

        f = open('ts_query.json', 'r')
        query = f.read()
        resp = requests.post(url = timeseries_query_uri, headers = headers, data = query)
	
        print("\n" + str(resp.json()))
        return
