import json, time, random, asyncio
from websocket import create_connection
from multiprocessing import Process

session_id = "" # insert ur account's sessionID here

def chatbot():
    count = 0
    rate_limited = []
    ws = create_connection("wss://ws.growcasino.net/")
    ws.send(json.dumps({"id": "authSession","sessionID": session_id}))
    while 1:
        r = json.loads(str(ws.recv()))
        if r["id"] == "onChatMessage":
            username = ""
            try:
                username = r["data"]["username"]
            except Exception as e: print(e); pass
            count += 1
            if count > 4:
                count = 0
                if len(rate_limited) > 0: rate_limited.pop(0)
            if username != "":
                if username != "bot" and username not in rate_limited:
                  input = str(r["data"]["message"])
                  if input == "@bot":
                      rate_limited.append(username)
                      ws.send(json.dumps({"id":"onChatMessage","message":( "@" + username + " Info: prefix '!' | commands: dice flip stats slap hug cock top"),"sessionID":session_id}))
                  elif input == "!cock":
                      rate_limited.append(username)
                      ws.send(json.dumps({"id":"onChatMessage","message":("@" + username + " 8=" + random.choice(["=====", "", "==", "===", "=", "=============", "=", "========MEGA=========", "=", "===", "==", "==", "=======", "=========", "=", "===", "=====", "=~=", "=-=", "=w=", "==u==", "==", "==", "=="]) + "D"),"sessionID":session_id}))
                  elif input == "!dice":
                      rate_limited.append(username)
                      ws.send(json.dumps({"id":"onChatMessage","message":( "@" + username + " rolled a " + str(random.randint(1,6)) + "!"),"sessionID":session_id}))
                  elif "!slap" in input:
                      if len(input) > 6:
                          rate_limited.append(username)
                          ws.send(json.dumps({"id":"onChatMessage","message":( "@" + username + " slapped @" + input.replace("!slap ", "").replace("@", "") + "!"),"sessionID":session_id}))
                  elif "!hug" in input:
                      if len(input) > 6:
                          rate_limited.append(username)
                          ws.send(json.dumps({"id":"onChatMessage","message":( "@" + username + " hugged @" + input.replace("!hug ", "").replace("@", "") + "!"),"sessionID":session_id}))
                  elif "!stats" in input:
                      rate_limited.append(username)
                      if len(input) > 7:
                          ws.send(json.dumps({"id":"onRequestUserData","username": input.replace("!stats ", "").replace("@", ""),"sessionID":session_id}))
                      else:
                          ws.send(json.dumps({"id":"onRequestUserData","username": username,"sessionID":session_id}))
                  elif input == "!flip":
                      rate_limited.append(username)
                      ws.send(json.dumps({"id":"onChatMessage","message":( "@" + username + " flipped " + str(random.choice(["heads", "tails"])) + "!"),"sessionID":session_id}))
                  elif input == "!top":
                      rate_limited.append(username)
                      ws.send(json.dumps({"id":"onRequestLeaderboard","orderBy":"profitMost","sessionID":session_id}))
        if r["id"] == "onRequestUserData" and r["success"]:
            msg = r["data"]["username"] + " (Total bets: " + str(r["data"]["gamesPlayed"]) + " | Net profit: " + str(round(float(r["data"]["netProfit"]))) + "DL)"
            ws.send(json.dumps({"id":"onChatMessage","message":msg,"sessionID":session_id}))
        if r["id"] == "onBalanceUpdated":
            ws.send(json.dumps({"id":"onChatMessage","message":("Bot's wallet: " + str(round(float(r["balance"])*100)) + "wl <3"),"sessionID":session_id}))
        if r["id"] == "onRequestLeaderboard":
            ws.send(json.dumps({"id":"onChatMessage","message":("Leaderboards > 1 " + r["data"][0]["username"] + " | 2 " + r["data"][1]["username"] + " | 3 " + r["data"][2]["username"]),"sessionID":session_id}))
    ws.close()


if __name__ == '__main__':
    Process(target=chatbot).start()
