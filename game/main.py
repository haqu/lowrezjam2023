import pyxel

CAT_START_POS=(6,5)
TILEMAP_INITIAL_OFFSET=(2,0)

OBSTACLES_ROWS=4
LADDER_TILE=(5,5)
BOT_TILE=(4,9)

CAT_TILE=(0,6)
CAT1_TILE=(0,7)
CAT2_TILE=(0,8)
CAT3_TILE=(0,9)
CAT4_TILE=(0,10)
SLEEPING_CAT_TILE=(0,11)

KEY1_TILE=(3,4)
KEY2_TILE=(4,4)
KEY3_TILE=(3,5)
KEY4_TILE=(4,5)
DNA_TILE=(4,8)

DOOR1_TILE=(3,6)
DOOR2_TILE=(4,6)
DOOR3_TILE=(3,7)
DOOR4_TILE=(4,7)

CHIP_TILE=(3,8)
SHIP_ALERT_TILE=(7,8)
SHIP_FIXED_TILE=(7,7)
BG_TILE=(5,4)
MAN_TILE=(1,14)

class Cat:
    def __init__(self):
        self.x=CAT_START_POS[0]*8
        self.y=CAT_START_POS[1]*8
        self.dx=0
        self.dy=0
        self.dir=1
        self.base_tile=CAT_TILE
        self.key_tile=DNA_TILE
        self.door_tile=None
        self.anim_frame=0
        self.has_chip=False
        self.is_sleeping=True
        self.no_collection_countdown=0

class Bot:
    def __init__(self):
        self.x=16
        self.y=40
        self.dir=1
        self.tx=self.x
        self.ty=self.y
        self.timer=30

class Ship:
    def __init__(self):
        self.alert_frame=0
        self.fixed=False

class Dialog:
    def __init__(self):
        self.started=False
        self.hint_started=False

class Game:
    def __init__(self):
        self.offset=TILEMAP_INITIAL_OFFSET
        self.ready_to_finish=False
        self.finished=False
        self.man_frame=0
        self.music_started=False

cat=Cat()
bot=Bot()
ship=Ship()
dialog=Dialog()
game=Game()

def check_obstacle(x,y):
    x+=game.offset[0]*64
    y+=game.offset[1]*64
    xi0,xi1=x//8,(x+7)//8
    yi0,yi1=y//8,(y+7)//8
    points=[
        (xi0,yi0),
        (xi1,yi0),
        (xi0,yi1),
        (xi1,yi1),
    ]
    tm=pyxel.tilemap(0)
    for (xi,yi) in points:
        t=tm.pget(xi,yi)
        if t[0]>=1 and t[1]<OBSTACLES_ROWS:
            return True
        if t==DOOR1_TILE and cat.door_tile!=t:
            return True
        if t==DOOR2_TILE and cat.door_tile!=t:
            return True
        if t==DOOR3_TILE and cat.door_tile!=t:
            return True
        if t==DOOR4_TILE and cat.door_tile!=t:
            return True
    return False

def check_ladder(x,y):
    x+=game.offset[0]*64
    y+=game.offset[1]*64
    xi0,xi1=x//8,(x+7)//8
    yi0,yi1=y//8,(y+7)//8
    points=[
        (xi0,yi0),
        (xi1,yi0),
        (xi0,yi1),
        (xi1,yi1),
    ]
    tm=pyxel.tilemap(0)
    for (xi,yi) in points:
        t2=tm.pget(xi,yi)
        if t2==LADDER_TILE:
            return True
    return False

