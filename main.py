import tkinter
import pyautogui
import chore
import dictionary
import place_check
import event
import copy
import re
import random

map = []
tool = []
map_img = tkinter.PhotoImage
player_img = tkinter.PhotoImage
boo = True  #screenのscrollのbool値
scr_w,scr_h= pyautogui.size()
data_dict = dictionary.data_dict
map_move_list = ["A","B","G","I","M","l","C","D","W"]
event_list = ["d","g","t","v","k","b","m","P","?","N","w","h"]
item_list = ['貸出し済みの本', 'ボール','体重計の鍵','教室の鍵','音楽室の鍵']
walk_count = 0
music_count = 0
death_count = 0
# 辞書の内容は[map_path,image_path,image_size,image_position,player_position,player_location]
 
corrider_back_dict =dictionary.corrider_back_dict
# 辞書の内容は[image_position,player_location] 
stopper_i = 0

def new_game(): #最初のスタート画面
    global condition, location_name
    new_game_b.destroy()
    canvas.delete('BG_start')
    location_name = 'corrider'
    set_up(location_name) 
    condition = True    #key受付の有無
    root.bind('<KeyPress>',push)
    root.bind('<KeyRelease>',action)

def push(e):
    global key
    key = e.keysym

def action(e):
    global condition, tool, walk_count, music_count
    if condition:
        move_ls = ['Up','Down','Right','Left']
        if (music_count > 1) and (location_name == 'corrider'):
            map[1][9] = 'Y'
            map[2][9] = 'Y'
            map[3][9] = 'Y'
        if key in move_ls:
            move_proc(key)
            walk_count += 1
            if map[player_loc[1]][player_loc[0]] == 'o':
                if not "体育館" in tool:
                    tool.append("体育館")
            if (walk_count % 50 == 0) and (location_name == 'corrider'):
                if not "歩数" in tool:
                    tool.append("歩数")
                stopper(2000)
                root.after(2000,normal_death)
            
        if key == 'm':
            whole_map()
        if key == 'w':
            walk_count_decleare()
        if key == 'space':
            if map[player_loc[1]][player_loc[0]] == 'J':
                Jaby()
            if map[player_loc[1]][player_loc[0]] in map_move_list:
                chore.SE('./music/SE/ドアを開ける.mp3')
                screen_change_check()
            elif map[player_loc[1]][player_loc[0]] == 'H':
                if "本" in tool:
                    walk_count = 99
                    tool.remove("本")
                    if not '図書室' in tool:
                        tool.append('図書室')
                chore.SE('./music/SE/ドアを開ける.mp3')
                screen_change_check()
            elif (map[player_loc[1]][player_loc[0]] == 'Q') or (map[player_loc[1]][player_loc[0]] == 'U'):
                walk_count = 99
                tool.append("教室")
                chore.SE('./music/SE/ドアを開ける.mp3')
                screen_change_check()
            elif map[player_loc[1]][player_loc[0]] == 'E':
                if "体育館" in tool:
                    walk_count = 99
                    if "ボール" in tool:
                        tool.remove("ボール")
                chore.SE('./music/SE/ドアを開ける.mp3')
                screen_change_check()
            elif (map[player_loc[1]][player_loc[0]] == 'L') or (map[player_loc[1]][player_loc[0]] == 'R'):
                if not "職員室" in tool:
                    tool.append("職員室")
                normal_death()
            elif map[player_loc[1]][player_loc[0]] == 'Y':
                chore.SE('./music/SE/ドアを開ける.mp3')
                screen_change_check()
            elif map[player_loc[1]][player_loc[0]] in event_list:
                narration(map[player_loc[1]][player_loc[0]])
            
            if map[player_loc[1]][player_loc[0]] == 'X':
                if not "教室" in tool:
                    tool.append("教室")
                normal_death()
            if map[player_loc[1]][player_loc[0]] == 'T':
                if not "階段" in tool:
                    tool.append("階段")
                normal_death()


        if key == 'k':
            if (map[player_loc[1]][player_loc[0]] == "L") or (map[player_loc[1]][player_loc[0]] == "R"):
                chore.SE('./music/SE/木のドアをノック1.mp3')
                screen_change_check()

def stopper(time):
    global condition, stopper_i
    stopper_i += 1
    if stopper_i == time:
        stopper_i = 0
    else:
        condition = False
        root.after(1,stopper,time)


def walk_count_decleare():
    global condition, label
    condition = False
    label = tkinter.Label(root,text=str(walk_count),font=('游ゴシック',24))
    label.place(x=0,y=0)
    root.after(2500,count_delete)

