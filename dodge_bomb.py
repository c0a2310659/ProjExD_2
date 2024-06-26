
import os
import random
import sys
import time
import pygame as pg

WIDTH, HEIGHT = 1200, 600

DELTA = {  #移動量辞書
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0)
    }

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct:pg.rect) -> tuple[bool,bool]:
    yoko,tate = True,True
    if obj_rct.left < 0 or WIDTH < obj_rct.right: 
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    cry_img = pg.image.load("fig/8.png")

    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bd_img = pg.Surface((20,20))
    bd_img.set_colorkey((0,0,0,))
    pg.draw.circle(bd_img,(255,0,0),(10,10),10)
    bd_rct = bd_img.get_rect()
    bd_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)    
    vx,vy = +5,+5

    clock = pg.time.Clock()
    tmr = 0
    RIGHT_img = pg.transform.flip(kk_img, False, True)  #画像の反転を作成
    LEFT_img = kk_img
    """
    練習1コウカトン向き
    """
    img_dict = {
         (0, 0):pg.transform.rotozoom(LEFT_img, 0, 1.0),
         (0, -5):pg.transform.rotozoom(RIGHT_img, -90, 1.0),
         (+5, -5):pg.transform.rotozoom(RIGHT_img, 225, 1.0), 
         (+5, 0):pg.transform.rotozoom(RIGHT_img, 180, 1.0),
         (+5, +5):pg.transform.rotozoom(RIGHT_img, 135, 1.0),
         (0, +5):pg.transform.rotozoom(RIGHT_img, 90, 1.0),
         (-5, +5):pg.transform.rotozoom(LEFT_img, 45, 1.0),
         (-5, 0):pg.transform.rotozoom(LEFT_img, 0, 1.0),
         (-5, -5):pg.transform.rotozoom(LEFT_img, -45, 1.0)
    }

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
                return
        if kk_rct.colliderect(bd_rct):
            """
            GameOver後の処理
            """
            BG_img = pg.Surface((1200,600))
            BG_rct = BG_img.get_rect()

            pg.draw.rect(BG_img,(0,0,0),(0,1200,0,600))
            BG_img.set_alpha(200)
            screen.blit(BG_img,BG_rct)
            fonto = pg.font.Font(None,80)
            txt = fonto.render("Game Over",True,(255,255,255))  #Game Over 表示
            txt_rct = txt.get_rect()
            txt_rct.center = WIDTH/2,HEIGHT/2
            screen.blit(cry_img,[390,270])  #コウカトン
            screen.blit(cry_img,[780,270])
            screen.blit(txt, txt_rct)

            pg.display.update()
            print("Game Over")
            time.sleep(5)
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for k,v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] +=v[0]
                sum_mv[1] +=v[1]
        kk_img = img_dict[(sum_mv[0],sum_mv[1])]  #練習1

        #if key_lst[pg.K_UP]:
         #   sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
         #   sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
         #   sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
         #   sum_mv[0] += 5

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bd_rct.move_ip(vx,vy)
        screen.blit(bd_img, bd_rct)
        yoko, tate = check_bound(bd_rct)
        if not yoko:  
            vx *= -1
        if not tate: 
            vy *= -1
        pg.display.update() 
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
