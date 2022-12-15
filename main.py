import pygame as pg
from pygame import mixer
from pygame.locals import *
from pygame import font
import random 
import tkinter
import tkinter.messagebox
import pickle
import mysql.connector as mysql
import os
from stat import S_IREAD, S_IRGRP, S_IROTH,S_IWUSR
from PIL import Image,ImageTk

logged = False
user_name = ""
passw = ""
all_time_score = 0

def register(conn,cursor,*userinfo):
    
    '''this function registeres user
      to users table in mysql'''
      
    username = userinfo[0]  
    password = userinfo[1]

    try:
        cursor.execute("insert into users values('{}','{}',0);".format(username,password))
        tkinter.messagebox.showinfo("Successfull","User registered successfully.")
        print("done")
    except:
        tkinter.messagebox.showinfo("Error","An error occured.")
        
    Name_Entry.delete("0","end")
    Pass_Entry.delete("0","end")
    conn.commit()
    conn.close()
    
def login(conn,userinfo):
    
    '''This function sets cokkie at users desktop
       to ensure that user stays logged in from next time
       basically making file and storing data '''
       
    global user_name
    global passw
    global all_time_score
    global logged

    with open("Player_data.txt","wb") as file:
        pickle.dump(userinfo,file)
    os.chmod("./Player_data.txt", S_IREAD|S_IRGRP|S_IROTH)
    user_name = userinfo[0][0]
    passw = userinfo[0][1]
    all_time_score = userinfo[0][2]
    win.destroy()
    logged = True
    conn.close()

def check_user():
    
    '''This function checks if user has entered right
       data and logins user basis of login state'''
       
    conn = mysql.connect(host="localhost",user= "root",passwd = "dhillon",database = "udta_panchi")
    cursor = conn.cursor()
    username = Name_Entry.get().strip()
    password = Pass_Entry.get().strip()
    
    if username == "":
        tkinter.messagebox.showinfo("Username","Username is required.")
    elif password == "":
        tkinter.messagebox.showinfo("Password","Password is required.")
        
    log_state = sign_btn.cget('text')
    cursor.execute("select * from users where username = '{}' and password = '{}';".format(username,password))
    user = cursor.fetchall()
    
    if log_state == "Sign Up":
        if len(user) == 0:
            register(conn,cursor,username,password)
        elif username != "" and password != "":
            tkinter.messagebox.showinfo("Error","Username is already taken.")
        
    elif log_state == "   Login":
        if len(user)>0:
            login(conn,user)
        else:
            tkinter.messagebox.showinfo("Try Sign Up","User not found.")

def change_log_state():
    
    '''To change user login state'''
    
    if log_btn.cget("text") == "Login":
        main_label.configure(text=" Login ")
        sign_btn.config(text="   Login")
        label1.config(text="Not a user ?")
        log_btn.config(text="Sign Up")
        
    elif log_btn.cget("text") == "Sign Up":
        main_label.configure(text="Sign Up")
        sign_btn.config(text="Sign Up")
        label1.config(text="Already a user?")
        log_btn.config(text="Login")

def toggle_password():
    
    '''This function  enables to
       see password or hide it'''
    
    if Pass_Entry.cget('show') == '':
        Pass_Entry.config(show='*')
        toggle_btn.config(image= hide)
    else:
        Pass_Entry.config(show='')
        toggle_btn.config(image= show)

#checking if user is already logged by checking the file we already saved as cokkie
file_exists = os.path.exists("./Player_data.txt")
if file_exists:
    with open("Player_data.txt","rb") as file:
        user_info = pickle.load(file)
    user_name = user_info[0][0]
    passw = user_info[0][1]
    all_time_score = user_info[0][2]
    logged = True

