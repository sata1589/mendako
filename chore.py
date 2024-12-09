from PIL import Image, ImageTk
from pygame import mixer

def resize(path,w=1,h=1) -> ImageTk.PhotoImage: #画像の成形
    img = Image.open(path)
    img = img.resize((int(w),int(h)))
    tkimg = ImageTk.PhotoImage(img)
    return tkimg
    
def BGM(path):    #BGMの再生
    try:
        mixer.quit()
    except:
        pass
    mixer.init()
    BGM = mixer.Sound(path)
    channel = mixer.Channel(0)
    channel.play(BGM,loops=-1)

def music_quit():
    mixer.quit()

def roommaker(path):    #mapの作成
    map = []
    with open(path,'r') as f:
        for ele in f:
            map.append(ele.strip().split(','))
    return map

def SE(path):   #効果音の再生
    try:
        SE = mixer.Sound(path)
    except:
        mixer.init()
        SE = mixer.Sound(path)
    channel = mixer.Channel(1)
    channel.play(SE)
