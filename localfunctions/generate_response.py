from googlesearch import search
import urllib
from bs4 import BeautifulSoup
from googlesearch import search
from flask import Flask,jsonify
import openai,os
import time

openai.api_key = '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'
# os.getenv("OPENAI_API_KEY")

app = Flask("internal")



def generate_travel_response(para,UserRefTravelFrom,UserRefTravelTo):
    start = time.time()
 
    query='distance between '+UserRefTravelFrom+'to '+UserRefTravelTo+' time duration'
    # websites=search(query,
    #        stop=2)
    #openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=query,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop= [" Human:", " AI:"]
            
        
      )
    #app.logger.info(response)
    urllist=[]
    checklist=[]

    # for i in websites:
      
    #     # #app.logger.info(i)
    #     sitename=i.replace('https://','').split('/')[0].replace('www.','')
    #     # #app.logger.info(sitename)
    #     if sitename not in checklist:
    #       checklist.append(sitename)
    #       urllist.append({
              
    #                     "type": "info",
    #                     "title": sitename ,
                        
    #                     "actionLink": i
    #                   }
              
    #           )
    # #app.logger.info(urllist)


    response_json = jsonify(  fulfillment_messages=[{
      "text": {
          "text": [(response['choices'][0]['text']).replace('\n','')]
          
          
      }
      },
          {
              "payload": {
      "richContent": [
    
     [
              {
                  "type": "chips",
                  "options": [
                     {
                        "text": "Retry"
                    },
                  
                   {
                      "text": "Book Train Ticket"
                  },
                   {
                      "text": "Book Bus Ticket"
                  },
                  {
                      "text": "Main menu"
                  },
                  {
                      "text": "End chat"
                  }
                  ]
              }
              ]
      ]
      }}
      ],
      outputContexts= [
                        {
                            "name": para['session'] + "/contexts/Ticketplace",
                            "lifespanCount": 20,
                            "parameters": {
                                "from": UserRefTravelFrom,
                                'to': UserRefTravelTo
                            }
                        }
                    ]
      )
    end = time.time()
    #app.logger.info((end-start) * 10**3)
   
    return  response_json, ''
    


def generate_food_response(UserRefFood,UserRefPlace):
    start = time.time()
    query='online order ' +UserRefFood + ' in '+UserRefPlace
    websites=search(query, tld="co.in",tbs='0', safe='off', num=10, start=0,
           stop=3, country='', extra_params=None,
           user_agent=None, verify_ssl=True)
    #app.logger.info(websites)
    urllist=[]
    checklist=[]
    # response = openai.Completion.create(
    #     model="text-davinci-003",
    #     prompt=UserRefFood + ' food',
    #     temperature=0.9,
    #     max_tokens=150,
    #     top_p=1,
    #     frequency_penalty=0.0,
    #     presence_penalty=0.6,
    #     stop= [" Human:", " AI:"]
            
        
    #   )
    for i in websites:
        #app.logger.info(i)
        sitename=i.replace('https://','').split('/')[0].replace('www.','')
        #app.logger.info(sitename)
        if sitename not in checklist:
          checklist.append(sitename)
          urllist.append({
              
                        "type": "info",
                        "title": sitename ,
                        "actionLink": i
                      }
              
              )
    #app.logger.info(urllist)


    response_json = jsonify(  fulfillment_messages=[{
      "text": {
          "text": [
          "Please select the website below to order"
          ]
      }
      },
          {
              "payload": {
      "richContent": [
     urllist,
     [
              {
                  "type": "chips",
                  "options": [
                     {
                        "text": "Retry"
                    },
                  {
                      "text": "Main menu"
                  },
                  {
                      "text": "End chat"
                  }
                  ]
              }
              ]
      ]
      }}
      ]
      )
    end = time.time()
    #app.logger.info((end-start) * 10**3)
   
   
    return  response_json, ''
    



def generate_tour_travel_response(para,place,days):
   
    # query=str(days)+' days tour package in '+place
    start = time.time()
    query='top 3 places to vist in '+ place
    # websites=search(query, tld="co.in",tbs='0', safe='off', num=10, start=0,
    #        stop=5, country='', extra_params=None,
    #        user_agent=None, verify_ssl=True)
    # #app.logger.info(websites)
    # urllist=[]
    # checklist=[]
    #openai.api_key = os.getenv("OPENAI_API_KEY")

    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=query,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop= [" Human:", " AI:"]
            
        
      )

    # for i in websites:
      
    #     #app.logger.info(i)
    #     sitename=i.replace('https://','').split('/')[0].replace('www.','')
    #     #app.logger.info(sitename)
    #     if sitename not in checklist:
    #       checklist.append(sitename)
    #       urllist.append({
              
    #                     "type": "info",
    #                     "title": sitename ,
                        
    #                     "actionLink": i
    #                   }
              
    #           )
    # #app.logger.info(urllist)


    response_json = jsonify(  fulfillment_messages=[{
      "text": {
          "text": ['Places to visit in '+place+'.\n'+
          response['choices'][0]['text'].replace('\n','',1)
          ]
      }
      },
          {
              "payload": {
      "richContent": [
     
     [
              {
                  "type": "chips",
                  "options": [
                     {
                        "text": "Retry"
                    },
                    {
                      "text": "Book Trip"
                  },
                  {
                      "text": "Main menu"
                  },
                  {
                      "text": "End chat"
                  }
                  ]
              }
              ]
      ]
      }}
      ],
      outputContexts= [
                        {
                            "name": para['session'] + "/contexts/Tripplace",
                            "lifespanCount": 20,
                            "parameters": {
                                "TripPlace": place,
                                'NoDays': str(days)
                            }
                        }
                    ]
      
      )
    end = time.time()
    #app.logger.info((end-start) * 10**3)
    return  response_json, ''  