def check_item():
    if cat.no_collection_countdown>0:
        cat.no_collection_countdown-=1
        return
    x=cat.x+game.offset[0]*64
    y=cat.y+game.offset[1]*64
    xi0,xi1=x//8,(x+7)//8
    yi0,yi1=y//8,(y+7)//8
    points=[
        (xi0,yi0),
        (xi1,yi0),
        (xi0,yi1),
        (xi1,yi1),
    ]
    tm=pyxel.tilemap(0)
    for (xi,yi) in points:
        t=tm.pget(xi,yi)
        if t==KEY1_TILE:
            tm.pset(xi,yi,cat.key_tile)
            cat.base_tile=CAT1_TILE
            cat.key_tile=KEY1_TILE
            cat.door_tile=DOOR1_TILE
            pyxel.play(0,1)
            cat.no_collection_countdown=30
            return
        if t==KEY2_TILE:
            tm.pset(xi,yi,cat.key_tile)
            cat.base_tile=CAT2_TILE
            cat.key_tile=KEY2_TILE
            cat.door_tile=DOOR2_TILE
            pyxel.play(0,1)
            cat.no_collection_countdown=30
            return
        if t==KEY3_TILE:
            tm.pset(xi,yi,cat.key_tile)
            cat.base_tile=CAT3_TILE
            cat.key_tile=KEY3_TILE
            cat.door_tile=DOOR3_TILE
            pyxel.play(0,1)
            cat.no_collection_countdown=30
            return
        if t==KEY4_TILE:
            tm.pset(xi,yi,cat.key_tile)
            cat.base_tile=CAT4_TILE
            cat.key_tile=KEY4_TILE
            cat.door_tile=DOOR4_TILE
            pyxel.play(0,1)
            cat.no_collection_countdown=30
            return
        if t==DNA_TILE:
            tm.pset(xi,yi,cat.key_tile)
            cat.base_tile=CAT_TILE
            cat.key_tile=DNA_TILE
            cat.door_tile=None
            pyxel.play(0,1)
            cat.no_collection_countdown=30
            return
        if t==CHIP_TILE:
            tm.pset(xi,yi,BG_TILE)
            pyxel.play(0,1)
            cat.has_chip=True
            return

def check_door():
    x=cat.x+game.offset[0]*64
    y=cat.y+game.offset[1]*64
    xi0,xi1=x//8,(x+7)//8
    yi0,yi1=y//8,(y+7)//8
    points=[
        (xi0,yi0),
        (xi1,yi0),
        (xi0,yi1),
        (xi1,yi1),
    ]
    tm=pyxel.tilemap(0)
    for (xi,yi) in points:
        t=tm.pget(xi,yi)
        if t==cat.door_tile:
            open_door_tile=(cat.door_tile[0],cat.door_tile[1]+4)
            tm.pset(xi,yi,open_door_tile)
            pyxel.play(0,5)
            return

def button_left():
    return (pyxel.btn(pyxel.KEY_LEFT) or
            pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT))

def button_right():
    return (pyxel.btn(pyxel.KEY_RIGHT) or
            pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT))

def button_up():
    return (pyxel.btn(pyxel.KEY_UP) or
            pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP) or
            pyxel.btn(pyxel.GAMEPAD1_BUTTON_A))

def button_down():
    return (pyxel.btn(pyxel.KEY_DOWN) or
            pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN))

def button_action():
    return (pyxel.btnp(pyxel.KEY_SPACE) or
            pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B))

def button_any():
    return (button_left() or
            button_right() or
            button_up() or
            button_down() or
            button_action())

