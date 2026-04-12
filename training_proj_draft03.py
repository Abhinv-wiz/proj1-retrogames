import pygame, random, sys
pygame.init()
W,H=400,500
scr=pygame.display.set_mode((W,H));pygame.display.set_caption("Game.exe")
try:
    bg = pygame.image.load("pixel.jpg")
    bg = pygame.transform.scale(bg, (W, H))
except Exception:
    bg = None
clock=pygame.time.Clock()

WHITE,BLACK,GRAY,DARK,RED,BLUE,BROWN=(255,255,255),(0,0,0),(90,90,90),(40,40,40),(200,60,60),(60,120,220),(139,69,19)
GREEN=(60,200,80);DARK_GREEN=(30,140,50);YELLOW=(240,210,40)
f_big=pygame.font.SysFont("courier",24,True)
f_mid=pygame.font.SysFont("courier",18,True)
f_small=pygame.font.SysFont("courier",14)
f_term=pygame.font.SysFont("terminal",16,True)

screen_mode="menu";help_open=False
btn_w,btn_h=260,40
menu_btns={}
y0=140
for i,(k,txt) in enumerate([("tic","Tic Tac Toe"),("click","Click the Button!"),("doge","Doge the Block"),("snake","Snake")]):
    menu_btns[k]=(pygame.Rect((W-btn_w)//2,y0+i*50,btn_w,btn_h),txt)
help_btn=pygame.Rect(W-90,H-40,80,30);help_close=pygame.Rect(0,0,0,0)

def draw_btn(r,txt,font=f_mid,color=DARK,txt_col=WHITE):
    pygame.draw.rect(scr,color,r)
    pygame.draw.rect(scr,GRAY,r,2)
    t=font.render(txt,True,txt_col);scr.blit(t,t.get_rect(center=r.center))

# Tic Tac Toe
tic_board=[[""]*3 for _ in range(3)]
tic_player="X";tic_status="";tic_reset_at=0
grid_rect=pygame.Rect(50,110,300,300)
back_btn=pygame.Rect(10,H-40,90,30)

def tic_reset():
    global tic_board,tic_player,tic_status,tic_reset_at
    tic_board=[[""]*3 for _ in range(3)];tic_player="X";tic_status="";tic_reset_at=0

def tic_winner():
    b=tic_board
    for i in range(3):
        if b[i][0] and b[i][0]==b[i][1]==b[i][2]:return b[i][0]
        if b[0][i] and b[0][i]==b[1][i]==b[2][i]:return b[0][i]
    if b[0][0] and b[0][0]==b[1][1]==b[2][2]:return b[0][0]
    if b[0][2] and b[0][2]==b[1][1]==b[2][0]:return b[0][2]
    if all(b[r][c] for r in range(3) for c in range(3)):return "Tie"
    return None

def draw_tic():
    scr.fill((30,30,30))
    t=f_big.render("Tic Tac Toe",True,WHITE);scr.blit(t,t.get_rect(center=(W//2,60)))
    for i in range(1,3):
        x=grid_rect.x+i*grid_rect.w//3
        y=grid_rect.y+i*grid_rect.h//3
        pygame.draw.line(scr,WHITE,(x,grid_rect.y),(x,grid_rect.bottom),2)
        pygame.draw.line(scr,WHITE,(grid_rect.x,y),(grid_rect.right,y),2)
    for r in range(3):
        for c in range(3):
            m=tic_board[r][c]
            if m:
                t=f_big.render(m,True,WHITE)
                cx=grid_rect.x+c*grid_rect.w//3+grid_rect.w//6
                cy=grid_rect.y+r*grid_rect.h//3+grid_rect.h//6
                scr.blit(t,t.get_rect(center=(cx,cy)))
    s=tic_status or f"Player {tic_player}'s turn"
    scr.blit(f_small.render(s,True,WHITE),(50,430))
    draw_btn(back_btn,"Back",f_small)

def tic_click(pos):
    global screen_mode,tic_player,tic_status,tic_reset_at
    if back_btn.collidepoint(pos):
        tic_reset();screen_mode="menu";return
    if tic_reset_at or not grid_rect.collidepoint(pos):return
    c=(pos[0]-grid_rect.x)*3//grid_rect.w
    r=(pos[1]-grid_rect.y)*3//grid_rect.h
    if tic_board[r][c]=="": 
        tic_board[r][c]=tic_player
        w=tic_winner()
        if w:
            tic_status="It's a Tie!" if w=="Tie" else f"Player {w} Wins!"
            tic_reset_at=pygame.time.get_ticks()+1500
        else: tic_player="O" if tic_player=="X" else "X"

#Doge the Block
doge_player=pygame.Rect(130,350,40,40)
doge_block=pygame.Rect(random.randint(0,260),0,40,40)
doge_score=0;doge_over=False;doge_back=pygame.Rect(0,0,0,0)
DOGE_SPEED=6

def doge_reset():
    global doge_player,doge_block,doge_score,doge_over,doge_back
    doge_player.update(130,350,40,40)
    doge_block.update(random.randint(0,260),0,40,40)
    doge_score=0;doge_over=False;doge_back=pygame.Rect(0,0,0,0)

def doge_update():
    global doge_score,doge_over,doge_back
    if doge_over:return
    doge_block.y+=DOGE_SPEED
    if doge_block.colliderect(doge_player): 
        doge_over=True;doge_back=pygame.Rect(100,270,200,40);return
    if doge_block.bottom>=400:
        doge_score+=1
        doge_block.y=0;doge_block.x=random.randint(0,260)

def doge_key(key):
    if doge_over:return
    if key==pygame.K_LEFT and doge_player.x>0:doge_player.x-=20
    if key==pygame.K_RIGHT and doge_player.right<300:doge_player.x+=20

def doge_click(pos):
    global screen_mode
    if doge_over and doge_back.collidepoint(pos):
        doge_reset();screen_mode="menu"

def draw_doge():
    scr.fill(BLACK)
    area=pygame.Rect((W-300)//2,40,300,400)
    pygame.draw.rect(scr,(20,20,20),area)
    p=doge_player.move(area.x,0);b=doge_block.move(area.x,0)
    pygame.draw.rect(scr,BLUE,p);pygame.draw.rect(scr,RED,b)
    scr.blit(f_mid.render(f"Score: {doge_score}",True,WHITE),(area.x,area.bottom+8))
    if doge_over:
        t=f_big.render("Game Over!",True,WHITE)
        scr.blit(t,t.get_rect(center=(W//2,220)))
        draw_btn(doge_back,"Back to Menu")

#Click game 
click_count=0
click_btn=pygame.Rect(80,200,240,60)

def draw_click():
    scr.fill((30,30,30))
    scr.blit(f_big.render("Click Counter",True,WHITE), (110,80))
    scr.blit(f_big.render(f"Clicks: {click_count}",True,WHITE),(120,130))
    draw_btn(click_btn,"Click Me!",f_big)
    draw_btn(back_btn,"Back",f_small)

def click_game_click(pos):
    global click_count,screen_mode
    if click_btn.collidepoint(pos):click_count+=1
    elif back_btn.collidepoint(pos):screen_mode="menu"

# ── Snake ──────────────────────────────────────────────────────────────────────
SNAKE_CELL   = 20          # px per grid cell
SNAKE_COLS   = 15          # cells wide  (15*20 = 300px)
SNAKE_ROWS   = 20          # cells tall  (20*20 = 400px)
SNAKE_AREA   = pygame.Rect((W - SNAKE_COLS*SNAKE_CELL)//2, 40,
                            SNAKE_COLS*SNAKE_CELL, SNAKE_ROWS*SNAKE_CELL)
SNAKE_TICK   = 120         # ms between steps (lower = faster)

snake_body   = []          # list of (col, row) tuples, head first
snake_dir    = (1, 0)      # (dc, dr)
snake_next   = (1, 0)      # buffered input direction
snake_food   = (0, 0)
snake_score  = 0
snake_over   = False
snake_started= False       # waiting for first key press
snake_last_t = 0
snake_back   = pygame.Rect(0,0,0,0)
snake_retry  = pygame.Rect(0,0,0,0)

def _snake_free_cell():
    occupied = set(snake_body)
    while True:
        c = random.randint(0, SNAKE_COLS-1)
        r = random.randint(0, SNAKE_ROWS-1)
        if (c,r) not in occupied:
            return (c, r)

def snake_reset():
    global snake_body,snake_dir,snake_next,snake_food
    global snake_score,snake_over,snake_started,snake_last_t
    global snake_back,snake_retry
    mid_c, mid_r = SNAKE_COLS//2, SNAKE_ROWS//2
    snake_body  = [(mid_c, mid_r),(mid_c-1, mid_r),(mid_c-2, mid_r)]
    snake_dir   = (1, 0)
    snake_next  = (1, 0)
    snake_food  = _snake_free_cell()
    snake_score = 0
    snake_over  = False
    snake_started = False
    snake_last_t  = 0
    snake_back  = pygame.Rect(0,0,0,0)
    snake_retry = pygame.Rect(0,0,0,0)

def snake_key(key):
    global snake_next, snake_started
    mapping = {
        pygame.K_UP:    (0,-1), pygame.K_w: (0,-1),
        pygame.K_DOWN:  (0, 1), pygame.K_s: (0, 1),
        pygame.K_LEFT:  (-1,0), pygame.K_a: (-1,0),
        pygame.K_RIGHT: (1, 0), pygame.K_d: (1, 0),
    }
    if key in mapping:
        nd = mapping[key]
        # forbid 180-degree reversal
        if (nd[0] != -snake_dir[0]) or (nd[1] != -snake_dir[1]):
            snake_next = nd
            snake_started = True

def snake_update():
    global snake_dir,snake_food,snake_score,snake_over,snake_last_t
    global snake_back,snake_retry
    if snake_over or not snake_started: return
    now = pygame.time.get_ticks()
    if now - snake_last_t < SNAKE_TICK: return
    snake_last_t = now
    snake_dir = snake_next
    hc, hr = snake_body[0]
    nc, nr = hc + snake_dir[0], hr + snake_dir[1]
    # wall collision
    if not (0 <= nc < SNAKE_COLS and 0 <= nr < SNAKE_ROWS):
        snake_over = True
        snake_back  = pygame.Rect(W//2-110, 295, 100, 34)
        snake_retry = pygame.Rect(W//2+10,  295, 100, 34)
        return
    # self collision
    if (nc, nr) in snake_body:
        snake_over = True
        snake_back  = pygame.Rect(W//2-110, 295, 100, 34)
        snake_retry = pygame.Rect(W//2+10,  295, 100, 34)
        return
    snake_body.insert(0,(nc,nr))
    if (nc,nr) == snake_food:
        snake_score += 1
        snake_food = _snake_free_cell()
    else:
        snake_body.pop()

def draw_snake():
    scr.fill(BLACK)
    t = f_big.render("Snake", True, WHITE)
    scr.blit(t, t.get_rect(center=(W//2, 20)))
    pygame.draw.rect(scr, (15,15,15), SNAKE_AREA)
    pygame.draw.rect(scr, GRAY, SNAKE_AREA, 2)
    fc, fr = snake_food
    fx = SNAKE_AREA.x + fc*SNAKE_CELL
    fy = SNAKE_AREA.y + fr*SNAKE_CELL
    pygame.draw.rect(scr, WHITE, (fx+2, fy+2, SNAKE_CELL-4, SNAKE_CELL-4))
    for i,(bc,br) in enumerate(snake_body):
        bx = SNAKE_AREA.x + bc*SNAKE_CELL
        by = SNAKE_AREA.y + br*SNAKE_CELL
        color = WHITE if i==0 else GRAY
        pygame.draw.rect(scr, color, (bx+1, by+1, SNAKE_CELL-2, SNAKE_CELL-2))
    score_y = SNAKE_AREA.bottom + 6
    scr.blit(f_small.render(f"Score: {snake_score}", True, WHITE), (SNAKE_AREA.x, score_y))
    if not snake_started and not snake_over:
        hint = f_small.render("Arrow keys / WASD to start", True, GRAY)
        scr.blit(hint, hint.get_rect(center=(W//2, score_y+16)))
    draw_btn(back_btn, "Back", f_small)
    if snake_over:
        go = f_big.render("Game Over!", True, WHITE)
        sc = f_mid.render(f"Score: {snake_score}", True, GRAY)
        scr.blit(go, go.get_rect(center=(W//2,230)))
        scr.blit(sc, sc.get_rect(center=(W//2,265)))
        draw_btn(snake_back,  "Menu",  f_small)
        draw_btn(snake_retry, "Retry", f_small)

def snake_click(pos):
    global screen_mode
    if snake_over:
        if snake_back.collidepoint(pos):
            snake_reset(); screen_mode="menu"
        elif snake_retry.collidepoint(pos):
            snake_reset()
    elif back_btn.collidepoint(pos):
        snake_reset(); screen_mode="menu"

# main menu
def draw_menu():
    if bg:scr.blit(bg,(0,0))
    else:scr.fill(BLACK)
    t=f_big.render("🎮 Game Hub",True,BROWN)
    bar=pygame.Rect(0,40,W,50)
    pygame.draw.rect(scr,(43,10,4),bar);pygame.draw.rect(scr,BROWN,bar,3)
    scr.blit(t,t.get_rect(center=bar.center))
    for r,txt in menu_btns.values():draw_btn(r,txt)
    draw_btn(help_btn,"help!",f_mid,(220,220,220),BLACK)
    global help_close
    if help_open:
        pop=pygame.Rect(40,210,W-80,130)
        pygame.draw.rect(scr,(34,34,34),pop)
        pygame.draw.rect(scr,GRAY,pop,2)
        scr.blit(f_mid.render("How to Play",True,WHITE),(pop.x+20,pop.y+10))
        scr.blit(f_small.render("its not that hard lil bro T_T",True,WHITE),(pop.x+20,pop.y+50))
        help_close=pygame.Rect(pop.centerx-50,pop.bottom-40,100,30)
        draw_btn(help_close,"X Close",f_small)
    else:help_close=pygame.Rect(0,0,0,0)

#loop
running=True
while running: 
    clock.tick(60)
    now=pygame.time.get_ticks()
    if tic_reset_at and now>=tic_reset_at:tic_reset()
    if screen_mode=="doge":doge_update()
    if screen_mode=="snake":snake_update()
    for e in pygame.event.get():
        if e.type==pygame.QUIT:running=False
        elif e.type==pygame.KEYDOWN:
            if screen_mode=="doge":doge_key(e.key)
            if screen_mode=="snake":snake_key(e.key)
        elif e.type==pygame.MOUSEBUTTONDOWN and e.button==1:
            pos=e.pos
            if screen_mode=="menu":
                if help_open and help_close.collidepoint(pos):help_open=False
                elif help_btn.collidepoint(pos):help_open=True
                elif not help_open:
                    for key,(r,_) in menu_btns.items():
                        if r.collidepoint(pos):
                            if key=="doge":doge_reset()
                            if key=="snake":snake_reset()
                            screen_mode=key;break
            elif screen_mode=="tic":tic_click(pos)
            elif screen_mode=="doge":doge_click(pos)
            elif screen_mode=="click":click_game_click(pos)
            elif screen_mode=="snake":snake_click(pos)

    if screen_mode=="menu":draw_menu()
    elif screen_mode=="tic":draw_tic()
    elif screen_mode=="doge":draw_doge()
    elif screen_mode=="click":draw_click()
    elif screen_mode=="snake":draw_snake()
    pygame.display.flip()

pygame.quit();sys.exit()