def generate_BookTrain_travel_response(place,c):
   
    query='book a Train ticket to travel from '+place+'to '+c
    
    websites=search(query, tld="co.in",tbs='0', safe='off', num=10, start=0,
           stop=5, country='', extra_params=None,
           user_agent=None, verify_ssl=True)
    #app.logger.info(websites)
    urllist=[]
    checklist=[]

    for i in websites:
      
        #app.logger.info(i)
        sitename=i.replace('https://','').split('/')[0].replace('www.','')
        #app.logger.info(sitename)
        if sitename not in checklist:
          checklist.append(sitename)
          urllist.append({
              
                        "type": "info",
                        "title": sitename ,
                        
                        "actionLink": i
                      }
              
              )
    #app.logger.info(urllist)


    response_json = jsonify(  fulfillment_messages=[{
      "text": {
          "text": [
          "Please select the website below to book a ticket"
          ]
      }
      },
          {
              "payload": {
      "richContent": [
     urllist,
     [
              {
                  "type": "chips",
                  "options": [
                     {
                        "text": "Retry"
                    },
                  {
                      "text": "Main menu"
                  },
                  {
                      "text": "End chat"
                  }
                  ]
              }
              ]
      ]
      }}
      ]
      )
   
    return  response_json, ''  


def generate_BookBus_travel_response(place,c):
   
    query='book a bus ticket to travel from '+place+'to '+c
    
    websites=search(query, tld="co.in",tbs='0', safe='off', num=10, start=0,
           stop=5, country='', extra_params=None,
           user_agent=None, verify_ssl=True)
    #app.logger.info(websites)
    urllist=[]
    checklist=[]

    for i in websites:
      
        #app.logger.info(i)
        sitename=i.replace('https://','').split('/')[0].replace('www.','')
        #app.logger.info(sitename)
        if sitename not in checklist:
          checklist.append(sitename)
          urllist.append({
              
                        "type": "info",
                        "title": sitename ,
                        
                        "actionLink": i
                      }
              
              )
    #app.logger.info(urllist)


    response_json = jsonify(  fulfillment_messages=[{
      "text": {
          "text": [
          "Please find the suitable website below"
          ]
      }
      },
          {
              "payload": {
      "richContent": [
     urllist,
     [
              {
                  "type": "chips",
                  "options": [
                     {
                        "text": "Retry"
                    },
                  {
                      "text": "Main menu"
                  },
                  {
                      "text": "End chat"
                  }
                  ]
              }
              ]
      ]
      }}
      ]
      )
   
    return  response_json, ''  



def generate_BooktourTrip_travel_response(place,days):
   
    query=str(days)+' days tour package in '+place
    websites=search(query, tld="co.in",tbs='0', safe='off', num=10, start=0,
           stop=5, country='', extra_params=None,
           user_agent=None, verify_ssl=True)
    #app.logger.info(websites)
    urllist=[]
    checklist=[]

    for i in websites:
      
        #app.logger.info(i)
        sitename=i.replace('https://','').split('/')[0].replace('www.','')
        #app.logger.info(sitename)
        if sitename not in checklist:
          checklist.append(sitename)
          urllist.append({
              
                        "type": "info",
                        "title": sitename ,
                        
                        "actionLink": i
                      }
              
              )
    #app.logger.info(urllist)


    response_json = jsonify(  fulfillment_messages=[{
      "text": {
          "text": [
          "Please select the website below to book a trip"
          ]
      }
      },
          {
              "payload": {
      "richContent": [
     urllist,
     [
              {
                  "type": "chips",
                  "options": [
                     {
                        "text": "Retry"
                    },
                  {
                      "text": "Main menu"
                  },
                  {
                      "text": "End chat"
                  }
                  ]
              }
              ]
      ]
      }}
      ]
      )
   
    return  response_json, ''  

def Generator_quickchat_response(userQuery):
    start = time.time()
 
    query=userQuery
    # websites=search(query,
    #        stop=2)
    #openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=query,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop= [" Human:", " AI:"]
            
        
      )
    #app.logger.info(response)
    
    response_json = jsonify(  fulfillment_messages=[{
      "text": {
          "text": [(response['choices'][0]['text']).replace('\n','',1)]
          
          
      }
      },
          {
              "payload": {
      "richContent": [
    
     [
              {
                  "type": "chips",
                  "options": [
                     {
                        "text": "Retry"
                    },
                  
                   
                  {
                      "text": "Main menu"
                  },
                  {
                      "text": "End chat"
                  }
                  ]
              }
              ]
      ]
      }}
      ]
      
      )
    end = time.time()
    #app.logger.info((end-start) * 10**3)
   
    return  response_json, ''
    