else:
    #setting screen for user to log in
    win = tkinter.Tk()
    win.title("Sign Up")
    win.geometry("400x700")
    win.resizable(0,0)
    
    background = Image.open("sprites/login.jpg")
    background = background.resize((400,700), Image.ANTIALIAS)
    background = ImageTk.PhotoImage(background)
    background_pl = tkinter.Label(image = background)
    background_pl.place(x = 0,y  =0)
    
    hide = Image.open("sprites/hide.png")
    hide = hide.resize((32,32), Image.ANTIALIAS)
    hide = ImageTk.PhotoImage(hide)
    
    show = Image.open("sprites/show.png")
    show = show.resize((32,32), Image.ANTIALIAS)
    show = ImageTk.PhotoImage(show)
    
    main_label = tkinter.Label(text=" Sign Up ",fg = "black",bg ="#94FDFF",font= ("Arial bold",20))
    main_label.place(x = 150,y = 60)
    
    label1 = tkinter.Label(text="Username",fg = "black",background="white",font= ("Arial bold",15))
    label1.place(x = 50,y = 271)
    
    Name_Entry = tkinter.Entry(font = ("Arial",20),border = 0)
    Name_Entry.place(x = 50,y=300.5)

    label2 = tkinter.Label(text="Password",fg = "black",bg="white",font= ("Arial bold",15))
    label2.place(x = 50,y = 349)
    
    Pass_Entry  = tkinter.Entry(font = ("Arial",20),show="*",border=0)
    Pass_Entry.place(x = 50,y=379.9)
    
    toggle_btn = tkinter.Button(image=hide,bg ="white",border=0,activebackground="white",command = lambda : toggle_password())
    toggle_btn.place(x = 320,y = 370)
    
    sign_btn = tkinter.Button(text="Sign Up",bg="#38B6FF",font=("Arial bold",13),activebackground="#38B6FF",border=0,command=lambda : check_user())
    sign_btn.place(x = 160,y=504)
    
    label1 = tkinter.Label(text="Already a user? ",fg = "black",bg="white",activebackground="white",font= ("Arial bold",13))
    label1.place(x = 90,y = 443)
    
    log_btn = tkinter.Button(text="Login",font=("Arial bold",11),bg="white",border=0,fg="black",command=lambda :change_log_state())
    log_btn.place(x = 230,y=442)
    win.mainloop()

