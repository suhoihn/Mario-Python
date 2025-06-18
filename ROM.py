#ROM
from Coin import *
from Spike import *
from Spring import *
from 와리가리 import *
from seesaw import *
from BackGround import *
import Ground
from Enemy import *
from Thwomp import *
from Pipe import *
from Cannon import *
from Block import *
from Platform import *
from Things import *
from Spiny import *
from Yoshi import *
#from Vine import *
from Galumba import *
from Goal import Goals
from Firebar import *

import importlib
##Coins = []
##Spikes = []
##Springs = []
##swings = []
##rotatingplatforms = []
##seesaws = []
##BackGrounds = []
##Koopas = []
##KoopaToopas = []
##Thowmps = []
##Pipes = []
##Cannons = []
##Blocks = []
##Platforms = []
##Pswitchs = []
##Spinies = []
##Yoshis = []
def initialize():
    import Lakitu,Firebar,Coin,Goal,Spike,Spring,와리가리,seesaw,BackGround,Enemy,Thwomp,Pipe,Cannon,Block,Mushroom,Platform,Things,Spiny,Yoshi,Galumba,Vine

    importlib.reload(Goal)

    importlib.reload(Coin)
    importlib.reload(Spike)
    importlib.reload(Spring)
    importlib.reload(와리가리)
    importlib.reload(seesaw)
    importlib.reload(BackGround)
    importlib.reload(Enemy)
    importlib.reload(Mushroom)
    importlib.reload(Thwomp)
    importlib.reload(Pipe)
    importlib.reload(Cannon)
    importlib.reload(Block)
    importlib.reload(Platform)
    importlib.reload(Things)
    importlib.reload(Spiny)
    importlib.reload(Yoshi)
    importlib.reload(Galumba)
    importlib.reload(Vine)
    importlib.reload(Firebar)
    importlib.reload(Lakitu)

#from Globals import MarioAt
Levels = [
    #"flat land test",
    "Fireland",
    "Autoscrolling Water Level",
    ["Falling Platforms","Falling Platforms_Exit"],
    ["SMB1 1-1 Remake","SMB1 1-1 Remake_Underground"],
    ["SMB3 1-5 Remake","SMB3 1-5 Remake_Bonus Level","SMB3 1-5 Remake_Exit"],
    "Lv.test",
    ["Rough Hills","Tower of Patience"],
    "A Decent Level Solely Made by Myself",
    "Kaizo Mario",
    #"Love Message",
    "The Doom of P-Switch",
    ["NSMB 1-1 Remake","NSMB 1-1 Remake_underground"],
    #"Unfinished Tutorial",
    ["Falling Platforms","Falling Platforms_Exit"],
    "Non-Stop Action with Stars"]
#random.shuffle(Levels)
def LoadLevel(L,MarioAt = 0):
    Lvidx = L
    if L == len(Levels):
        Lvidx = 0
        Globals.Lvidx = 0
        random.shuffle(Levels)
    Globals.SnowTheme = False
    Globals.WaterTheme = False
    Globals.AutoScroll = False
    info = ""
    if type(Levels[Lvidx]) == list:
        LvName = Levels[Lvidx][MarioAt]#sub-level이 있는 경우
    else:
        LvName = Levels[Lvidx]#sub-level이 없는 경우
    try:
        with open("Levels/" + LvName + ".py",'r',encoding='UTF8') as f :
            a = f.readlines()
            for i in a:
                info += i
            f.close()
    except:
        with open("Levels/" + LvName + ".txt",'r',encoding='UTF8') as f :
            a = f.readlines()
            for i in a:
                info += i
            f.close()
    exec(info)

