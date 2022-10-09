import discord
import random
import asyncio
import json
import math
import pytz
from discord.utils import get

from datetime import datetime
from datetime import date

# from azure.core.credentials import AzureKeyCredential
# from azure.ai.textanalytics import TextAnalyticsClient

client = discord.Client(intents=discord.Intents.all())

azureKey = ""
timeGap = 60

async def giveWeeklyWinner(winnerID):
    f = open("lastWinner.txt", "r")
    lastWinner = f.read()
    f.close()
    member2 = get(client.get_all_members(), id=int(lastWinner))
    role = get(member2.guild.roles, name='LAST WEEKS WINNER')
    await member2.remove_roles(role)
  
    member = get(client.get_all_members(), id=int(winnerID))
    
    await member.add_roles(role)
    f = open("lastWinner.txt", "w")
    f.write(f"{winnerID}")
    f.close()


  
def genWeekly(mapping):
    s = "The weekly leaderboard is as follows: \n"
    people = []
    for id in mapping:
        if mapping[id] != []:
            activity = mapping[id][0] - mapping[id][2]
        people.append([activity, int(id)])
    people = sorted(people, reverse=True)
    i  = 0
    best = 0
    for person in people:
        if i ==0:
          best = person[1]
        num = "{:.2f}".format(math.sqrt(person[0]))
        temp = f"<@{person[1]}> with a activity measure of {num} \n"
        s += temp
        i += 1

    return s, best


def genLeaderboard(mapping):
    s = "The all time leaderboard is as follows: \n"
    people = []
    for id in mapping:
        if mapping[id] != []:
            activity = mapping[id][0]
            people.append([activity, int(id)])
    people = sorted(people, reverse=True)
    for person in people:
        if person[0] == 0:
            break

        num = "{:.2f}".format(math.sqrt(person[0]))
        temp = f"<@{person[1]}> with a activity measure of {num} \n"
        s += temp

    return s


def getMessageValue(currTime, lastTime):
    deltaTime = abs(lastTime - currTime)
    if deltaTime > 2:
        deltaTime += 0.05

    if deltaTime < timeGap:

        return max(deltaTime / timeGap, 0.01)
    else:
        return 1


async def checkIfNewDay():
    f = open("lastDate.txt", "r")
    s = f.read()
    f.close()

    utc_now = pytz.utc.localize(datetime.utcnow())
    pst_now = utc_now.astimezone(pytz.timezone("America/Los_Angeles"))
    currentDateString = pst_now.strftime('%m-%d')

    if (s != currentDateString):
        print("last date: " + s + ", today: " + currentDateString +
              ", today time:" + str(pst_now.hour))
        channel = client.get_channel(224198577033838592)

        s = currentDateString

        f = open("lastDate.txt", "w")
        f.write(f"{s}")
        f.close()

        f = open("birthdays.json", "r")
        birthdays = json.load(f)
        f.close()

        day = pst_now.strftime("%d")
        month = getMonth2(pst_now.strftime("%b"))
        print("Today is " + str(day) + " " + str(month))
        #check if birthday exists
        for x in birthdays:
            print(str(x['day']) + " " + str(x['month']))
            if (x['day'] == int(day) and x['month'] == int(month)):
                print("found")
                await channel.send('Happy birthday ' + x['name'] + '!!!')


async def everySecond():
    while True:
        day = date.today().weekday()
        hour = datetime.now().hour
        minute = datetime.now().minute
        channel = client.get_channel(224198577033838592)

        generalVoice = client.get_channel(671465043354976260)
        generalVoice2 = client.get_channel(669689207467409418)
        f = open("activityMessages.json", "r")
        activityMessages = json.load(f)
        f.close()

        if (day == 1 and hour == 9 and minute == 5):  # resets
            # print leaderboard
            
            await channel.send(
                "resseting weekly activity! the scores are as follows:")
            s, best = genWeekly(activityMessages)
            await channel.send(s)
            for key in activityMessages:
                activityMessages[key][2] = activityMessages[key][0]
            await giveWeeklyWinner(int(best))
            
        if (len(generalVoice.members) > 1):
          for mem in generalVoice.members:
              id = str(mem.id)
              # print("doing")
              # print(activityMessages)
              if id in activityMessages:
                  # print(f"old activty is {activityMessages[id][0]}")
                  activityMessages[id][0] += 0.025
                  # print(f"new activty is {activityMessages[id][0]}")
        if (len(generalVoice2.members) > 1):
          for mem in generalVoice2.members:
              id = str(mem.id)
              # print("doing")
              # print(activityMessages)
              if id in activityMessages:
                  # print(f"old activty is {activityMessages[id][0]}")
                  activityMessages[id][0] += 0.025
                  # print(f"new activty is {activityMessages[id][0]}")
        f = open("activityMessages.json", "w")
        json.dump(activityMessages, f)
        f.close()
        goodDay = random.choice(range(1, 100000))

        if goodDay == 8458:
            await channel.send("@everyone How has your day been?")

        await checkIfNewDay()
        await asyncio.sleep(60)


