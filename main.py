# import the opencv library
import cv2
import datetime
import time
from os.path import exists
import discord
from discord.ext import commands
import os
import asyncio
import sys
def makeFolder():
    username = os.getlogin()
    if(os.path.exists("/Users/"+username+"/Documents/TooReal")):
        pass
    else:
        os.makedirs("/Users/"+username+"/Documents/TooReal")
makeFolder()
username = os.getlogin()
pathToPictures = "/Users/"+username+"/Documents/TooReal/"
def isPictureTaken():
    tod = datetime.datetime.today().strftime("%b-%d-%Y")
    return exists(pathToPictures+tod+".png")
def takePicture():
    cam_port = 0
    cam = cv2.VideoCapture(cam_port)
    time.sleep(0.1)
    # reading the input using the camera
    result, image = cam.read()

    # If image will detected without any error, 
    # show result
    if result:
        tod = datetime.datetime.today().strftime("%b-%d-%Y")
        # saving image in local storage
        cv2.imwrite(pathToPictures+tod+".png", image)
    
    # If captured image is corrupted, moving to else part
    else:
        print("No image detected. Please! try again")
def getPictureTime():
    today = datetime.datetime.today()
    date_int = int(today.strftime('%d%m'))*17
    date_int_alt = int(today.strftime('%d%Y'))*7
    targ_hour = (date_int % 12) + 9
    targ_min = date_int_alt % 60
    targ_sec = 0
    return datetime.datetime.now().replace(hour=targ_hour, minute=targ_min, second=targ_sec)
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
discordBotKey = 'insertYourKeyHere'
discordChannelID = 000 # put in your own discord channel here!
@bot.event
async def on_ready():
    print('Bot is online')
    channel = bot.get_channel(discordChannelID)
    target = getPictureTime()
    time_difference = (target - datetime.datetime.now()).total_seconds()
    if(time_difference>0):
        print("It's not time to be TooReal! Waiting.")
        await asyncio.sleep(time_difference)
    takePicture()
    tod = datetime.datetime.today().strftime("%b-%d-%Y")
    with open(pathToPictures+tod+".png", "rb") as image:
        file = discord.File(image, pathToPictures+tod+".png")
        await channel.send("It's time to be TooReal! Here is "+username+" right now:")
        await channel.send(file=file)
    print("You have now been real!")
    sys.exit()
if isPictureTaken():
    print("You have already been real!")
    sys.exit()
else:
    # run the bot. in the bot, we do this below.
    bot.run(discordBotKey)