def update_cat():
    if cat.is_sleeping:
        cat.anim_frame=(cat.anim_frame+0.03)%2
        if button_any() and cat.is_sleeping:
            cat.is_sleeping=False
            advance_dialog()
        return
    x,y=cat.x,cat.y
    cat.dx=0
    if button_left():
        cat.dx=-2
        cat.dir=-1
    if button_right():
        cat.dx=2
        cat.dir=1
    on_ladder=check_ladder(x,y)
    if on_ladder:
        cat.dy=0
        if button_up():
            cat.dy=-2
        elif button_down():
            cat.dy=2
        if cat.dy!=0:
            while not check_ladder(x,y+cat.dy+1):
                cat.dy-=pyxel.sgn(cat.dy)
    else:
        if check_obstacle(x,y+1) or check_ladder(x,y+1):
            if button_up():
                # snap to empty space above
                if check_obstacle(x,y-1):
                    for x2 in range(x-3,x+3+1):
                        if not check_obstacle(x2,y-1):
                            x=x2
                            break
                if not check_obstacle(x,y-1):
                    cat.dy=-8
                    pyxel.play(1,0)
            elif button_down():
                cat.dy=2
            else:
                # snap to empty space below
                if cat.dx==0:
                    for x2 in range(x-3,x+3+1):
                        if not check_obstacle(x2,y+1):
                            x=x2
                            break
        else:
            cat.dy=min(cat.dy+2,3)
    while check_obstacle(x+cat.dx,y):
        found=False
        for y2 in range(y,y-4,-1):
            if not check_obstacle(x+cat.dx,y2):
                found=True
                y=cat.y=y2
                break
        if found:
            break
        cat.dx-=pyxel.sgn(cat.dx)
    x+=int(cat.dx)
    while check_obstacle(x,y+cat.dy):
        cat.dy-=pyxel.sgn(cat.dy)
    y+=int(cat.dy)
    if x>64-4:
        if game.offset[0]==6:
            x=64-4
        elif dialog.started and game.offset==TILEMAP_INITIAL_OFFSET:
            dialog.hint_started=True
            x=64-4
        else:
            dialog.started=False
            game.offset=(game.offset[0]+1,game.offset[1])
            x-=64
    elif x<-4:
        if game.offset[0]==0:
            x=-4
        elif dialog.started and game.offset==TILEMAP_INITIAL_OFFSET:
            dialog.hint_started=True
            x=-4
        else:
            dialog.started=False
            game.offset=(game.offset[0]-1,game.offset[1])
            x+=64
    if y>64-4:
        dialog.started=False
        game.offset=(game.offset[0],game.offset[1]+1)
        y-=64
    elif y<-4:
        if game.offset[1]==0:
            y=-4
        else:
            dialog.started=False
            game.offset=(game.offset[0],game.offset[1]-1)
            y+=64
    cat.x=x
    cat.y=y
    check_item()
    check_door()
    if cat.dx!=0 and cat.dy==0:
        cat.anim_frame=(cat.anim_frame+0.5)%2
    else:
        cat.anim_frame=0

def advance_dialog():
    if not dialog.started:
        dialog.started=True
        dialog.phrase_index=0
        if game.offset==TILEMAP_INITIAL_OFFSET:
            if cat.base_tile!=CAT_TILE:
                dialog.phrases=[
                    ('cat','bzargh!',1),
                    ('bot',' go away!',2),
                ]
            elif not ship.fixed:
                dialog.phrases=[
                    ('cat','meow?',0),
                    ('bot','rocket...',2),
                    ('bot','malfunction',2),
                    ('bot','find',1),
                ]
            else:
                dialog.phrases=[
                    ('cat','meow!',0),
                    ('bot','welcome back',3),
                    ('bot','get ready!',2),
                    ('cat','purr',0),
                ]
        else:
            if cat.base_tile!=CAT_TILE:
                dialog.phrases=[
                    ('cat','bzargh!',1),
                ]
            else:
                dialog.phrases=[
                    ('cat','meow!',0),
                ]

        dialog.n_phrases=len(dialog.phrases)
    else:
        dialog.phrase_index+=1
        dialog.hint_started=False
    if dialog.phrase_index==dialog.n_phrases:
        dialog.started=False
        if ship.fixed and cat.base_tile==CAT_TILE:
            game.ready_to_finish=True
        elif not game.music_started:
            pyxel.playm(0,0,True)
            game.music_started=True
    else:
        who,txt,_=dialog.phrases[dialog.phrase_index]
        if who=='cat':
            if cat.base_tile!=CAT_TILE:
                pyxel.play(0,7)
            else:
                if txt.startswith('purr'):
                    pyxel.play(0,6)
                else:
                    pyxel.play(0,2)
        else:
            pyxel.play(0,3)