def count_delete():
    global condition
    label.destroy()
    condition = True

def whole_map():
    global condition
    condition = False
    canvas.create_image(scr_w/2,scr_h/2,image=whole_map_img,tag='whole_map')
    root.after(2500,map_delete)

def Jaby():
    if ("教室の鍵" in tool) and ("体重計の鍵" in tool) and ("音楽室の鍵" in tool):
        narration('tako_clear')
    elif "教室" in tool:
        narration('tako_class')
    elif "階段" in tool:
        narration('tako_stairs')
    elif "職員室" in tool:
        narration('tako_teacher')
    elif "図書室" in tool:
        narration('tako_library')
    elif "体育館" in tool:
        narration('tako_gym')
    elif "歩数" in tool:
        narration('tako_walk')
    elif "鬼ごっこ" in tool:
        narration('tako_play')
    elif death_count > 10:
        narration()
    else:
        narration('tako_start')

def normal_death():
    global walk_count, condition, ghost_img
    walk_count = 0
    condition = False
    chore.music_quit()
    ghost_img = chore.resize('./img/ghost/back.png',scr_w/13,scr_h/13)
    canvas.create_image(scr_w/2,scr_h/2+scr_h/15,image=ghost_img,tag='ghost')
    chore.SE('./music/SE/死亡時テキスト.mp3')
    narration('death')
    root.after(1000,reset)

def reset():
    global location_name, condition, death_count, music_count
    condition = False
    for i in item_list:
        if i in tool:
            tool.remove(i)
    chore.SE('./music/SE/打撃8.mp3')
    canvas.create_image(scr_w/2,scr_h/2,image=death_img,tag='death')
    death_count += 1
    music_count = 0
    root.after(1000,black_out)

def black_out():
    global location_name, condition
    condition = False
    canvas.delete('all')
    #chore.SE('./music/SE/打撃8.mp3')
    location_name = 'corrider'
    #canvas.create_image(scr_w/2,scr_h/2,image=death_img,tag='death')
    root.after(1000,set_up,location_name)

def narration(signal):
    global condition, music_count
    def text_flow(counter):
        global label
        try:
            label.destroy()
        except:
            pass
        label = tkinter.Label(root,text=all_text[counter],font=('游ゴシック',24))   #labelの様式設定よろしくお願いします
        label.place(relx=11/60,rely=301/400)
        chore.SE('./music/SE/決定ボタンを押す7.mp3')                                     #位置指定お願いします
        if counter != len(all_text) -1:
            root.after(1500,text_flow,counter+1)
        else:
            root.after(1500,finish)
    def finish():
        global condition, tool
        label.destroy()
        canvas.delete('textbox')
        item, lost_item, extra_event_boo =event.event_resalt(signal)
        if not item in tool:
            tool.append(item)
        if lost_item in tool:
            tool.remove(lost_item)
        condition = True
        if extra_event_boo:
            develop(signal)
    condition = False
    if map[player_loc[1]][player_loc[0]] == 'h':
        music_count = 3
    all_text = event.call_text(signal).split('\n')
    canvas.create_image(scr_w/2,3*scr_h/4,image=textbox_img,tag='textbox')  #位置指定お願いします
    text_flow(0)
    
def develop(signal):
    if (signal == 'm') and ('本' in tool):
        narration('m2')
    if (signal == 'g') and ('貸出し済みの本' in tool):
        narration('g2')
    if (signal == 'k') and ('ボール' in tool):
        narration('k2')
    if (signal == '?') and ('謎の部屋の鍵' in tool):
        narration('?2')
    if signal =='t':
        map_change()    #出口をNに書き換える、倉庫をWに書き換える、鬼ごっこ開始
    #if signal == 'd':
    #    password()  #パスワード入力、あっていたらnarration('d_OK')、まちがっていたらnarration('d_NG')
    if (signal == 'd') and ('教室の鍵' in tool) and ('体重計の鍵' in tool) and ('音楽室の鍵' in tool):
        narration('d_SOS')
    if signal == '?2':
        global condition
        condition = False
        print(death_count)
        canvas.create_image(scr_w/2,45*scr_h/100,image=clear_img,tag='Clear')
        chore.music_quit()
        chore.SE('./music/BGM/教会の祈り.mp3')
          