if logged:
    
    #Defining some variables to use for player speed etc.
    scr_size = height,width = 400,700
    jump = False
    gravity = 3
    jump_height = 25
    speed = jump_height
    count = 0
    max_count = 0

    # y positions for pipe generation
    y_pos = [i for i in range(60,300,15)]

    #initiating pygame functions
    pg.init()
    mixer.init()
    
    #getting user postion and other top players 
    conn = mysql.connect(host="localhost",user= "root",passwd = "dhillon",database = "udta_panchi")
    cursor = conn.cursor()
    cursor.execute("select * from users order by score desc;")
    top_players = cursor.fetchall()
    player_rank = top_players.index((user_name,passw,all_time_score))
    conn.close()
    
    #setting screen
    screen = pg.display.set_mode(scr_size)
    pg.display.set_caption("Udta Panchi")

    #setting game icon
    pygame_icon = pg.image.load("sprites/flappy_bird.png")
    pg.display.set_icon(pygame_icon)
    
    #loading flappy bird images
    idle_flappy = pg.image.load("sprites/flappy_bird.png")
    idle_flappy = pg.transform.scale(idle_flappy,(50,35))
    idle_flappy1 = idle_flappy.get_rect(midleft =(175,250))

    #loading pipe images
    pipe = pg.image.load("sprites/pipe.png")
    pipe = pg.transform.scale(pipe,(80,400))
    pipe1 = pipe.get_rect(bottomleft =(400,900))

    piper = pg.image.load("sprites/pipe.png")
    piper = pg.transform.scale(piper,(80,400))
    piper = pg.transform.rotate(piper,180)
    piper1 = piper.get_rect(bottomleft =(400,300))
    
    pipe_dup = pg.image.load("sprites/pipe2.png")
    pipe_dup = pg.transform.scale(pipe_dup,(80,400))
    pipe_dup1 = pipe_dup.get_rect(bottomleft =(600,700))

    piper_dup = pg.image.load("sprites/pipe2.png")
    piper_dup = pg.transform.scale(piper_dup,(80,400))
    piper_dup = pg.transform.rotate(piper_dup,180)
    piper_dup1 = piper_dup.get_rect(bottomleft =(600,100))
    
    #coin image
    coin = pg.image.load("sprites/coin.png")
    coin = pg.transform.scale(coin,(45,45))
    coin1 = coin.get_rect(center =(435,400))
    
    coin_dup = pg.image.load("sprites/coin.png")
    coin_dup = pg.transform.scale(coin,(45,45))
    coin_dup1 = coin_dup.get_rect(center =(635,200))
    
    #leaderboard screen image
    rank = pg.image.load("sprites/ranking-star-2.png")
    rank = pg.transform.scale(rank,(30,30))
    rank1 = rank.get_rect(center =(30,25))
    
    leader = pg.image.load("sprites/bgr.png")
    leader = pg.transform.scale(leader,(400,450))
    leader1 = leader.get_rect(midleft =(0,350))
    
    #logout image
    logout = pg.image.load("sprites/logout.png")
    logout = pg.transform.scale(logout,(20,20))
    logout1 = logout.get_rect(center =(366,27))
    
    #setting screen images
    gear = pg.image.load("sprites/gear.svg")
    gear = pg.transform.scale(gear,(20,20))
    gear1 = gear.get_rect(center =(81,27))

    check = pg.image.load("sprites/check.png")
    check = pg.transform.scale(check,(25,25))
    
    cross = pg.image.load("sprites/xmark.png")
    cross = pg.transform.scale(cross,(25,25))
    
    square = pg.image.load("sprites/square.png")
    square = pg.transform.scale(square,(35,35))
    
    #background images
    bg = pg.image.load("sprites/bg2.png")
    bg = pg.transform.scale(bg,(400,720))
    bg1 = bg.get_rect()
    bg1.center = 200,300

    ground = pg.image.load("sprites/ground.png")
    ground = pg.transform.scale(ground,(1200,50))
    ground1 = ground.get_rect()
    ground1.center = 600,680
    
    ground_dup = pg.image.load("sprites/ground.png")
    ground_dup = pg.transform.scale(ground,(1200,50))
    ground_dup1 = ground.get_rect()
    ground_dup1.center = 1000,680

    #importing all fonts
    font_rank = pg.font.Font('fonts/Aberforth Rough.ttf', 26) 
    font_flappy = pg.font.Font('fonts/flappybirdy.ttf', 80)
    font_small = pg.font.Font('fonts/Inter-Regular.ttf', 22)
    font_big = pg.font.Font('fonts/Ringofkerry-Egyr.otf', 22)
    font_small2 = pg.font.Font('fonts/Ringofkerry-Egyr.otf', 18)

    Game_Name = font_flappy.render('      Udta Panchi      ', True, (215, 180, 0),(255,255,255))
    Game_Name_loc = Game_Name.get_rect()
    Game_Name_loc.center = 200,120

    Game_over = font_flappy.render(' G a m e   O v e r ', False, (225, 0, 0),(255,255,255))
    Game_over_loc = Game_over.get_rect()
    Game_over_loc.center = 200,200

    restart_txt = font_small.render('> Press R to RESTART ', True, (255,0, 0))
    restart_txt_loc = restart_txt.get_rect()
    restart_txt_loc.center = 195,400

    pause_txt = font_rank.render('> Press P to PAUSE ', True, (255, 0, 0))
    pause_txt_loc = restart_txt.get_rect()
    pause_txt_loc.center = 195,450

    start_txt = font_rank.render('> Press SPACEBAR to START ', True, (255, 0, 0))
    start_txt_loc = start_txt.get_rect()
    start_txt_loc.center = 210,400
    
    setting_1 = font_rank.render(' Background Music ', True, (255, 0, 0))
    setting_1_loc = start_txt.get_rect()
    setting_1_loc.center = 250,240
    
    setting_2 = font_rank.render(' Sound Effects ', True, (255, 0, 0))
    setting_2_loc = start_txt.get_rect()
    setting_2_loc.center = 250,300
    
    user_msg = font_rank.render('Hello, '+user_name, True, (255, 255, 0))
    user_msg_loc = user_msg.get_rect()
    user_msg_loc.center = 200,300

    #clock object for fps control in game
    clock = pg.time.Clock()

    #game screen showing variables
    q = False
    running = True
    gameover = False
    game_pause = False
    menu = True
    coin_collision = False
    ranking_scr = False
    show_dup = False
    coin_coll_dup = False
    ground_dup_show = False
    setting_scr = False
    check_mark = True
    check_mark2 = True
    
    #all music for game
    mixer.music.load("sound/back_music.mp3")
    mixer.music.set_volume(0.05)
    mixer.music.play(-1)

    coin_sound = pg.mixer.Sound("sound/coin-sound.wav")
    mixer.Sound.set_volume(coin_sound,0.03)
                                        
    whoosh = pg.mixer.Sound("sound/whoo.wav")
    mixer.Sound.set_volume(whoosh,4)

    gameover_sound = pg.mixer.Sound("sound/game-over.wav")
    mixer.Sound.set_volume(gameover_sound,0.1)

    #game runs here
    while running:
        
        #getting mouse position of user
        mouse = pg.mouse.get_pos()
        
        #start navigating menu
        if menu:
            screen.blit(bg,bg1)
            screen.blit(idle_flappy,idle_flappy1)
            screen.blit(Game_Name,Game_Name_loc)
            screen.blit(start_txt,start_txt_loc)
            screen.blit(pause_txt,pause_txt_loc)
            screen.blit(user_msg,user_msg_loc)
            count = 0
            
        #when game is started
        if q == False and menu == False and gameover == False:
            #moving pipes along x axis
            pipe1.x -= 2
            piper1.x -= 2
            coin1.x -= 2

            #moving bird to down
            idle_flappy1.y += gravity
            
            #if bird collides with screen ends game ends
            if idle_flappy1.y >= 550 :
                if check_mark2:
                    mixer.Sound.play(gameover_sound)
                gameover = True
            elif idle_flappy1.y <= 0 :
                if check_mark2:
                    mixer.Sound.play(gameover_sound)
                gameover = True
                
            #if jumping then this scenario applies
            if jump:
                idle_flappy1.y -= speed 
                speed -= gravity
                
                if speed <= 0 :
                    jump = False
                    speed = jump_height

            #pipe randomly generating code 
            if pipe1.x == -80:
                coin_collision = False
                n = random.choice(y_pos)
                piper1 = piper.get_rect(bottomleft =(400,n))
                pipe1 = pipe.get_rect(bottomleft = (400,n + 600))
                coin1 = coin.get_rect(center =(435,n + 100))

            if pipe1.x == 210:
                coin_collision = False
                count += 1
                if check_mark2:
                    mixer.Sound.play(coin_sound)
            
            if pipe_dup1.x == 200:
                count += 1
                if check_mark2:
                    mixer.Sound.play(coin_sound)
                
            if pipe1.x == 150:
                coin_coll_dup = False
                l = random.choice(y_pos)
                show_dup = True
                piper_dup1 = piper_dup.get_rect(bottomleft =(400,l))
                pipe_dup1 = pipe_dup.get_rect(bottomleft = (400,l + 600))
                coin_dup1 = coin_dup.get_rect(center =(435,l + 100))

            #if player collide with pipes game ends
            if idle_flappy1.colliderect(pipe1) or idle_flappy1.colliderect(pipe_dup1) or idle_flappy1.colliderect(piper1) or idle_flappy1.colliderect(piper_dup1):
                if check_mark2:    
                    mixer.Sound.play(gameover_sound)
                gameover = True
                
            #if player collides with coins 
            elif idle_flappy1.colliderect(coin1):
                coin_collision = True
                
            elif idle_flappy1.colliderect(coin_dup1):
                coin_coll_dup = True

            screen.blit(bg,bg1)
            screen.blit(idle_flappy,idle_flappy1)
            screen.blit(pipe,pipe1)
            screen.blit(piper,piper1)
            
            #Making coin disappear after collision with player
            if coin_collision == False:
                screen.blit(coin,coin1)
            if coin_coll_dup == False and show_dup == True:
                screen.blit(coin_dup,coin_dup1)

            #duplicate pipes
            if show_dup == True:
                pipe_dup1.x -= 2
                piper_dup1.x -= 2
                coin_dup1.x -= 2
                
                screen.blit(pipe_dup,pipe_dup1)
                screen.blit(piper_dup,piper_dup1)
            
            #showing score
            Score_text = font_rank.render(' Score : '+str(count)+" ", True, (255,255,255),(0,0,0))
            Score_loc = Score_text.get_rect()
            Score_loc.center = 330,30
            screen.blit(Score_text,Score_loc)
        
        #if game is paused by player
        if game_pause and gameover == False and menu == False:
            
            screen.blit(idle_flappy,idle_flappy1)
            screen.blit(pipe,pipe1)
            screen.blit(piper,piper1)
            screen.blit(pipe_dup,pipe_dup1)
            screen.blit(piper_dup,piper_dup1)
            
            if coin_collision == False:
                screen.blit(coin,coin1)
            if coin_coll_dup == False:
                screen.blit(coin_dup,coin_dup1)
                
            restart_txt = font_rank.render('> Press R to RESTART ', True, (255, 0, 0))
            screen.blit(Score_text,Score_loc)
            screen.blit(restart_txt,restart_txt_loc)
            
            q = True
            text = font_flappy.render('Paused', True, (255, 215, 0))
            text_loc = text.get_rect()
            text_loc.center = 200,200
            screen.blit(text,text_loc)
            
        if gameover:
            screen.blit(bg,bg1)
            screen.blit(Game_over,Game_over_loc)
            
            #updating databases on basis of score
            if count>max_count:
                max_count = count
                if max_count>all_time_score:
                    all_time_score = max_count
                    conn = mysql.connect(host="localhost",user= "root",passwd = "dhillon",database = "udta_panchi")
                    cursor = conn.cursor()
                    cursor.execute("Update users set score = {} where username = '{}';".format(all_time_score,user_name))
                    cursor.execute("select * from users order by score desc;")
                    top_players = cursor.fetchall()
                    player_rank = top_players.index((user_name,passw,all_time_score))
                    conn.commit()
                    conn.close()
                    
            
            Score_text = font_rank.render('   Score : '+str(count)+"   ", True, (255, 255, 255),(0,0,0))
            Score_loc = Score_text.get_rect()
            Score_loc.center = 200,270
            screen.blit(Score_text,Score_loc)
            Score_text = font_rank.render('   high Score : '+str(all_time_score)+"   ", True, (255, 255, 255),(0,0,0))
            Score_loc = Score_text.get_rect()
            Score_loc.center = 200,320
            screen.blit(Score_text,Score_loc)
            
            restart_txt = font_rank.render('> Press 0 for MENU ', True, (255, 0, 0))
            screen.blit(restart_txt,restart_txt_loc)
        
        #while player is on leaderboards screen
        if ranking_scr and not game_pause:
            screen.blit(bg,bg1)
            screen.blit(leader,leader1)
            y = 305
            
            #showing top players on basis of scores
            for i in range(0,4):
                x = 170
                color = (10,100,119)
                
                if top_players[i] == (user_name,passw,all_time_score):
                    color = (0,0,0)
                for j in range(0,4,2):
                    player_txt = font_rank.render("{}".format(top_players[i][j]), True,color)
                    player_txt1 = player_txt.get_rect()
                    player_txt1.center = x,y
                    screen.blit(player_txt,player_txt1)
                    x += 170
                y+= 52
                
            player_txt = font_rank.render("{}.".format(player_rank+1), True, (255,100,0))
            player_txt1 = player_txt.get_rect()
            player_txt1.center = 50,510
            screen.blit(player_txt,player_txt1)
            player_txt = font_rank.render("{}".format(user_name), True, (255,100,0))
            player_txt1 = player_txt.get_rect()
            player_txt1.center = 170,510
            screen.blit(player_txt,player_txt1)
            player_txt = font_rank.render("{}".format(all_time_score), True, (255,100,0))
            player_txt1 = player_txt.get_rect()
            player_txt1.center = 340,510
            screen.blit(player_txt,player_txt1)
        
        #while player is on settings screen
        if setting_scr:
            screen.blit(bg,bg1)
            
            cross1 = cross.get_rect(center =(85,240))
            check1 = check.get_rect(center =(85,240))
            square1 = square.get_rect(center =(85,240))
            
            screen.blit(square,square1)
            if check_mark:
                screen.blit(check,check1)
            else:
                screen.blit(cross,cross1)
            
            cross1 = cross.get_rect(center =(85,300))
            check1 = check.get_rect(center =(85,300))
            square1 = square.get_rect(center =(85,300))
            
            screen.blit(square,square1)
            if check_mark2:
                screen.blit(check,check1)
            else:
                screen.blit(cross,cross1)
                
            screen.blit(setting_1,setting_1_loc)
            screen.blit(setting_2,setting_2_loc)
        
        #making ground move along x axis
        if not ranking_scr and not gameover and not game_pause and not setting_scr:
            ground1.x -= 2
            if ground1.x == -770:
                ground_dup_show = True
            if ground_dup_show:
                ground_dup1.x -= 2
            if ground_dup1.x == -600:
                ground1 = ground.get_rect()
                ground1.center = 0,680
                ground_dup1 = ground.get_rect()
                ground_dup1.center = 1000,680
                ground_dup_show = False 
                
        #catching all events of keyboard
        for event in pg.event.get():
            if event.type == pg.QUIT:
                q = True
                running = False
                
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    setting_scr = False
                    ranking_scr = False
                    jump = True
                    menu = False
                    if gameover == False:
                        if check_mark2:
                            mixer.Sound.play(whoosh)
                        
                if event.key == pg.K_0:
                    setting_scr = False
                    ranking_scr = False
                    game_pause = False
                    gameover = False
                    menu = True
                    q = False
                    coin_collision = False
                    coin_coll_dup = False
                    idle_flappy1 = idle_flappy.get_rect(midleft =(175,250))
                    pipe1 = pipe.get_rect(bottomleft =(400,900))
                    piper1 = piper.get_rect(bottomleft =(400,300))
                    coin1 = coin.get_rect(center =(435,400))
                    
                    coin_dup1 = coin_dup.get_rect(center =(1000,0))
                    piper_dup1 = piper_dup.get_rect(bottomleft =(1000,0))
                    pipe_dup1 = pipe_dup.get_rect(bottomleft =(1000,0))

                if event.key == pg.K_p and gameover!=True and menu!= True:
                    setting_scr = False
                    ranking_scr = False
                    game_pause = True

                if event.key == pg.K_r:
                    setting_scr = False
                    game_pause = False
                    ranking_scr = False
                    q = False
                    
            if event.type == pg.MOUSEBUTTONDOWN:
                #if clicked on leaderboard button
                if 10 <= mouse[0] <= 50 and 10 <= mouse[1] <= 45:
                    setting_scr = False
                    if ranking_scr == False:
                        ranking_scr = True
                    else:
                        ranking_scr = False
                        
                if menu or gameover:
                    #if clicked on settings button
                    if 65 <= mouse[0] <= 100  and 10 <= mouse[1] <= 45:
                        ranking_scr = False
                        if setting_scr == False:
                            setting_scr = True
                        else:
                            setting_scr = False
                            
                    #if clicked on logout button
                    if 350 <= mouse[0] <= 385 and 10 <= mouse[1] <= 45:
                        running = False
                        os.chmod("./player_data.txt", 0o777)
                        os.remove("./player_data.txt")
                        pg.quit()
                        
                #if clicked on setting's button
                if setting_scr:
                    if 72 <= mouse[0] <= 100  and 225 <= mouse[1] <= 255:
                        if check_mark:
                            check_mark = False
                            mixer.music.pause()
                        else:
                            check_mark = True
                            mixer.music.unpause()
                            
                    if 72 <= mouse[0] <= 100  and 285 <= mouse[1] <= 315:
                        if check_mark2:
                            check_mark2 = False
                        else:
                            check_mark2 = True   
                            
        #fps control 
        if count<100:
            clock.tick(80+count/3)
        else:
            clock.tick(120)
            
        #drawing rectangle for leaderboard button
        if 10 <= mouse[0] <= 50 and 10 <= mouse[1] <= 45:
            pg.draw.rect(screen,(220,220,220),[10,10,40,35])
        else:
            pg.draw.rect(screen,(255,255,255),[10,10,40,35])
            
        #drawing rectangle for settings button
        if menu or gameover:
            if 65 <= mouse[0] <= 100  and 10 <= mouse[1] <= 45:
                pg.draw.rect(screen,(220,220,220),[65,10,35,35])
            else:
                pg.draw.rect(screen,(255,255,255),[65,10,35,35])
            screen.blit(gear,gear1)
            
        #logout button
        if menu or gameover:
            if 350 <= mouse[0] <= 385 and 10 <= mouse[1] <= 45:
                pg.draw.rect(screen,(220,220,220),[350,10,35,35])
            else:
                pg.draw.rect(screen,(255,255,255),[350,10,35,35])
            screen.blit(logout,logout1)

        screen.blit(rank,rank1)
        screen.blit(ground,ground1)
        screen.blit(ground_dup,ground_dup1)

        #updating screen constantly
        pg.display.update()

    #exit game
    if q == True :
        
        #updating file before signing player out
        os.chmod("./Player_data.txt", S_IWUSR|S_IREAD)
        with open("./Player_data.txt","wb") as file:
            pickle.dump([(user_name,passw,all_time_score)],file)
        os.chmod("./Player_data.txt", S_IREAD|S_IRGRP|S_IROTH)
            
        pg.quit()