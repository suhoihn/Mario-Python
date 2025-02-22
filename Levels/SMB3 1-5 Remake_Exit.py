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
from Galumba import *

import Globals
Globals.AutoScroll = False
Globals.ScrollLimit = [[None,32 * 12],[None, 357 - 9]]#441]]
#=======BackGround=======
for i in range(8):
    BackGround(i)
#=======Block=======
#TextBlock(32 * 9,32 * 21,["OMG This took so long time!","Made in 2021 05 16","","Original", "Super Mario Bros. 3 1 dash 5"])
##QBlock(32 * 18,32 * 19,Invisible = True,ContainmentType = "Mushroom")
##QBlock(32 * 18,32 * 19,Invisible = True,ContainmentType = "FireFlower")
##QBlock(32 * 18,32 * 19,Invisible = True,ContainmentType = "Star")

#=======Cannon=======

#=======Coin=======
        
#=======Enemy(Koopa)=======

#=======Ground=======#ln 38 start
Map ="""
00000000000000000000000000000000
00000000000000000000000000000000
00000000000000000000000000000000
00000000000000000000000000000000
00000000000000000000000000000000
00000000000000000000000000000000
00000000000000000000000000000000
00000000000000000000000000000000
00000000000000000000000000000000
00000000000000000000000000000000
00000000000000000000000000000000
00000000000000000000000000000000
00000000000000000000000000000000
00000000000000000000000000000000
00000000000000000000000000000000
00000000000000000000000000000000
00000000000000000000000000000000
00000000000000000000000000000000
00000000000000000000000000000000
00000000000000000000000000000000
00000000000000000000000000000000
00000000000000000000000000000000
000000000000000000G0000000000000
00000000000000000000000000000000
11111111111111111111111111111111
11111111111111111111111111111111
"""
Ground.initialize(Map)

#=======Pipe======
pipe(32 * 2, 32 * 22,3,"DOWN",LvTrans = True,TargetLevelIdx = 0)

Globals.CurrentPipes = pipes

#=======Platform=======

#=======Seesaw=======

#=======Spike=======

#=======Spiny=======

#=======Spring=======

#=======Things(Pswitch)=======

#=======Thowmp=======

#=======와리가리=======

#=======Yoshi=======

#=======Galumba=======