def map_change():
    global ghost_loc, ghost_screen_loc
    map[5][1] = 'N'
    map[5][12] = 'W'
    ghost_loc = [12,5]
    ghost_screen_loc = [375*scr_w/1200+11*208*scr_w/5000,1013*scr_h/2000]   #指定求む
    chore.music_quit()
    chore.SE('./music/SE/ドアを蹴破る.mp3')
    root.after(1000,narration,'t2')
    root.after(2000,ghost_chase)
    root.after(2000,chore.BGM,'./music/SE/Chase_music.mp3')
    
def ghost_chase():
    global ghost_i, condition, ghost_screen_loc, ghost_img, walk_count
    ghost_i = 0
    print(ghost_loc,player_loc)
    num = random.randint(1,3)
    if (player_loc[1] < ghost_loc[1]) and (num == 1):    #Up
        ghost_loc[1] -= 1
        path = './img/ghost/back.png'
        ghost_img = chore.resize(path,scr_w/15,scr_h/15)
        canvas.create_image(ghost_screen_loc[0],ghost_screen_loc[1],image=ghost_img,tag='ghost')
        def move_ghost():
            global ghost_i, condition
            if not re.match('gym',location_name):
                canvas.delete('ghost')
                chore.BGM('./music/SE/探索.mp3')
            else:
                canvas.delete('ghost')
                ghost_screen_loc[1] -= 135*scr_h/18000
                canvas.create_image(ghost_screen_loc[0],ghost_screen_loc[1],image=ghost_img,tag='ghost')
                ghost_i += 1
                if ghost_i != 10:
                    root.after(20,move_ghost)
                else:
                    root.after(1,ghost_chase)
        move_ghost()
    elif (player_loc[1] > ghost_loc[1]) and (num == 1):  #Down
        ghost_loc[1] += 1
        path = './img/ghost/front.png'
        ghost_img = chore.resize(path,scr_w/15,scr_h/15)
        canvas.create_image(ghost_screen_loc[0],ghost_screen_loc[1],image=ghost_img,tag='ghost')
        def move_ghost():
            global ghost_i, condition
            if not re.match('gym',location_name):
                canvas.delete('ghost')
                chore.BGM('./music/SE/探索.mp3')
            else:
                canvas.delete('ghost')
                ghost_screen_loc[1] += 135*scr_h/18000
                canvas.create_image(ghost_screen_loc[0],ghost_screen_loc[1],image=ghost_img,tag='ghost')
                ghost_i += 1
                if ghost_i != 10:
                    root.after(20,move_ghost)
                else:
                    root.after(1,ghost_chase)
        move_ghost()
    elif (player_loc[0] > ghost_loc[0]) and (num == 2):  #Right
        ghost_loc[0] += 1
        path = './img/ghost/right.png'
        ghost_img = chore.resize(path,scr_w/15,scr_h/15)
        canvas.create_image(ghost_screen_loc[0],ghost_screen_loc[1],image=ghost_img,tag='ghost')
        def move_ghost():
            global ghost_i, condition
            if not re.match('gym',location_name):
                canvas.delete('ghost')
                chore.BGM('./music/SE/探索.mp3')
            else:
                canvas.delete('ghost')
                ghost_screen_loc[0] += 208*scr_w/50000
                canvas.create_image(ghost_screen_loc[0],ghost_screen_loc[1],image=ghost_img,tag='ghost')
                ghost_i += 1
                if ghost_i != 10:
                    root.after(20,move_ghost)
                else:
                    root.after(1,ghost_chase)
        move_ghost()
    elif (player_loc[0] < ghost_loc[0]) and (num == 2):  #left
        ghost_loc[0] -= 1
        path = './img/ghost/left.png'
        ghost_img = chore.resize(path,scr_w/15,scr_h/15)
        canvas.create_image(ghost_screen_loc[0],ghost_screen_loc[1],image=ghost_img,tag='ghost')
        def move_ghost():
            global ghost_i, condition
            if not re.match('gym',location_name):
                canvas.delete('ghost')
                chore.BGM('./music/SE/探索.mp3')
            else:
                canvas.delete('ghost')
                ghost_screen_loc[0] -= 208*scr_w/50000
                canvas.create_image(ghost_screen_loc[0],ghost_screen_loc[1],image=ghost_img,tag='ghost')
                ghost_i += 1
                if ghost_i != 10:
                    root.after(20,move_ghost)
                else:
                    root.after(1,ghost_chase)
        move_ghost()  
    elif (player_loc[0] == ghost_loc[0]) and (player_loc[1] == ghost_loc[1]):
        canvas.delete('ghost')
        canvas.delete('Player')
        condition = False
        walk_count = 0
        chore.music_quit()
        if not "鬼ごっこ" in tool:
            tool.append("鬼ごっこ")
        reset()
    else:
        ghost_chase()

