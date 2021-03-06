import asyncio
import getpass
import json
import os
import pygame
import websockets
import agent
import pygame

pygame.init()
program_icon = pygame.image.load("data/icon2.png")
pygame.display.set_icon(program_icon)

async def agent_loop(server_address="localhost:8000", agent_name="student"):
    async with websockets.connect(f"ws://{server_address}/player") as websocket:
        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
        c,x,y=0,0,0
        actions=[]
        lookahead=1 #change this to change the number of lookahead pieces
        while True:
            try:
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server
                
                if(c==0): #process first message sent by the server
                    x,y=state.get('dimensions')
                    c=1
                    continue
                piece = state.get('piece')
                if(piece!=None):
                    if(actions==[]):
                        actions=agent.run_ai(state.get('game'),piece,state.get('next_pieces'),x,y,lookahead) #go fetch new actions
                    else:
                        await websocket.send(json.dumps({"cmd": "key", "key": actions.pop(0)}))  # send key command to server               
                else:
                    actions=[]
            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return


# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