@client.event
async def on_ready():
    client.loop.create_task(everySecond())
    print('We have logged in as {0.user}'.format(client))


@client.event
# add everything in here!!!!!

# connors id: 224039480921686016
async def on_message(message):
    badWords = {
        "fuck": "f-word",
        "shit": "s-word",
        "cunt": "c-word",
        "bitch": "b-word",
        "whore": "w-word",
        "valorant": "v-word",
        "penis": "p-word",
        "deez nuts": "d-words"
    }

    if message.author == client.user:
        return
    # if message.content == "give me admin":
    #     member = message.author
    #     role = get(member.guild.roles, name='LAST WEEKS WINNER')
    #     await member.add_roles(role)

  
    if '$hello' in message.content.lower():
        await message.channel.send('Hello!')

    if '$swap' in message.content.lower():
        await giveWeeklyWinner(290242931221331969)
    if '$help' in message.content.lower():
        f = open("help.txt", "r")
        s = f.read()
        f.close()
        await message.channel.send(s)\

    if '$outro' in message.content.lower():
        channel = client.get_channel(363829704224145408)
        s = "/stop"
        s2 = "/play https://www.youtube.com/watch?v=FX9eEhoRZhY"
        await channel.send(s)
        await channel.send(s2)
    if message.content.startswith('$connor'):
        await message.channel.send('hello there my BRB')
    if '$tom' in message.content.lower():
        await message.channel.send('hello there my creator')
    id = f"{message.author.id}"

    f = open("activityMessages.json", "r")
    activityMessages = json.load(f)
    f.close()

    if "$trackme" in message.content.lower():
        f = open("activityMessages.json", "r")
        activityMessages = json.load(f)
        f.close()
        if id not in activityMessages:
            activityMessages[id] = [0, 0, 0]
            await message.channel.send("You are being tracked...")
        else:
            await message.channel.send("I'm already watching you...")

    if "$weeklyactivity" in message.content.lower():
        s,best = genWeekly(activityMessages)
        await message.channel.send(s)

    if "$alltimeactivity" in message.content.lower():
        s = genLeaderboard(activityMessages)
        await message.channel.send(s)
##########

    if id in activityMessages:

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        ll = current_time.split(":")
        time = 0
        for i in range(3):
            if i == 0:
                time += int(ll[0]) * 60
            elif i == 1:
                time += int(ll[1])
            else:
                time += int(ll[2]) / 60

        if activityMessages[id] == []:
            activityMessages[id] = [1, time, 0]
        else:
            activityMessages[id][0] += getMessageValue(time,
                                                       activityMessages[id][1])
            activityMessages[id][1] = time

        f = open("activityMessages.json", "w")
        json.dump(activityMessages, f)
        f.close()
