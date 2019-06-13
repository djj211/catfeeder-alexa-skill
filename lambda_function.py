import urllib2, base64, json
from datetime import datetime

def lambda_handler(event, context):
    username = ""
    password = ""
    baseUrl = ""
    alexaResponse = ""
    intent = "FeedCats"
    
    try:
        intent = event['request']['intent']['name']
    except:
        intent = "FeedCats"
        
    if intent == "LastFeed":
        jsonStr = {}
        data = json.dumps(jsonStr)
        
        request = urllib2.Request(baseUrl + "time", data, {'Content-Type': 'application/json'})
        base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        
        result = urllib2.urlopen(request)
        
        response = result.read()
        
        result.close()
        
        retJson = json.loads(response)
        lastFeed = retJson['date']

        lastFeedDate = datetime.strptime(lastFeed, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
        lastFeedTime = datetime.strptime(lastFeed, "%Y-%m-%d %H:%M:%S").strftime("%I:%M %p")
        
        alexaResponse = "The Cats were last fed on " + lastFeedDate + " at " + lastFeedTime
        
    else:
        feedTime = "4"

        try:
            feedTime = event['request']['intent']['slots']['seconds']['value']
        except:
            feedTime = "4"
            
        jsonStr = {'time':feedTime}
        data = json.dumps(jsonStr)
        
        request = urllib2.Request(baseUrl + "feed", data, {'Content-Type': 'application/json'})
        base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        
        result = urllib2.urlopen(request)
        
        response = result.read()
        
        result.close()
        
        retJson = json.loads(response)

        alexaResponse = "Cat Feed Complete"
        
        if retJson['result'] != "OK":
            alexaResponse = retJson['result']

    return {
     	"version": "1.0",
    	"response": {
    	"outputSpeech": {
    	  "type": "PlainText",
    	  "text": alexaResponse
    	},
    	"card": {
    	  "content": alexaResponse,
    	  "title": "Cat Feeder",
    	  "type": "Simple"
    	},
    	"reprompt": {
    	  "outputSpeech": {
    		"type": "PlainText",
    		"text": ""
    	  }
    	},
    	"shouldEndSession": True
    	},
    	"sessionAttributes": {}   
    }