def verify():
    global condition
    password = textbox.get()
    textbox.destroy()
    enter_button.destroy()
    if password == '7049':
        narration('d_OK')
    else:
        narration('d_NG')

def password():
    global condition, enter_button, textbox
    condition = False
    textbox = tkinter.Entry(width=40)
    textbox.place(x=2*scr_w/5,y=3*scr_h/5)  #位置指定頼む 
    enter_button = tkinter.Button(text='OK!',command=verify)
    enter_button.place(x=scr_w/2,y=2*scr_h/3)

def map_delete():
    global condition
    canvas.delete('whole_map')
    condition = True

def screen_change_check():
    global location_name
    check_boo, destination, vector = place_check.check(map[player_loc[1]][player_loc[0]],location_name)
    if check_boo:
        if vector:
            location_name = destination
            set_up(location_name)
        else:
            back_corrider_setup(location_name)
            location_name = destination

def move_proc(key):
    global condition, map_position, location_name, player_loc, player_screen_loc, player_img,tile_y,tile_x, i
    i = 0
    if key == 'Up' and map[player_loc[1]-1][player_loc[0]] != '1':
        condition = False
        player_loc[1] -= 1
        path = './img/player/back.png'
        player_img = chore.resize(path,scr_w/15,scr_h/15)
        if boo:
            def move():
                global i, condition
                canvas.delete(location_name)
                map_position[1] += 91*scr_h/18000            #y歩幅調整済み
                canvas.create_image(map_position[0],map_position[1],image=map_img,tag=location_name)
                canvas.create_image(tile_x,tile_y,image=player_img,tag='Player')
                # print(player_loc)
                # print(map[player_loc[1]][player_loc[0]])
                i += 1
                if i != 10:
                    root.after(10,move)
                else:
                    condition = True
            move()
        else:
            def move():
                global i, condition
                canvas.delete('Player')
                player_screen_loc[1] -= 135*scr_h/18000
                canvas.create_image(player_screen_loc[0],player_screen_loc[1],image=player_img,tag='Player')
                #canvas.create_image(tile_x,tile_y,image=player_img,tag='Player')
                # print(player_loc)                             #常に移動先の座標を表示
                # print(map[player_loc[1]][player_loc[0]])
                i += 1
                if i != 10:
                    root.after(10,move)
                else:
                    condition = True
            move()
    if key == 'Down' and map[player_loc[1]+1][player_loc[0]] != '1':
        condition = False
        path = './img/player/front.png'
        player_img = chore.resize(path,scr_w/15,scr_h/15)
        player_loc[1] += 1
        if boo:
            def move():
                global i, condition
                canvas.delete(location_name)
                map_position[1] -= 91*scr_h/18000
                canvas.create_image(map_position[0],map_position[1],image=map_img,tag=location_name)
                canvas.create_image(tile_x,tile_y,image=player_img,tag='Player')
                # print(player_loc)
                # print(map[player_loc[1]][player_loc[0]])
                i += 1
                if i != 10:
                    root.after(10,move)
                else:
                    condition = True
            move()
        else:
            def move():
                global i, condition
                canvas.delete('Player')
                player_screen_loc[1] += 135*scr_h/18000
                canvas.create_image(player_screen_loc[0],player_screen_loc[1],image=player_img,tag='Player')
                # print(player_loc)
                # print(map[player_loc[1]][player_loc[0]])
                i += 1
                if i != 10:
                    root.after(10,move)
                else:
                    condition = True
            move()
    if key == 'Right' and map[player_loc[1]][player_loc[0]+1] != '1':
        condition = False
        path = './img/player/right.png'
        player_img = chore.resize(path,scr_w/15,scr_h/15)
        player_loc[0] += 1
        if boo:
            def move():
                global i, condition
                canvas.delete(location_name)
                map_position[0] -= scr_w/360   #歩幅調整完了
                canvas.create_image(map_position[0],map_position[1],image=map_img,tag=location_name)
                canvas.create_image(tile_x,tile_y,image=player_img,tag='Player')
                # print(player_loc)
                # print(map[player_loc[1]][player_loc[0]])
                i += 1
                if i != 10:
                    root.after(10,move)
                else:
                    condition = True
            move()
        else:
            def move():
                global i, condition
                canvas.delete('Player')
                player_screen_loc[0] += 208*scr_w/50000
                canvas.create_image(player_screen_loc[0],player_screen_loc[1],image=player_img,tag='Player')
                # print(player_loc)
                # print(map[player_loc[1]][player_loc[0]])
                i += 1
                if i != 10:
                    root.after(10,move)
                else:                    
                    condition = True
            move()
    if key == 'Left' and map[player_loc[1]][player_loc[0]-1] != '1':
        condition = False
        path = './img/player/left.png'
        player_img = chore.resize(path,scr_w/15,scr_h/15)
        player_loc[0] -= 1
        if boo:
            def move():
                global i, condition
                canvas.delete(location_name)
                map_position[0] += scr_w/360   #歩幅調整完了
                canvas.create_image(map_position[0],map_position[1],image=map_img,tag=location_name)
                canvas.create_image(tile_x,tile_y,image=player_img,tag='Player')
                # print(player_loc)
                # print(map[player_loc[1]][player_loc[0]])
                i += 1
                if i != 10:
                    root.after(10,move)
                else:
                    condition = True
            move()
        else:
            def move():
                global i, condition
                canvas.delete('Player')
                player_screen_loc[0] -= 208*scr_w/50000
                canvas.create_image(player_screen_loc[0],player_screen_loc[1],image=player_img,tag='Player')
                # print(player_loc)
                # print(map[player_loc[1]][player_loc[0]])
                i += 1
                if i != 10:
                    root.after(10,move)
                else:
                    condition = True
            move()
         
