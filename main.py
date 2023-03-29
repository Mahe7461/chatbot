from flask import Flask,request,make_response,jsonify,render_template,send_from_directory
from localfunctions.generate_response import *
from logging.config import dictConfig


# initialize the flask app 
# app = Flask("internal")
app = Flask(
    __name__,
    # static_url_path='/localfunctions',
    template_folder='./'
)


# default route 
@app.route("/home")
def home():
    resp = make_response(render_template('index.html'))
    return resp

def RedirectToTravel(para):
    return jsonify( followupEventInput= {"name": "TrigGetTravelDetails"}), ''
def RedirectToTourTravel(para):
    return jsonify( followupEventInput= {"name": "TiggTourTravel"}), ''
def RedirectToFood(para):
    return jsonify( followupEventInput= {"name": "TrigFoodReq"}), ''
def RedirectToquickchat(para):
    return jsonify( followupEventInput= {"name": "TrigQuickchatIntent"}), ''


from googlesearch import search
import urllib
from bs4 import BeautifulSoup

def GetTravelDetails(para):
    UserRefTravelFrom=(para.get('queryResult')['parameters']['travelFrom'])
    UserRefTravelTo=(para.get('queryResult')['parameters']['travelTo'])
    return generate_travel_response(para,UserRefTravelFrom,UserRefTravelTo)

def GetFoodDetails(para):
    UserRefFood=(para.get('queryResult')['parameters']['UserFood'])
    UserRefPlace=(para.get('queryResult')['parameters']['Usercity'])
    return generate_food_response(UserRefFood,UserRefPlace)

def GetTourTravelDetails(para):
    place=(para.get('queryResult')['parameters']['place'])
    days=(para.get('queryResult')['parameters']['NoofDays'])
    return generate_tour_travel_response(para,place,days)

def BookTrainTicket(para):
    travelfrom=(para.get('queryResult')['parameters']['from'])
    travelTo=(para.get('queryResult')['parameters']['to'])

    return generate_BookTrain_travel_response(travelfrom,travelTo)


def BookBusTicket(para):
    travelfrom=(para.get('queryResult')['parameters']['from'])
    travelTo=(para.get('queryResult')['parameters']['to'])


    return generate_BookBus_travel_response(travelfrom,travelTo)


def BookTripIntent(para):
    tripPlace=(para.get('queryResult')['parameters']['tripPlace'])
    NoDays=(para.get('queryResult')['parameters']['NoDays'])


    return generate_BooktourTrip_travel_response(tripPlace,NoDays)

def Getquickchat(para):
    userQuery=(para.get('queryResult')['parameters']['userQuery'])
    


    return Generator_quickchat_response(userQuery)    

HANDLERS={    
    
    # "ServiceTrackingTiggerIntent": ServiceTrackingTiggerIntent
    # 'TravelRequestTiggerIntent':RedirectToTravel,
    'TravelRequestDefaultIntent':GetTravelDetails,
    'TravelRequestRetryIntent':RedirectToTravel,
    'TravelTourDefaultRetryIntent':RedirectToTravel,
    'TravelTourDefaultIntent':GetTourTravelDetails,
    'BookingTrainTicket':BookTrainTicket,
    'BookBusTicket':BookBusTicket,
    'BookTripIntent':BookTripIntent,
    'FoodRequestTiggerIntent':RedirectToFood,
    'FoodRequestRetryIntent':RedirectToFood,
    'FoodRequestDefaultIntent': GetFoodDetails,
    'quickchatDefaultIntent':Getquickchat,
    'quickchatRetryIntent':RedirectToquickchat

    
}


# create a route for webhook 
@app.route('/webhook', methods=['GET', 'POST']) 
def webhook(request): 
# def webhook(): 
    try:
        req=request.get_json(force=True)
        action= req.get('queryResult').get('intent')['displayName']
        handler = HANDLERS.get(action)
        # #app.logger.info(req)
        #app.logger.info('Intent name: '+str(action))
    
        user_res=(req['queryResult']['queryText'])
        ses=req['session']
        sessionId=ses.split('sessions/')[-1]

        if handler:
            #app.logger.info('Triggered function name: '+str(handler))
            # user_details,IsUserLogIn=get_username(req)
            # username=user_details['username']
            # mailId=user_details['mailId']
            res,bot_res=handler(req)
            # user_res=(req['queryResult']['queryText'])
            # ses=req['session']
            # sessionId=ses.split('sessions/')[-1]
            return res
        else:
            bot_res=(req['queryResult']['fulfillmentText'])
            ses=req['session']
            sessionId=ses.split('sessions/')[-1]
            return make_response(jsonify({'fulfillmentText': None})) 
    except  Exception as e:
        #app.logger.info(e)
        return make_response(jsonify({'fulfillmentText': None})) 



if __name__ == '__main__': 
    import logging
    logFormatStr = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
    logging.basicConfig(format = logFormatStr, filename = "AHK_chatbot_log.log", level=logging.DEBUG)
    formatter = logging.Formatter(logFormatStr,'%m-%d %H:%M:%S')
    fileHandler = logging.FileHandler("AHK_chatbot_log.log")
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.DEBUG)
    streamHandler.setFormatter(formatter)
    #app.logger.addHandler(fileHandler)
    #app.logger.addHandler(streamHandler)
    #app.logger.info("Logging is set up.")
    app.run(host='0.0.0.0', port=5000)
	
	


	





