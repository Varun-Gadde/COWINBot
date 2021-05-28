import discord
import requests
import json
from requests import sessions
from fake_useragent import UserAgent
import pprint
from pygame import mixer
from datetime import datetime, timedelta
import time
from discord.ext import commands

temp_user_agent = UserAgent()
browser_header = {'User-Agent': temp_user_agent.random}


def dictToString(dict):
  return str(dict).replace(', ','\r\n').replace("u'","").replace("'","").replace("{","").replace("]","").replace("}","").replace("[","").replace('"',"")[1:-1]
client = commands.Bot(command_prefix='.')

@client.command()
async def findvaccine(ctx, pincode, date):
  if pincode and date:
    url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode='
    newUrl = (url +  pincode + "&" + 'date=' + date)

    r = requests.get(newUrl, headers=browser_header)

    data = r.json()
    
    completedData = dictToString(json.dumps(data, indent=4, sort_keys=True))
    embed=discord.Embed(title="Vaccine Availablility", url="", description=completedData, color=0xFF5733)
    await ctx.send(embed=embed)
  else:
    await ctx.send("You must send the proper parameters, for example .findvaccine 500010 31-7-21")



@client.command()
async def searchforvaccines(ctx,pincode,age,num_days):
  age = int(age)
  pincodes = []
  pincodes.append(pincode)
  num_days = int(num_days)

  print_flag = 'Y'

  await ctx.send("Starting search for Covid vaccine slots!")

  actual = datetime.today()
  list_format = [actual + timedelta(days=i) for i in range(num_days)]
  actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]

  while True:
      counter = 0   

      for pincode in pincodes:   
          for given_date in actual_dates:

              URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pincode, given_date)
              header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} 
              
              result = requests.get(URL, headers=header)

              if result.ok:
                  response_json = result.json()
                  if response_json["centers"]:
                      if(print_flag.lower() =='y'):
                          for center in response_json["centers"]:
                              for session in center["sessions"]:
                                  if (session["min_age_limit"] <= age and session["available_capacity"] > 0 ) :
                                      

                                      
                                      await ctx.send('Pincode: ' + pincode)
                                      time.sleep(0.5)
                                      await ctx.send("Available on: {}".format(given_date))
                                      time.sleep(0.5)
                                      await ctx.send("Center name: " + center["name"])
                                      time.sleep(0.5)
                                      await ctx.send("Block name: " + center["block_name"])
                                      time.sleep(0.5)
                                      await ctx.send("Price: " +  center["fee_type"])
                                      time.sleep(0.5)
                                      await ctx.send("Availablity : " + session["available_capacity"])
                                      time.sleep(0.5)

                                      if(session["vaccine"] != ''):
                                          print("\t Vaccine type: ", session["vaccine"])
                                      print("\n")
                                      counter = counter + 1
              else:
                  await ctx.send("No Response!")
                  
      if counter:
          await ctx.send("No Vaccination slot available!")
      else:
        
          await ctx.send("Search Completed!")

      dt = datetime.now() + timedelta(minutes=3)

      while datetime.now() < dt:
          time.sleep(1)


client.run('your token here')



