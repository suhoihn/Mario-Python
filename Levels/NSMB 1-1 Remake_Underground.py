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
Globals.ScrollLimit = [[0,32 * 13],[0,0]]
Globals.LevelCount = 3

#=======BackGround=======#As well as music
for i in range(2):
    BackGround(i,"Underground")
#=======Block=======
for i in range(5):
    BreakableBlock(32 * (4 + i), 32 * 7)
    if i == 0 or i == 2: QBlock(32 * (16 + i), 32 * 6,ContainmentType = "Coin")
    elif i == 4: QBlock(32 * (16 + i), 32 * 6,ContainmentType = "FireFlowerR")
    else: BreakableBlock(32 * (16 + i), 32 * 6)
for i in range(2):
    for j in range(2):
        Block(32 * (31 + i), 32 * (7 + j))
#=======Cannon=======

#=======Coin=======
for i in range(5):
    coin(32 * (4 + i), 32 * 6)

for i in range(4):
    if i == 0 or i == 3:
        coin(32 * (11 + i), 32 * 7)
    else:
        coin(32 * (11 + i), 32 * 6)

for i in range(2):
    coin(32 * (22 + i), 32 * 6)
    coin(32 * (25 + i), 32 * 5)

#=======Enemy(Koopa)=======
#=======Ground=======#ln 36 start
Map ="""
100111111111111111111111111111100
100000000000000000000000000001100
100000000000000000000000000001100
100000000000000000000000000001100
100000000000000000000000000001100
100000000000000000000000000001100
100000000000000000000000000001100
100000000000000000000000000000000
100000000000000000000000000000000
1000000000000000000000000(1111111
1000000000000000000000(1111111111
111111111111001111111111111111111
111111111111001111111111111111111
111111111111001111111111111111111
111111111111001111111111111111111
111111111111001111111111111111111
"""
Ground.initialize(Map)

#=======Pipe======
pipe(32 * 1, 32 * 0,1,"UP",LvTrans = True,TargetLevelIdx = 0,Enterable = False)
pipe(32 * 28, 32 * 7,2,"RIGHT",length = 4,LvTrans = True,TargetLevelIdx = 0)
pipe(32 * 31, 32 * -2,-1,"DOWN",length = 9)

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
galumba(32 * 10, 32 * 10)
galumba(32 * 24, 32 * 9)
galumba(32 * 27, 32 * 8)