###################

    if '$doghouse' in message.content.lower():
        f = open("dogHouse.txt", "r")
        s = f.read()
        f.close()
        if int(s) == 1:
            await message.channel.send(
                "Connor is currently in the :dog: :house: as per Haley")
        elif int(s) == 0:
            await message.channel.send(
                "Connor is not currently in the dog house")
    if message.author.id == 192450685550198785 or message.author.id == 224039480921686016:
        if message.content.startswith("$patchNotes"):
            f = open("patchNotes.txt", "r")
            s = f.read()
            f.close()
            channel = client.get_channel(224198577033838592)
            await channel.send(s)

        if message.content.startswith("$botmsg"):

            string = message.content.replace("$botmsg ", "")
            channel = client.get_channel(224198577033838592)
            await channel.send(string)

    if '$addbirthday' in message.content.lower():

        input = readInput(message.content)
        month = input[1]
        month = getMonth(month)
        day = int(input[2])
        name = ""
        for x in range(3, len(input)):
            name += input[x]
            if (x != len(input) - 1):
                name += " "

        print(month)
        print(day)
        print(name)

        f = open("birthdays.json", "r")
        birthdays = json.load(f)
        f.close()

        foundBday = False
        #check if birthday exists
        for x in birthdays:
            if (x['name'].lower() == name.lower()):
                foundBday = True
                x['day'] = day
                x['month'] = month
                await message.channel.send('Changed birthday!')
            break

        if (not foundBday):
            dict = {'name': name, 'day': day, 'month': month}
            birthdays.append(dict)
            await message.channel.send('Added birthday!')

        f = open("birthdays.json", "w")
        json.dump(birthdays, f)
        f.close()

    if '$deletebirthday' in message.content.lower():
        input = readInput(message.content)
        name = ""
        for x in range(1, len(input)):
            name += input[x]
            if (x != len(input) - 1):
                name += " "

        f = open("birthdays.json", "r")
        birthdays = json.load(f)
        f.close()

        foundBday = False
        #check if birthday exists
        for x in birthdays:
            if (x['name'].lower() == name.lower()):
                foundBday = True
                birthdays.remove(x)
                await message.channel.send('Deleted birthday: ' + name)
                break
        f = open("birthdays.json", "w")
        json.dump(birthdays, f)
        f.close()

        if (not foundBday):
            await message.channel.send('Birthday not found')
    if '$getbirthdays ' in message.content.lower():
        try:
            input = readInput(message.content)

            monthInput = 0
            if (len(input) < 2):
                monthInput = datetime.now().month
                await message.channel.send('Birthdays this month:')
            else:
                monthInput = input[1]
                await message.channel.send('Birthdays in ' + monthInput)
                monthInput = getMonth(monthInput)

            f = open("birthdays.json", "r")
            birthdays = json.load(f)
            f.close()

            currentMonth = datetime.now().strftime("%b")
            found = False
            for x in birthdays:
                if (x['month'] == monthInput):
                    found = True
                    await message.channel.send(x['name'])

            if (not found):
                await message.channel.send('Invalid month')
        except:
            await message.channel.send('Invalid month')
        return

    if '$getbirthday ' in message.content.lower():
        input = readInput(message.content)
        name = ""
        for x in range(1, len(input)):
            name += input[x]
            if (x != len(input) - 1):
                name += " "

        f = open("birthdays.json", "r")
        birthdays = json.load(f)
        f.close()

        foundBday = False
        #check if birthday exists
        for x in birthdays:
            if (x['name'].lower() == name.lower()):
                foundBday = True
                await message.channel.send(f"{x['month']} / {x['day']}")
                break
        if (not foundBday):
            await message.channel.send('No birthday found...')
        return

    if '$poggybalance' in message.content.lower():
        input = readInput(message.content)

        await message.channel.send(
            f"Your balance is {getUserPoggyBalance(input[1])}")

    if '$addpoggypoints' in message.content.lower():
        if (message.author.id == 176911013856149504
                or message.author.id == 224039480921686016
                or message.author.id == 192450685550198785):
            input = readInput(message.content)
            addUserPoggyPoints(input[1], input[2])
            await message.channel.send("Added " + input[2] + " to user " +
                                       input[1])

    if '$notpog' in message.content.lower():
        if (message.author.id == 176911013856149504
                or message.author.id == 224039480921686016
                or message.author.id == 192450685550198785):
            input = readInput(message.content)
            removeUserPoggyBalance(input[1])
            await message.channel.send("Removed " + input[1])

    if '$poggyboard' in message.content.lower():
        print("Getting poggyboard")
        f = open("balances.json", "r")
        balances = json.load(f)
        f.close()

        string = 'The POGGY POINT current leaderboard is: \n'
        leaders = leaderBoard()
        size = len(leaders)
        for i in range(size):
            s2 = f"{leaders[i]} with {balances[leaders[i]]} points\n"
            string += s2
        await message.channel.send(string)


# haley dog 699374568195751958
    if message.author.id == 699374568195751958:  #haley
        if message.content.startswith("!doghouse"):
            f = open("dogHouse.txt", "r")
            s = f.read()
            f.close()
            dog = 0
            if int(s) == 0:
                dog = 1

            f = open("dogHouse.txt", "w")
            f.write(f"{dog}")
            f.close()
            await message.channel.send("Doghouse status has been changed.")

    if message.author.id == 290327583843942400:

        f = open("messageStats.txt", "r")
        str = f.read()

        oldNum = int(str)
        num = oldNum + 1
        f.close()
        f = open("messageStats.txt", "w")
        f.write(f"{num}")
        f.close()

        p = open("randomInt.txt", "r")
        rInt = int(p.read())
        f.close()

        if (num % rInt == 0):
            p = open("randomInt.txt", "w")
            p.write(f"{random.choice(range(1,100))}")
            p.close()
            await message.channel.send(
                f"The number of based messages from Jake is {num}")

    # Minion -> Jake Functionality
    if "minion" in message.content.lower(
    ) or "minions" in message.content.lower():
        userId = message.author.id
        temp = message.content.lower().replace("minion", "Jake")
        minionStr = temp
        await message.channel.send(
            f"<@{userId}> Did you mean to say: '{minionStr}'")

    # Bad word Corrector
    if message.author.id == 224039480921686016:
        for word in badWords:
            if word in message.content.lower():
                userId = message.author.id
                string = f"<@{userId}> Did you mean to say, '{message.content.lower().replace(word,                         badWords[word])}' as per <@{699374568195751958}> 's request"

                await message.channel.send(string)

    if "reportfarm" in message.content.lower():
      input = readInput(message.content)
      name = ""
      if len(input) > 1 :
          for x in range(1, len(input)):
            name += input[x]
            if (x != len(input) - 1):
                name += " "
      await message.channel.send(f"Reported '{name}' for farming. Points will be deducted by the end of the week.")
                                       
