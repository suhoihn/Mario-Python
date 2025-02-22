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
Globals.ScrollLimit = [[None,None],[0,85]]
Globals.LevelCount = 1
#=======BackGround=======
for i in range(8):
    BackGround(i,theme = "Underground")
#=======Block=======

#=======Cannon=======

#=======Coin=======

#=======Enemy(Koopa)=======

#=======Ground=======#ln 40 start
Map ="""
00000000000000000000000000000000000000
00000000000000000000000000000000000000
00000000000000000000000000000000000000
00000000000000000000000000000000000000
00000000000000000000000000000000000000
00000000000000000000000000000000000000
00000000000000000000000000000000000000
00000000000000000000000000000000000000
00000000000000000000000000000000000000
00000000000000000000000000000000000000
00000000000000000000000000000000000000
00000000000000000000000000000000000000
00000000000000000000000000000000000000
00000000000000000000000000000000000000
00000000000000000000000000000000000000
00000000000000000000000000000000000000
00000000000000000000000000000000000000
"""
Ground.initialize(Map)

#=======Pipe======
##pipe(32 * 39, 32 * 15,-1,"UP",19)
##pipe(32 * 45, 32 * 22,-1,"DOWN",6)
##
##pipe(32 * 92, 32 * 0,2,"UP",LvTrans = True,TargetLevelIdx = 1)
##pipe(32 * 117, 32 * 21,-1,"DOWN",6)
##
##pipe(32 * 119, 32 * 22,-1,"DOWN",5)
##pipe(32 * 125, 32 * 19,-1,"UP",23)
##
##pipe(32 * 140, 32 * 16,3,"UP",20,LvTrans = True,TargetLevelIdx = 2)
##pipe(32 * 57 -16, 32 * -2,1,"UP",LvTrans = True,TargetLevelIdx = 1)

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

