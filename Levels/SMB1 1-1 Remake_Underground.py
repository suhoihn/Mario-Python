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
Globals.SnowTheme = False
Globals.WaterTheme = False
Globals.AutoScroll = False
Globals.ScrollLimit = [[0,0],[0,0]]

#=======BackGround=======#As well as music
for i in range(2):
    BackGround(i,theme = "Underground")
#=======Block=======
for i in range(8):
    BreakableBlock(32 * (6 + i), 32 * 2, ContainmentType = "Coin")
    for j in range(3):
        BreakableBlock(32 * (6 + i), 32 * (10 + j),ContainmentType = "Coin")
        if (i,j) != (0,0) and (i,j) != (7,0):
            coin(0,0,center = (32 * (7 + i) - 16, 32 * (5 + j * 2) + 16))
for i in range(13):
    BreakableBlock(32 * 0, 32 * i,ContainmentType = "Coin")
    
#=======Cannon=======

#=======Coin=======

#=======Enemy(Koopa)=======

#=======Ground=======#ln 36 start
Map ="""
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
11111111111111111111
11111111111111111111
"""
Ground.initialize(Map)

#=======Pipe======
pipe(32 * 1,32 * 0,0,"UP",LvTrans = True)
pipe(32 * 16,32 * 11,1,"RIGHT",LvTrans = True)
pipe(32 * 18,32 * -1,-1,"DOWN",length = 14)
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