def readInput(string):  #reads the input peolpe give.

    #remove the command from the string
    string = string.split(" ")
    print(f"this is the current string: {string}")

    return string


def leaderBoard():
    f = open("balances.json", "r")
    balances = json.load(f)
    f.close()

    pos = 0
    temp = 0

    balList = list(balances.keys())
    for i in range(0, len(balList) - 1):
        max = balances[balList[i]]
        for x in range(i + 1, len(balList)):
            if balances[balList[x]] > max:  # swap these two
                max = balances[balList[x]]
                pos = x
        if max != balances[balList[i]]:
            temp = balList[pos]
            balList[pos] = balList[i]
            balList[i] = temp

    return balList


def addUserPoggyPoints(
        name, points):  # lets people place a bet, either true or false

    f = open("balances.json", "r")
    balances = json.load(f)
    f.close()

    if name.lower() not in balances:
        balances[name.lower()] = 0

    balances[name.lower()] += int(points)

    f = open("balances.json", 'w')
    json.dump(balances, f)
    f.close()


def getUserPoggyBalance(name):  # check your point balance
    f = open("balances.json", "r")
    balances = json.load(f)
    f.close()

    if name not in balances:
        balances[name.lower()] = 0

    f = open("balances.json", 'w')
    json.dump(balances, f)
    f.close()

    return balances[name.lower()]


def removeUserPoggyBalance(name):
    f = open("balances.json", "r")
    balances = json.load(f)
    f.close()

    if name.lower() not in balances:
        return

    balances.pop(name.lower())

    f = open("balances.json", 'w')
    json.dump(balances, f)
    f.close()


def getMonth2(num) -> str:
    mapping = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }

    return mapping[num]


def getMonth(s) -> int:
    s = s.lower()
    mapping = {
        "january": 1,
        "february": 2,
        "march": 3,
        "april": 4,
        "may": 5,
        "june": 6,
        "july": 7,
        "august": 8,
        "september": 9,
        "october": 10,
        "november": 11,
        "december": 12
    }
    return mapping[s]


def getMonth2(s) -> int:
    s = str(s).lower()
    mapping = {
        "jan": 1,
        "feb": 2,
        "mar": 3,
        "apr": 4,
        "may": 5,
        "jun": 6,
        "jul": 7,
        "aug": 8,
        "sep": 9,
        "oct": 10,
        "nov": 11,
        "dec": 12
    }
    return mapping[s]
    # Dalle-Bot Functionality

    # ## sean id 290242931221331969
    # # if sean, perform sentiment analysis
    # if message.author.id == 290242931221331969:

    #     credential = AzureKeyCredential("0385372efab1468da43a7f2ecc5ce7fc")
    #     endpoint = "https://discordbotanalysis.cognitiveservices.azure.com/"
    #     text_analytics_client = TextAnalyticsClient(endpoint, credential)

    #     documents = [message.content]

    #     response = text_analytics_client.analyze_sentiment(documents,
    #                                                        language="en")

    #     result = [doc for doc in response if not doc.is_error]

    #     for doc in result:
    #         print("Overall sentiment: {}".format(doc.sentiment))
    #         print("Scores: positive={}; neutral={}; negative={} \n".format(
    #             doc.confidence_scores.positive,
    #             doc.confidence_scores.neutral,
    #             doc.confidence_scores.negative,
    #         ))
    # # test for connor
    # # connor id 224039480921686016
    # # if connor, perform sentiment analysis
    # if message.author.id == 224039480921686016:

    #     credential = AzureKeyCredential("0385372efab1468da43a7f2ecc5ce7fc")
    #     endpoint = "https://discordbotanalysis.cognitiveservices.azure.com/"
    #     text_analytics_client = TextAnalyticsClient(endpoint, credential)

    #     documents = [message.content]

    #     response = text_analytics_client.analyze_sentiment(documents,
    #                                                        language="en")

    #     result = [doc for doc in response if not doc.is_error]

    #     for doc in result:
    #         m = "Scores: positive={}; neutral={}; negative={} \n".format(
    #             doc.confidence_scores.positive, doc.confidence_scores.neutral,
    #             doc.confidence_scores.negative)

    #     await message.channel.send(m)


# jakes id 290327583843942400

client.run('OTYxNDYyMTk4OTc3MzIzMDYw.Yk5Vcw.Yz8GmasD2V9Ty6hJEC6nfIYDv7c')
