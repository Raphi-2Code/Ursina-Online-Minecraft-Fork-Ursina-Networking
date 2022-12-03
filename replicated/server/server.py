from asyncio.tasks import sleep
from random import uniform
from time import *
from ursinanetworking import *
from perlin_noise import PerlinNoise
from opensimplex import OpenSimplex
from ursina import Vec3, distance
import asyncio

print("Hello from the server !")

Server = UrsinaNetworkingServer(socket.gethostbyname(socket.gethostname()), 25565)
Easy = EasyUrsinaNetworkingServer(Server)
Blocks = {}
saving_list = []
def Explosion(position):
    Server.broadcast("Explode", position)
    sleep(1)
    to_destroy = []
    for x in Blocks:
        a = (Blocks[x]["position"])
        b = (position)
        if distance(Vec3(a), Vec3(b)) < 2:
            to_destroy.append(x)
    for x in to_destroy:
        destroy_block(x)


def destroy_block(Block_name):
    del Blocks[Block_name]
    Easy.remove_replicated_variable_by_name(Block_name)

i = 0
def spawn_block(block_type, position, investigator = "client"):
    global i
    block_name = f"blocks_{i}"
    Easy.create_replicated_variable(
        block_name,
        { "type" : "block", "block_type" : block_type, "position" : position, "investigator" : investigator}
    )

    if block_type == "tnt":
        threading.Thread(target = Explosion, args=(position,)).start()

    Blocks[block_name] = {
        "name" : block_name,
        "position" : position
    }
    spawn_Block = block_name+"="+f"spawn_block(block_type='{block_type}',position={position},investigator='{investigator}'"+")"
    saving_list.append(spawn_Block)
    i += 1
@Server.event
def onClientConnected(Client):
    Easy.create_replicated_variable(
        f"player_{Client.id}",
        { "type" : "player", "id" : Client.id, "position" : (0, 0, 0) }
    )
    print(f"{Client} connected !")
    Client.send_message("GetId", Client.id)

@Server.event
def onClientDisconnected(Client):
    Easy.remove_replicated_variable_by_name(f"player_{Client.id}")
    try:e=open("New World.txt","x")
    except:os.remove("New World.txt");e=open("New World.txt","x")
    for block in saving_list:
        e.write(block+"\n")
    print(f"{Client} disconnected!")

@Server.event
def request_destroy_block(Client, Block_name):
    destroy_block(Block_name)
    for block in saving_list:
        if block.startswith(Block_name):
            saving_list.remove(block)
@Server.event
def request_place_block(Client, Content):
    spawn_block(Content["block_type"], Content["position"])
@Server.event
def MyPosition(Client, NewPos):
    Easy.update_replicated_variable_by_name(f"player_{Client.id}", "position", NewPos)

tmp = OpenSimplex(seed=random.randint(10000000000,10000000000000000))
load=True
BLOCK_TYPES = [
    "grass",
    "leave",
    "wood",
    "sand",
    "glass",
    "tnt"
]
def BlockSaving():

    for x in range(32):
        for z in range(32):

            l = round(tmp.noise2(x = x / 5, y = z / 5))+1
            def TerrainChanges():
                if l<1: spawn_block(block_type="sand", position=(x, l, z), investigator = "server")
                randomized=random.randint(1,4)
                if l >= 2 and randomized==1:
                    spawn_block(block_type="wood", position=(x, l, z), investigator = "server")
                    spawn_block(block_type="wood", position=(x, l+1, z), investigator="server")
                    spawn_block(block_type="wood", position=(x, l+2, z), investigator="server")
                    spawn_block(block_type="leave", position=(x+1, l+2, z-1), investigator="server")
                    spawn_block(block_type="leave", position=(x+1, l+2, z), investigator="server")
                    spawn_block(block_type = "leave", position = (x, l + 2, z+1), investigator = "server")
                    spawn_block(block_type = "leave", position = (x+1, l + 2, z + 1), investigator = "server")
                    spawn_block(block_type = "leave", position = (x-1, l + 2, z-1), investigator = "server")
                    spawn_block(block_type="leave", position=(x-1, l+2, z-1), investigator="server")
                    spawn_block(block_type="leave", position=(x-1, l+2, z), investigator="server")
                    spawn_block(block_type = "leave", position = (x-1, l + 2, z + 1), investigator = "server")
                    #__________________________________________________________________________________________
                    spawn_block(block_type="leave", position=(x + 1, l + 3, z - 1), investigator="server")
                    spawn_block(block_type="leave", position=(x + 1, l + 3, z), investigator="server")
                    spawn_block(block_type="leave", position=(x, l + 3, z + 1), investigator="server")
                    spawn_block(block_type="leave", position=(x + 1, l + 3, z + 1), investigator="server")
                    spawn_block(block_type="leave", position=(x - 1, l + 3, z - 1), investigator="server")
                    spawn_block(block_type="leave", position=(x - 1, l + 3, z - 1), investigator="server")
                    spawn_block(block_type="leave", position=(x - 1, l + 3, z), investigator="server")
                    spawn_block(block_type="leave", position=(x - 1, l + 3, z + 1), investigator="server")
                    spawn_block(block_type="leave", position=(x, l + 3, z), investigator="server")
                    spawn_block(block_type="leave", position=(x, l + 3, z - 1), investigator="server")
                    spawn_block(block_type="leave", position=(x , l + 2, z - 1), investigator="server")
                if l>=2 and randomized!=1:
                    spawn_block("grass",(x,l,z),investigator="server")
            spawn_block("grass",(x,l,z),investigator="server") if l>=1 and not(l>=2) else TerrainChanges()
if not load:BlockSaving()
else:
    try:
        if open("New World.txt","r").read()=='':
            BlockSaving()
    except:pass
    exec(open("New World.txt","r").read())
while True:
    Easy.process_net_events()