def back_corrider_setup(location):
    global map, map_img, player_img, boo, player_loc, tile_x, tile_y, map_position, player_screen_loc
    data = copy.deepcopy(corrider_back_dict[location])
    canvas.delete('all')
    map = chore.roommaker('./data/corrider.txt')
    map_img = chore.resize('./img/map/corrider.png',2*scr_w,2*scr_h)
    player_screen_loc = copy.copy(data[0])
    canvas.create_image(data[0][0],data[0][1],image=map_img,tag=location)
    player_img = chore.resize('./img/player/front.png',scr_w/15,scr_h/15)    #縦廊下の1/3になるように調整
    tile_x = scr_w/2
    tile_y = scr_h/2
    canvas.create_image(tile_x,tile_y,image=player_img,tag='Player')
    map_position = copy.copy(data[0])
    player_loc = data[1]
    boo = True

def set_up(location):    #場面転換
    global map, map_img, player_img, boo, player_loc, tile_x, tile_y, map_position, player_screen_loc, condition, walk_count, music_count
    condition = True
    if walk_count == 0:
        chore.BGM('./music/SE/探索.mp3')
    canvas.delete('all')
    data = copy.deepcopy(data_dict[location])
    map = chore.roommaker(data[0])
    map_img = chore.resize(data[1],data[2][0],data[2][1])
    player_screen_loc = data[4]
    canvas.create_image(data[3][0],data[3][1],image=map_img,tag=location)
    player_img = chore.resize('./img/player/front.png',scr_w/15,scr_h/15)    #縦廊下の1/3になるように調整
    tile_x = player_screen_loc[0]
    tile_y = player_screen_loc[1]
    canvas.create_image(tile_x,tile_y,image=player_img,tag='Player')
    map_position = data[3]
    player_loc = data[5]
    
    if location == 'corrider':
        boo = True
    else:
        boo = False

chore.BGM('./music/BGM/natsunokiri.mp3')
root = tkinter.Tk()
root.geometry(f'{scr_w}x{scr_h}')
canvas = tkinter.Canvas(width=scr_w,height=scr_h,bg='black')
canvas.pack()
s_img_1 = chore.resize('./img/screen/スタート画面_めんだこ.png',scr_w,scr_h)
canvas.create_image(scr_w/2,scr_h/2,image=s_img_1,tag='BG_start')
b_img_1 = chore.resize('./img/buttun/start3.png',scr_w/5,scr_h/10)
new_game_b = tkinter.Button(image=b_img_1,command=new_game)
new_game_b.place(x=int(scr_w*0.4),y=int(scr_h*0.7))
whole_map_img = chore.resize('./img/map/whole_map.png',scr_w,scr_h)
textbox_img = chore.resize('./img/component/textbox.png',3*scr_w/4,scr_h/4)
clear_img = chore.resize('./img/screen/クリア画面.png',scr_w,scr_h)
death_img = chore.resize('./img/screen/death_4.png',scr_w,scr_h)        #death,death_2,death_3,death_4選択可能
root.mainloop()