def update():
    #if pyxel.btnp(pyxel.KEY_Q):
    #    quit()
    if game.finished:
        game.man_frame=(game.man_frame+0.05)%2
        cat.anim_frame=(cat.anim_frame+0.05)%2
        return
    if button_action() and not cat.is_sleeping:
        if game.ready_to_finish:
            game.finished=True
            pyxel.playm(1,0,True)
            return
        elif game.offset==TILEMAP_INITIAL_OFFSET and not cat.is_sleeping:
            if cat.has_chip and cat.base_tile==CAT_TILE:
                cat.has_chip=False
                ship.fixed=True
        advance_dialog()
    if game.offset==TILEMAP_INITIAL_OFFSET:
        ship.alert_frame=(ship.alert_frame+0.05)%2
    update_cat()
    # bot
    if game.offset==TILEMAP_INITIAL_OFFSET:
        if bot.tx!=bot.x:
            bot.x+=pyxel.sgn(bot.tx-bot.x)
        else:
            bot.timer-=1
            if bot.timer==0:
                bot.timer=pyxel.rndi(30,60)
                bot.tx=pyxel.rndi(0,64-8)
                if bot.tx>bot.x:
                    bot.dir=1
                else:
                    bot.dir=-1

def draw():
    pyxel.cls(0)
    # end screen
    if game.finished:
        pyxel.bltm(0,0, 2, 0,0, 64,64, 0)
        pyxel.text(12,27, 'thanks for', 7)
        pyxel.text(18,33, 'playing', 7)
        x,y=CAT_TILE
        x+=int(cat.anim_frame)
        pyxel.blt(8,48, 0, x*8,y*8,8,8, 0)
        x,y=MAN_TILE
        x+=int(game.man_frame)
        pyxel.blt(48,40, 0, x*8,y*8,8,16, 0)
        return
    # tilemap
    pyxel.bltm(0,0, 0, game.offset[0]*64,game.offset[1]*64, 64,64, 0)
    # ship
    if game.offset==TILEMAP_INITIAL_OFFSET:
        if not ship.fixed:
            if int(ship.alert_frame)==1:
                x,y=SHIP_ALERT_TILE
                pyxel.blt(16,24, 0, x*8,y*8,8,8, 0)
        else:
            x,y=SHIP_FIXED_TILE
            pyxel.blt(16,24, 0, x*8,y*8,8,8, 0)
            x,y=CHIP_TILE
            pyxel.blt(16,32, 0, x*8,y*8,8,8, 0)
    # bot
    if game.offset==TILEMAP_INITIAL_OFFSET:
        u,v=BOT_TILE[0]*8,BOT_TILE[1]*8
        w=8*bot.dir
        pyxel.blt(bot.x,bot.y, 0, u,v,w,8, 0)
    # dialog
    if dialog.started:
        who,txt,size_index=dialog.phrases[dialog.phrase_index]
        size=[32,40,56,64][size_index]
        hs=size/2
        if who=='cat':
            x,y=cat.x+4,cat.y
        else:
            x,y=bot.x+4,bot.y
        if x<hs:
            x=hs
        elif x>64-hs:
            x=64-hs
        pyxel.bltm(x-hs,y-16, 1, 0,size_index*16, 64,16, 0)
        pyxel.text(x-hs+7,y-16+6, txt, 7)
        if dialog.phrase_index==3 and not ship.fixed:
            x2,y2=CHIP_TILE[0]*8,CHIP_TILE[1]*8
            pyxel.blt(x+5,y-11, 0, x2,y2,8,8, 0)
        if dialog.hint_started:
            pyxel.text(10,2, 'press space', 7)
    if game.ready_to_finish:
        pyxel.text(10,2, 'press space', 7)
    # cat
    if cat.is_sleeping:
        u=SLEEPING_CAT_TILE[0]*8
        v=SLEEPING_CAT_TILE[1]*8
        w=8
        u+=8*int(cat.anim_frame)
    else:
        u=cat.base_tile[0]*8
        v=cat.base_tile[1]*8
        w=8*cat.dir
        u+=8*int(cat.anim_frame)
    pyxel.blt(cat.x,cat.y, 0, u,v,w,8, 0)
    if cat.has_chip:
        u,v=CHIP_TILE
        pyxel.blt(64-10,2, 0, u*8,v*8,8,8, 0)

pyxel.init(64,64,title="Cat's Space Quest",display_scale=5)
pyxel.load('main.pyxres')
pyxel.run(update,draw)

