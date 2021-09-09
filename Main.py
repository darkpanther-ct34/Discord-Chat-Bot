import torch
import os
import random
import discord
from model import NeuralNet
from nltkFunc import bagofwords, tokenize
from dotenv import load_dotenv
import json
# from discord.ext import commands
from reddit import display_meme, display_cursed_image, display_art, display_joke

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('data.json', 'r') as f:
    intents = json.load(f)

FILE = "data.pth"
data = torch.load(FILE)

inputSize = data["inputSize"]
hiddenSize = data["hiddenSize"]
outputSize = data["outputSize"]
allWords = data["allWords"]
tags = data["tags"]
modelState = data["modelState"]

model = NeuralNet(inputSize, hiddenSize, outputSize).to(device)
model.load_state_dict(modelState)
model.eval()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()


def write_json(datatwo, filename='missedMessages.json'):
    with open(filename, 'w') as fi:
        json.dump(datatwo, fi, indent=4)


lastEvent = ""


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_message(message):
    global lastEvent
    if message.author == client.user:
        return
    print(f'{message.author}: {message.content}')
    sentance = tokenize(message.content)
    x = bagofwords(sentance, allWords)
    x = x.reshape(1, x.shape[0])
    x = torch.from_numpy(x)

    output = model(x)

    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.85:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                response = random.choice(intent["responses"])
                if response == "meme":
                    meme = []
                    lastEvent = "meme"
                    send = display_meme(meme)
                    await message.channel.send(embed=send)
                elif response == "cursed image":
                    cursedimage = []
                    lastEvent = "cursed image"
                    send = display_cursed_image(cursedimage)
                    await message.channel.send(embed=send)
                elif response == "art":
                    art = []
                    lastEvent = "art"
                    send = display_art(art)
                    await message.channel.send(embed=send)
                elif response == "roll":
                    lastEvent = "roll"
                    dice = str(random.choice(range(1, 21)))
                    embedvar = discord.Embed(title="Dice Roll",
                                             description="I rolled a dice with twenty sides and got %s." % dice,
                                             color=0x206EEF)
                    await message.channel.send(embed=embedvar)
                elif response == "joke":
                    joke = []
                    lastEvent = "joke"
                    send = display_joke(joke)
                    await message.channel.send(embed=send)
                elif response == "help":
                    embedvar = discord.Embed(title="Meme Function",
                                             description="The Meme Function shows you a credited meme.",
                                             color=0xEF2051)
                    embedvar.add_field(name="Cursed Image Function",
                                       value="The Cursed Image Function shows you a cursed image.", inline=False)
                    embedvar.add_field(name="Art Function",
                                       value="The Art Function shows you a credited piece of art.", inline=False)
                    embedvar.add_field(name="Roll Function",
                                       value="The Roll Function rolls a dice and tells you the result.", inline=False)
                    embedvar.add_field(name="Joke Function",
                                       value="The Joke Function tells you a credited joke.", inline=False)
                    embedvar.set_author(name="Help Menu")
                    lastEvent = "help"
                    await message.channel.send(embed=embedvar)
                elif response == "repeat":
                    if lastEvent == "meme":
                        meme = []
                        lastEvent = "meme"
                        send = display_meme(meme)
                        await message.channel.send(embed=send)
                    elif lastEvent == "cursed image":
                        cursedimage = []
                        lastEvent = "cursed image"
                        send = display_cursed_image(cursedimage)
                        await message.channel.send(embed=send)
                    elif lastEvent == "art":
                        art = []
                        lastEvent = "art"
                        send = display_art(art)
                        await message.channel.send(embed=send)
                    elif lastEvent == "roll":
                        lastEvent = "roll"
                        dice = str(random.choice(range(1, 21)))
                        embedvar = discord.Embed(title="Dice Roll",
                                                 description="I rolled a dice with twenty sides and got %s." % dice,
                                                 color=0x206EEF)
                        await message.channel.send(embed=embedvar)
                    elif lastEvent == "joke":
                        joke = []
                        lastEvent = "joke"
                        send = display_joke(joke)
                        await message.channel.send(embed=send)
                    elif lastEvent == "help":
                        embedvar = discord.Embed(title="Meme Function",
                                                 description="The Meme Function shows you a credited meme.",
                                                 color=0xEF2051)
                        embedvar.add_field(name="Cursed Image Function",
                                           value="The Cursed Image Function shows you a cursed image.", inline=False)
                        embedvar.add_field(name="Art Function",
                                           value="The Art Function shows you a credited piece of art.", inline=False)
                        embedvar.add_field(name="Roll Function",
                                           value="The Roll Function rolls a dice and tells you the result.",
                                           inline=False)
                        embedvar.add_field(name="Joke Function",
                                           value="The Joke Function tells you a credited joke.", inline=False)
                        embedvar.set_author(name="Help Menu")
                        lastEvent = "help"
                        await message.channel.send(embed=embedvar)
                    else:
                        didnotlastevent = [
                            "I didn't do anything last time :(",
                            "Do what again?",
                            "Repeat what?",
                            "What do you want me to repeat?"
                            ]
                        goingtosend = random.choice(didnotlastevent)
                        await message.channel.send(goingtosend)
                elif message.content.lower() == "hello there":
                    await message.channel.send("General Kenobi")
                    lastEvent = ""
                else:
                    await message.channel.send(response)
                    lastEvent = ""
    else:
        with open('missedMessages.json') as json_file:
            datatwo = json.load(json_file)
        datatwo["DidNotUnderstand"].append(message.content)
        write_json(datatwo)
        await message.channel.send("I dont understand...")


"""
print("Let's chat! type 'quit' to exit")
while True:
    sentance = input("You: ")
    if sentance.lower() == "quit":
        break
    sentance = tokenize(sentance)
    x = bagOfWords(sentance, allWords)
    x = x.reshape(1, x.shape[0])
    x = torch.from_numpy(x)

    output = model(x)

    _, predicted = torch.max(output, dim = 1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim = 1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.9:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                print(f' {random.choice(intent["responses"])}')
    else:
        print(f' I do not understand..')"""


client.run(TOKEN)
