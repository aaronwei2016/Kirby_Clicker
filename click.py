import pygame
import random
import json
from datetime import datetime
pygame.init()
pygame.init()
start_time = pygame.time.get_ticks()
pygame.mixer.init()
width = 1000
height = 700
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Kirby Clicker")
center_x = width / 2
center_y = height / 2
background_img = pygame.image.load("images/background.png").convert()

running = True
start_time = pygame.time.get_ticks()
shock_time = pygame.time.get_ticks()

already_pro = False
money = 0
ally_damage = 0
click_power = 1
season = "Star Flun Heros"
season_color = "background.png"
image = "kirby2.png"  
kirby = pygame.image.load(f"images/{image}")
kirby_rect = kirby.get_rect(center=(center_x, center_y))
background_img = pygame.image.load(f"images/{season_color}")
background = pygame.transform.scale(background_img, (width, height))
ally_x = 0
ally_y = center_y

MAX_CLICK_POWER = 9999999999999
wsound = "ww.mp3"
typing = True
name = "Guest"
adding = ""
selected = image
shop = False
shopping = False
pressed = False
falcon = pygame.mixer.Sound("Sounds/falcon.mp3")
ally_image = None

song = pygame.mixer.Sound("Sounds/song.mp3")
allys = []
avatar = {
    "eyes": "0_0",
    "color": (0, 0, 0)
}


ability = None
power = None
text = pygame.font.SysFont("Arial", 39)
need = pygame.font.SysFont("Arial", 29)
font = pygame.font.SysFont("Arial", 28)
clock = pygame.time.Clock()
filename = "clicker.json"

cover = pygame.image.load("images/cover.png")


choices = [
    {
        "name": "1.Normal Kirby",
        "cost": 0,
        "image": pygame.image.load("images/kirby2.png"),
        "pos": (400, 30),
        "real": "kirby2.png",
        "rect": pygame.Rect(400, 30, 49, 49),
        "bought": True,
        "color": (0, 255, 0),
        "name_pos": (370, 120),
        "cost_pos": (470, 150),
        "extra": 1
    },
    {
        "name": "2.Sword Kirby",
        "cost": 200,
        "image": pygame.image.load("images/swordkirby.png"),
        "pos": (400, 200),
        "real": "swordkirby.png",
        "rect": pygame.Rect(400, 200, 49, 49),
        "bought": False,
        "color": (255, 216, 0),
        "name_pos": (370, 290),
        "cost_pos": (470, 320),
        "extra": 3
    },
    {
        "name": "3.Fire Kirby",
        "cost": 500,
        "image": pygame.image.load("images/kirby3.png"),
        "pos": (400, 340),
        "real": "kirby3.png",
        "rect": pygame.Rect(400, 340, 49, 9999),
        "bought": False,
        "color": (255, 216, 0),
        "name_pos": (370, 490),
        "cost_pos": (470, 520),
        "extra": 5
    },
    {
        "name": "4.Crystal Ice Kirby",
        "cost": 1000,
        "image": pygame.image.load("images/kirby.png"),
        "pos": (400, 540),
        "real": "kirby.png",
        "rect": pygame.Rect(400, 540, 49, 49),
        "bought": False,
        "color": (255, 216, 0),
        "name_pos": (370, 640),
        "cost_pos": (470, 620),
        "extra": 9
    }
]




ally = None
any_ally_owned = False
kirbys = []
def save_game():
    data = {
        "money": money,
        "season": season,
        "click_power": click_power,
        "season_color": season_color,
        "name": name,
        "eyes": avatar["eyes"],
        "color": avatar["color"],
        "selected": selected,
        "any_ally_owned": any_ally_owned,
        "ally_image": ally_image,
        "pro_level": pro_level,
        "ability": ability,
        "start_time": start_time,
        "current_reward": current_reward,
        "kirbys": kirbys,
        "allys": [
            {
                "name": ally["name"],
                "sound": ally["sound"],
                "image": ally["image"],
                "damage": ally["damage"],
                "bought": ally.get("bought", False),
                "rect": {
                    "x": ally["rect"].x,
                    "y": ally["rect"].y,
                    "w": ally["rect"].width,
                    "h": ally["rect"].height
                }
            }
            for ally in allys
        ],
        "skins": [
            {
                "name": choice["name"],
                "real": choice["real"],
                "bought": choice.get("bought", False)
            }
            for choice in choices
        ]
    }

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def load_game():
    global money, season, click_power, season_color, name, typing, selected, kirby, kirby_rect, background
    global pro_level, any_ally_owned, ability, ally_image
    
    try:
        with open(filename, "r") as f:
            data = json.load(f)

        money = data.get("money", 0)
        season = data.get("season", None)
        click_power = data.get("click_power", 1)
        season_color = data.get("season_color", "background.png")
        name = data.get("name", "Guest")
        pro_level = data.get("pro_level", 1)
        any_ally_owned = data.get("any_ally_owned", False)
        ally_image = data.get("ally_image", "nothing.png")
        ability = data.get("ability", None)
        start_time = data.get("start_time", pygame.time.get_ticks())
        current_reward = data.get("current_reward", 50)
        if name:
            typing = False
        if click_power <= 0:
            click_power = 1
        avatar["eyes"] = data.get("eyes", avatar["eyes"])
        avatar["color"] = data.get("color", avatar["color"])
        selected = data.get("selected", "kirby2.png")
        saved_skins = data.get("skins", [])
        for saved_skin in saved_skins:
            if "name" not in saved_skin:
                continue
            for choice in choices:
                if choice["name"] == saved_skin["name"]:
                    choice["bought"] = saved_skin.get("bought", False)

        saved_allies = data.get("allys", [])
        for saved_ally in saved_allies:
            for ally in allys:
                if ally["name"] == saved_ally["name"]:
                    ally["bought"] = saved_ally.get("bought", False)
                    ally["sound"] = saved_ally.get("sound", ally["sound"])
                    ally["damage"] = saved_ally.get("damage", ally["damage"])
                    ally["rect"] = {"x": ally["rect"].x, "y": ally["rect"].y, "w": ally["rect"].width, "h": ally["rect"].height}
        kirby = pygame.image.load(f"images/{selected}")
        kirby_rect = kirby.get_rect(center=(center_x, center_y))
        background = pygame.image.load(f"images/{season_color}")
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Load error: {e}")



def select_kirby(the_kirby):
    global selected, kirby
    pass




upgrade_cost = click_power * 3 + 5
def draw_screen():
    global posi, season_page
    if not season_page:
        screen.blit(background, posi)
    score = text.render(f"Money: {money}", True, (255, 255, 255))
    power = text.render(f"Click Power : {click_power}", True, (255, 255, 255))
    screen.blit(score, (50, 50))
    screen.blit(power, (450, 50))
    if season_color != "com.png":
        screen.blit(kirby, kirby_rect)
    


def draw_shop():
    global shopping, pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_s] and not pressed:
        pressed = True
        shopping = not shopping
    if shopping:
        pygame.draw.rect(screen, (100, 100, 100), (center_x - 250, center_y - 120, 490, 390))
        title = font.render("Upgrade Shop", True, (255, 255, 255))
        upgrade_text = font.render(f">>> Upgrade Click Power ${upgrade_cost}", True, (255, 255, 255))
        screen.blit(title, (400, 260))
        screen.blit(upgrade_text, (center_x - 200, center_y + 40))
        upgrade2_text = font.render(f">>> Star Click ${upgrade_cost * 2}", True, (255, 255, 255))
        screen.blit(upgrade2_text, (center_x - 200, center_y + 70))
        screen.blit(title, (400, 260))
        screen.blit(upgrade_text, (center_x - 200, center_y + 40))
        exit_rect2 = pygame.Rect(width - 310, 240, 40, 40)
        x = need.render("X", True, (255, 110, 10))
        pygame.draw.rect(screen, (255, 0, 0), exit_rect2, border_radius=5)
        screen.blit(x, (width - 300, 245))





def draw_kirby():
    if shop:
        for choice in choices:
            choice["rect"] = pygame.Rect(choice["pos"], (49, 49))
            screen.blit(choice["image"], choice["pos"])
            label = need.render(choice["name"], True, (0, 0, 0))
            screen.blit(label, choice["name_pos"])

            cost = need.render(f"Cost: ${choice['cost']}", True, (0, 255, 0))
            screen.blit(cost, (choice["rect"].x + 80, choice["rect"].y + 10))

            status = need.render(f"Bought: {choice['bought']}", True, choice["color"])
            screen.blit(status, (choice["rect"].x + 80, choice["rect"].y + 40))

        exit_rect = pygame.draw.rect(screen, (200, 0, 0), (width - 200, 50, 150, 50))
        exit_text = font.render("Exit", True, (255, 255, 255))
        screen.blit(exit_text, (width - 180, 60))



def add_name():
    global name, adding, typing
    label = text.render("Enter your name:", True, (255, 255, 255))
    user_input = font.render(adding, True, (255, 255, 255))
    screen.blit(label, (center_x - 150, center_y - 60))
    screen.blit(user_input, (center_x - 150, center_y))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                adding = adding[:-1]
            elif event.key == pygame.K_RETURN:
                typing = False
                name = adding
            else:
                if len(adding) < 17:
                    adding += event.unicode
pause = False
pause_image = pygame.image.load("images/back.png")
window_visible = False

current_song = None
def play(word):
    global current_song
    current_song = word
    sound = pygame.mixer.music.load(word)##load the mucic for Aaron(STILL ITS A SOUND(5.0 seconds atleast))
    pygame.mixer.music.play(loops=-1, start=0.0)##Yay! STARTT THE MUSIC AND IT STARTS at the 0.0 second of the music





def play_sound():
    key = pygame.key.get_pressed()
    if key[pygame.K_1]:
        pygame.mixer.music.stop()
        play("Sounds/song.mp3")
    elif key[pygame.K_2]:
        pygame.mixer.music.stop()
        play("Sounds/song2.mp3")
    elif key[pygame.K_3]:
        pygame.mixer.music.stop()
        play("Sounds/song3.mp3")
    elif key[pygame.K_4]:
        pygame.mixer.music.stop()
        play("Sounds/song4.mp3")

ability = None
def buy_power(power):
    global ability
    ability = power

def get_power():
    global ability, money
    screen.blit(background)
poyo = pygame.mixer.Sound("Sounds/poyo.mp3")

posi = (0, 0)
last_background = None
copykirby = pygame.mixer.Sound("Sounds/copykirby.mp3")
star = pygame.mixer.Sound("Sounds/star.mp3")
abilitys = [
    {
        "extra": 5,
        "name": "Star Sucker",
        "sound": None,
        "cost": 100,
        "bought": False,
        "pos1": (center_x - 80, 150),
        "pos2": (center_x - 80, 200),
        "rect": pygame.Rect(center_x - 80, 150, 230, 70)
    },
    {
        "extra": 10,
        "name": "Hi-Co-Punch!",
        "sound": "Sounds/falcon.mp3",
        "cost": 290,
        "bought": False,
        "pos1": (center_x - 80, 320),
        "pos2": (center_x - 80, 370),
        "rect": pygame.Rect(center_x - 80, 320, 230, 70)
    },
    {
        "extra": 15,
        "name": "Warp Click",
        "sound": "Sounds/star.mp3",
        "bought": False,
        "cost": 410,
        "pos1": (center_x - 80, 470),
        "pos2": (center_x - 80, 520),
        "rect": pygame.Rect(center_x - 80, 470, 230, 70)
    }
]

current_hour = 1
current_reward = 50

def give_daily_bonus():
    global money, click_power, current_day, next_day, current_reward
    money += current_reward
    
need2 = pygame.font.Font(None, 25)
bosses = [
    {
        "name": "Mecha Dedede",
        "health": 560,
        "real": "mecha.png",
        "extra": 150,
        "max_health": 560,
        "sheild": False
    },    
    {
        "name": "Captain Gordo",
        "health": 760,
        "real": "bomb.png",
        "extra": 200,
        "max_health": 760,
        "sheild": False
    },
    {
        "name": "Zero-Two",
        "health": 1060,
        "real": "boss4.png",
        "extra": 250,
        "max_health": 1060,
        "sheild": False
    },
    {
        "name": "Aeon Hero Light",
        "health": 1260,
        "real": "mega.png",
        "extra": 550,
        "max_health": 1260,
        "sheild": False
    },
    {
        "name": "Aeon Hero Dark",
        "health": 1560,
        "real": "ultra.png",
        "extra": 550,
        "max_health": 1560,
        "sheild": False
    },
    {
        "name": "Morpho Soul",
        "health": 2960,
        "real": "mouse.png",
        "extra": 550,
        "max_health": 2960,
        "sheild": False
    },
    {
        "name": "Morpho Knight",
        "health": 5260,
        "real": "morph.png",
        "extra": 650,
        "max_health": 5260,
        "sheild": False
    },
    {
        "name": "Dark Matter",
        "health": 10260,
        "real": "evil.png",
        "extra": 1050,
        "max_health": 10260,
        "sheild": False
    }
]


foods = [
    {
        "name": "Kirby Hamburger",
        "cost": 50
    }
]

season_kirby = "jumpkirby.png"
season_kirby_two = "starkirby.png"
magolor = pygame.image.load(f"allies/{season_kirby}")
season_page = False
magolor_two = pygame.image.load(f"allies/{season_kirby_two}")
kirby_one = "Super Kirby"
kirby_two = "Star Kirby"

messages = []


second_file = "owner_messages.json"
def send(message):
    try:
        with open(second_file, "r") as file:
            messages = json.load(file)##every thing in the file!
            if not isinstance(messages, list):## is not messages is a list?(Then its a new file)
                messages = []
    except (FileNotFoundError, json.JSONDecodeError) as error:
        messages = []
        print(f"The Error : {error}")
        

    messages.append(f"{name}: {message}")

    with open(second_file, "w") as file:##writing
        json.dump(messages, file, indent=4)



sending_stuff = ""
line_x = 353
def owner_page():
    global sending_stuff, running, line_x
    screen.fill((0, 0, 0))
    user_text = font.render(sending_stuff, True, (255, 255, 255))
    label = font.render("Enter Your Message:", True, (255, 255, 255))
    screen.blit(label, (390, 200))
    screen.blit(user_text, (350, 300))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                sending_stuff = sending_stuff[:-1]
                line_x -= 14
            elif event.key == pygame.K_RETURN:
                if sending_stuff.strip(): 
                    send(sending_stuff.strip())
                    sending_stuff = ""
                    line_x = 353
            else:
                if event.unicode.isprintable():
                    sending_stuff += event.unicode
                    line_x += 14


        
    




pro_level = 0
story = []
pro_pass = [
    {
        "reward": "money",
        "level": 1,
        "bonus": 20,
        "got": False,
        "dic": "Money+20",
        "x_pos": 250,
        "y_pos": center_y - 70,
        "rect": pygame.Rect(150, center_y - 20, 224, 30),
        "image": "coins.png",
        "image_pos": (265, center_y - 142)  
    },
    {
        "reward": "money",
        "level": 2,
        "bonus": 35,
        "got": False,
        "dic": "Money+35",
        "x_pos": 450,
        "y_pos": center_y - 70,
        "rect": pygame.Rect(350, center_y - 20, 224, 30),
        "image": "coins.png",
        "image_pos": (465, center_y - 142)
    },
    {
        "reward": "click_power",
        "level": 3,
        "bonus": 4,
        "got": False,
        "dic": "Click Power+4",
        "x_pos": 650,
        "y_pos": center_y - 70,
        "rect": pygame.Rect(530, center_y - 20, 364, 30),
        "image": "xp.png",
        "image_pos": (685, center_y - 152)
    },
    {
        "reward": "skin",
        "level": 5,
        "bonus": "badana.png",
        "got": False,
        "x_pos": 850,
        "y_pos": center_y - 70,
        "rect": pygame.Rect(750, center_y - 20, 420, 30),
        "dic": "Waddle dee Ally",
        "damage": 10,
        "image": "badana.png",
        "image_pos": (865, center_y - 152),
        "Sound": "ww.mp3",
        "name": "Badana Waddle Dee",
        "speed": 3
    },
    {
        "reward": "click_power",
        "level": 10,
        "bonus": 5,
        "got": False,
        "dic": "Click Power+5",
        "x_pos": 250,
        "y_pos": center_y + 100,
        "rect": pygame.Rect(730, center_y - 20, 364, 30),
        "image": "xp.png",
        "image_pos": (285, center_y + 100 - 82)
    },
    {
        "reward": "skin",
        "level": 15,
        "bonus": "meta.png",
        "got": False,
        "x_pos": 450,
        "y_pos": center_y + 100,
        "rect": pygame.Rect(750, center_y - 20, 420, 30),
        "dic": "Meta Knight Ally",
        "damage": 28,
        "image": "metaknight.png",
        "image_pos": (445, center_y + 100 - 115),
        "Sound": "metaknight.wav",
        "name": "Meta Knight",
        "speed": 5
    },
    {
        "reward": "money",
        "level": 20,
        "bonus": 40,
        "got": False,
        "dic": "Money+40",
        "x_pos": 650,
        "y_pos": center_y + 100,
        "rect": pygame.Rect(550, center_y - 20, 224, 30),
        "image": "coins.png",
        "image_pos": (665, center_y + 100 - 72),
        "x2_pos": (640, center_y + 2)
    },
    {
        "reward": "click_power",
        "level": 25,
        "bonus": 5,
        "got": False,
        "dic": "Click Power+5",
        "x_pos": 850,
        "y_pos": center_y + 100,
        "rect": pygame.Rect(750, center_y - 20, 364, 30),
        "image": "xp.png",
        "image_pos": (865, center_y + 100 - 82),
        "x2_pos": (840, center_y + 2)
    },
    {
        "reward": "story piece",
        "level": 29,
        "got": False,
        "bonus": [
            "Beyond The Stars, A Glimmer Of Spark Was Caught By",
            "The Eye Of Kirby, Kirby : Poyo! Its A Mace!,",
            "But It Was Not... It Was Better. It Sparkled Through The Glimpse",
            "Of The Stars, Blasted From The Fountain",
            "Of Dreams, And Flew Right In Front Of Kirby",
            "While Behind The Rotted Forest, A Mysterius Dark Figure Was Watching...",
            "With A Dark Red Eye And A Dark Mind Ahead"
        ],
        "x_pos": 150,
        "y_pos": center_y + 300,
        "rect": pygame.Rect(230, center_y - 20, 420, 30),
        "dic": "Special Skin",
        "damage": 28,
        "image": "Story Piece One",
        "image_pos": (160, center_y + 200 - 12),
        "name": "Story Piece One",
        "x2_pos": (140, center_y + 202)
    },
    {
        "reward": "story piece",
        "level": 33,
        "bonus": [
            "While Terrified From The Light, The Mysterius Dark",
            "Figure Jumped From The Shadows, With  A Glowing Black And",
            "Red Eye Staring At Kirby. Kirby Grabbed The Triple Star Mace",
            "And Charged At The Figure Dark Mind WIth A Shocking Blow",
            "Dark Mind Was Not Finished... It Was Never Finished.",
            "Kirby Relized A Spirit May Never Be Gone,",
            "So Kirby Locked Dark Mind In A Prison With",
            "A Blast Of Light In The Fountain Of Dreams.",
            "There, The Light Will Never Be Gone."
        ],
        "got": False,
        "x_pos": 450,
        "y_pos": center_y + 300,
        "rect": pygame.Rect(530, center_y - 20, 420, 30),
        "dic": "Special Skin",
        "damage": 28,
        "image": "Story Piece Two",
        "image_pos": (460, center_y + 200 - 12),
        "name": "Story Piece Two",
        "extra_bonus": 20,
        "x2_pos": (440, center_y + 202)
    },
    {
        "reward": "story piece",
        "level": 35,
        "bonus": [
            "As Dark Mind Peirced Through His",
            "Prison With A Revengefull Stare,",
            "Meta Knight Watched... It Was",
            "His Chance To Be A PowerFull Knight.",
            "But He Held Back... Why? Kirby Asked.",
            "Meta Knight Couldnt Belive It... It",
            "Was The Beggining Of Fate...",
            "The Rebirth Of The One Who",
            "Belived In Darkness... The Entity",
            "Who Never Came Back For Sentrys...",
            "Dark Matter......"
        ],
        "got": False,
        "x_pos": 450,
        "y_pos": center_y + 300,
        "rect": pygame.Rect(530, center_y - 20, 420, 30),
        "dic": "Special Skin",
        "damage": 28,
        "image": "Story Piece Two",
        "image_pos": (460, center_y + 200 - 12),
        "name": "Story Piece Two",
        "extra_bonus": 20,
        "x2_pos": (440, center_y + 202)
    },
    {
        "reward": "story piece",
        "level": 37,
        "bonus": [
           "As With No Hope, Dark Mind",
           "Crumbled Into Peices While Dark Matter Contained",
           "Kirby Grabbed His Mace And Hopefully Landed",
           "A Painfull Shockwave On Dark Matters Forehead",
           "Kirby Suddenly Woke Up In A Nightmare...",
           "Kirby : Poyo? What Is This?",
           "Why Is It All Black?. Dark Matter Contained",
           "And So On, Kirby knew It.... With A Burst",
           "Of Stars, Kirby Won. Darkness Loses",
           "By Heart",
           "Epilogue : While In The Volcano...",
           "A Soul Rebirthed"
        ],
        "got": False,
        "x_pos": 450,
        "y_pos": center_y + 300,
        "rect": pygame.Rect(530, center_y - 20, 420, 30),
        "dic": "Special Skin",
        "damage": 28,
        "image": "Story Piece Two",
        "image_pos": (460, center_y + 200 - 12),
        "name": "Story Piece Two",
        "extra_bonus": 20,
        "x2_pos": (440, center_y + 202)
    },
    {
        "reward": "kirby",
        "level": 40,
        "bonus": "triple.png",
        "got": False,
        "x_pos": 750,
        "y_pos": center_y + 300,
        "rect": pygame.Rect(830, center_y - 20, 420, 30),
        "dic": "Special Skin",
        "damage": 28,
        "image": "triple2.png",
        "image_pos": (760, center_y + 200 - 12),
        "name": "Star Mace Kirby",
        "extra_bonus": 20,
        "x2_pos": (740, center_y + 202)
    },
]

ally = None
ally_image = None
sending_message = False
def give_reward(suprise):
    global money, click_power, skin, pro_level, ally_image, wsound
    global any_ally_owned, ally_damage, kirby
    global selected, kirby_rect, already_pro
    if pro_level >= suprise["level"] and not suprise["got"]:
        if suprise["reward"] == "money":
            money += suprise["bonus"]
            suprise["got"] = True
        elif suprise["reward"] == "click_power":
            click_power += suprise["bonus"]
            suprise["got"] = True
        elif suprise["reward"] == "skin":
            new_ally = {
                "sound": suprise["Sound"],
                "image": suprise['bonus'],
                "damage": suprise["damage"],
                "rect": pygame.Rect(0, 0, 88, 100),
                "name": suprise["name"],
                "bought": True,
                "speed": suprise["speed"]
            }
            allys.append(new_ally)
            any_ally_owned = True
            suprise["got"] = True
        elif suprise["reward"] == "kirby":
            kirby = pygame.image.load(f"pro pass rewards/{suprise['bonus']}")
            kirby_rect = kirby.get_rect(center=(center_x, center_y))
            click_power += suprise["extra_bonus"]
            suprise["got"] = True
        elif suprise["reward"] == "story piece":
            story.append(suprise["bonus"])
            suprise["got"] = True
            already_pro = True
        suprise["got"] = True
    
    
pro = False



def instanly_change_season():
    global season_kirby, season_kirby_two, kirby_one, kirby_two, magolor, magolor_two, season, money, click_power
    now = datetime.now()
    if now.month == 7 or now.month == 8:
        season = "Star Flun Heros"
        season_kirby = "jumpkirby.png"
        season_kirby_two = "starkirby.png"
        magolor = pygame.image.load(f"allies/{season_kirby}")
        magolor_two = pygame.image.load(f"allies/{season_kirby_two}")
        kirby_one = "Super Kirby"
        kirby_two = "Star Kirby"
    elif now.month == 1 or now.month == 2:
        season = "Magolors Odessy"
        season_kirby = "magolor.png"
        season_kirby_two = "ultrasword.png"
        magolor = pygame.image.load(f"allies/{season_kirby}")
        magolor_two = pygame.image.load(f"allies/{season_kirby_two}")
        kirby_one = "Magolor"
        kirby_two = "Ultra Sword"
    elif now.month == 11 or now.month == 12:
        season = "Meta Mayhem"
        season_kirby = "metaknight.png"
        season_kirby_two = "metakirby.png"
        magolor = pygame.image.load(f"allies/{season_kirby}")
        magolor_two = pygame.image.load(f"allies/{season_kirby_two}")
        kirby_one = "Meta Knight"
        kirby_two = "Meta Kirby"
    elif now.month == 4 or now.month == 5:
        season = "Katana Kingdom"
        season_kirby = "samuraikirby.png"
        season_kirby_two = "samurai.png"
        magolor = pygame.image.load(f"allies/{season_kirby}")
        magolor_two = pygame.image.load(f"allies/{season_kirby_two}")
        kirby_one = "Katana Kirby"
        kirby_two = "Waddle Doo"
    else:
        season = None
        season_page = False
    save_game()




        



def event_draw():
    global season, season_page
    screen.fill((30, 0, 60))
    pygame.draw.rect(screen, (234, 4, 255), (200, center_y - 150, 200, 400), border_radius=9)
    pygame.draw.rect(screen, (152, 0, 255), (200, center_y - 150, 200, 400), 10, border_radius=9)
    screen.blit(magolor, (237, center_y - 30))
    superlabel = font.render(f"{kirby_one}", True, (255, 255, 255))
    screen.blit(superlabel, (220, center_y - 140))
    event_label = font.render(f"{season}", True, (255, 255, 255))
    screen.blit(event_label, (center_x - 200, 45))

    
    
    

    
    pygame.draw.rect(screen, (234, 4, 255), (490, center_y - 150, 200, 400), border_radius=9)
    pygame.draw.rect(screen, (152, 0, 255), (490, center_y - 150, 200, 400), 10, border_radius=9)
    screen.blit(magolor_two, (527, center_y - 30))

    superlabel = font.render(f"{kirby_two}", True, (255, 255, 255))
    screen.blit(superlabel, (520, center_y - 140))
    

    
    exit_button = pygame.draw.rect(screen, (200, 0, 0), (width - 200, 50, 150, 50))
    exit_text = font.render("Exit", True, (255, 255, 255))
    screen.blit(exit_text, (width - 180, 60))
    

    
    
    


def add_reward():
    if pro:
        for i in range(len(pro_pass)):
            give_reward(pro_pass[i])


bigger = pygame.font.Font(None, 30)             
def draw_rewards():
    screen.blit(background, (0, 0))
    for gift in pro_pass:
        if "story piece" != gift["reward"]:     
            image = pygame.image.load(f"pro pass rewards/{gift['image']}")
        if "special" not in gift:
            pygame.draw.rect(screen, (255, 255, 0), (gift["x_pos"] + 0, gift["y_pos"] - 92, 130, 100), 3)
            pygame.draw.rect(screen, (0, 255, 255), (gift["x_pos"] + 3, gift["y_pos"] - 89, 125, 94))
        if "story piece" != gift["reward"]:
            screen.blit(image, gift["image_pos"])
        else:
            text = small.render(gift["image"], True, (0, 0, 0))
            screen.blit(text, (gift["x_pos"] + 3, gift["y_pos"] - 50))
        pygame.draw.circle(screen, (152, 0, 255), (gift["x_pos"], gift["y_pos"] - 90), 15)
        pygame.draw.circle(screen, (234, 4, 255), (gift["x_pos"], gift["y_pos"] - 90), 15, 3)
        number = small.render(f"{gift['level']}", True, (255, 255, 255))
        if "x2_pos" not in gift:
            screen.blit(number, (gift["x_pos"] - 5, gift["y_pos"] - 97))
        else:
            screen.blit(number, gift["x2_pos"])
        if "special" in gift:
            pygame.draw.rect(screen, (255, 255, 0), (gift["x_pos"] - 200, gift["y_pos"] - 92, 330, 100), 3)
            pygame.draw.rect(screen, (0, 255, 255), (gift["x_pos"] - 200, gift["y_pos"] - 89, 325, 94))
            mage_special = pygame.image.load(f"pro pass rewards/{gift['special']}")
            imagex, imagey = mage_special.get_size()
            image_special = pygame.transform.scale(mage_special, (imagex / 4, imagey / 4))
            screen.blit(image_special, gift["image_pos"])
    ay = font.render(f"Level : {pro_level}", True, (0, 0, 0))
    screen.blit(ay, (100, 100))
    exit_rect = pygame.draw.rect(screen, (200, 0, 0), (width - 200, 50, 150, 50))
    exit_text = font.render("Exit", True, (255, 255, 255))
    screen.blit(exit_text, (width - 180, 60))
    
    


mode = None
start_now = False
small = pygame.font.Font(None, 25)

boxes = [
    {
        "rect": pygame.Rect(center_x / 2, center_y / 2 + 100, 200, 60)
    },
    {
        "rect": pygame.Rect(center_x + center_x / 2 - 50, center_y - center_y / 2 + 100, 200, 60)
    },
    {
        "rect": pygame.Rect(center_x / 2, center_y + center_y / 2 - 100, 200, 60)
    },
    {
        "rect": pygame.Rect(center_x + center_x / 2 - 50, center_y + center_y / 2 - 100, 200, 60)
    }
]


fight = 1
index = 0
last_kirby = kirby
current_boss = bosses[index]
current_boss_health = current_boss["health"]
battle = False
wee = pygame.image.load("images/waddle.png")
wx, wy = wee.get_size()
waddle = pygame.transform.scale(wee, (wx * 3, wy * 3))
def arena():
    global battle, kirby, kirby_rect, last_kirby, current_boss, current_boss_health
    global season_color, background, last_background, posi, fight, index, mode
    last_background = background
    season_color = "arena.png"
    background = pygame.image.load(f"images/{season_color}")
    posi = (-100, -50)
    index = 0
    fight = 1
    for ret in boxes:
        for boss in bosses:
            pygame.draw.rect(screen, (255, 255, 255), ret["rect"], border_radius=9)
            namee = need.render(boss["name"], True, (0, 0, 0))
            screen.blit(namee, (ret["rect"].x + 10, ret["rect"].y + 20))

    battle = True
    if battle and season_color != "com.png":
        last_kirby = kirby
        current_boss = bosses[index]
        current_boss_health = current_boss["health"]
        kirby = pygame.image.load(f"images/{current_boss['real']}")
        kirby_rect = kirby.get_rect(center=(center_x, center_y))

def power_up():
    global ability, power
    for power1 in abilitys:
        mouse = pygame.mouse.get_pos()
        powerr = font.render(f"{power1['name']} ${power1['cost']}", True, (0, 0, 0))
        powerrr = font.render(f"Ability : {power1['extra']}+Money", True, (220, 220, 0))
        screen.blit(powerr, power1["pos1"])
        screen.blit(powerrr, power1["pos2"])
    screen.blit(waddle, (200, center_y - 10))
    exit_button = pygame.draw.rect(screen, (200, 0, 0), (width - 200, 50, 150, 50))
    exit_text = font.render("Exit", True, (255, 255, 255))
    screen.blit(exit_text, (width - 180, 60))
        


title = pygame.image.load("titles/title.png")

updates = [
    {"on": True, "word": "New Seasons!", "posx": center_x - 50, "posy": 110, "description": "Seasons : Katana Kingdom, Meta Mayhem, Star Flun Heros,", "date": "2025-07-20", "version": "v1.8.0"},
    {"on": True, "word": "Story Palace", "posx": center_x - 50, "posy": 220, "description": "Dicover The Orgin Of The Triple Star Mace!", "date": "2025-07-20", "version": "v1.8.0"},
    {"on": True, "word": "Pro Pass", "posx": center_x - 50, "posy": 310, "description": "Level up and get allies and boosts!", "date": "2025-07-18", "version": "v1.8.0"},
    {"on": True, "word": "Update Log Logic", "posx": center_x - 50, "posy": 410, "description": "Fixed Scrolling logic! Scroll Peacefully.", "date": "2025-07-16", "version": "v1.8.0"},
    {"on": True, "word": "Dark Matter Boss", "posx": center_x - 50, "posy": 510, "description": "The Entity Of Evil Is Here...", "date": "2025-07-15", "version": "v1.8.0"},
    {"on": True, "word": "New Background!", "posx": center_x - 50, "posy": 610, "description": "🎨background added!", "date": "2025-07-14", "version": "v1.8.0"},
    {"on": True, "word": "Morpho Knight Boss", "posx": center_x - 50, "posy": 710, "description": "🗡️ The Judgment is here!", "date": "2025-07-13", "version": "v1.7.0"},
    {"on": True, "word": "Boss Backgrounds", "posx": center_x - 50, "posy": 810, "description": "New battle backgrounds: Dedede’s Area and more!", "date": "2025-07-9", "version": "v1.6.0"},
    {"on": True, "word": "Fire Kirby Skin", "posx": center_x - 50, "posy": 910, "description": "🔥 New Fire Kirby skin added!", "date": "2025-07-8", "version": "v1.5.1"},
    {"on": True, "word": "Skins Boosts", "posx": center_x - 50, "posy": 1010, "description": "Boom! Skins now give you extra boosts!", "date": "2025-07-7", "version": "v1.5.0"},
    {"on": True, "word": "Arena", "posx": center_x - 50, "posy": 1110, "description": "Battle Kirby’s strongest enemies!", "date": "2025-07-04", "version": "v1.4.0"},
    {"on": True, "word": "Ability Shop", "posx": center_x - 50, "posy": 1210, "description": "Abilities are here with Sound Effects!", "date": "2025-07-1", "version": "v1.3.0"},
    {"on": True, "word": "Player Names", "posx": center_x - 50, "posy": 1310, "description": "You can now customize your name!", "date": "2025-06-28", "version": "v1.2.0"},
    {"on": True, "word": "Kirby Skins", "posx": center_x - 50, "posy": 1410, "description": "You can now buy Kirbys from the shop!", "date": "2025-06-25", "version": "v1.1.0"},
    {"on": True, "word": "Update Log Started", "posx": center_x - 50, "posy": 1510, "description": "What's updated? Keep track here!", "date": "2025-06-03", "version": "v1.0.0"},
]

updating = False
rd = font.render("|UPDATE LOG|", True, (255, 255, 255))

def show_updates():
    screen.fill("black")
    title_text = font.render("Update Log", True, (255, 255, 255))
    screen.blit(title_text, (center_x + 200, 50))
    for update in updates:
        if update["on"]:
            y = update["posy"]
            word_surface = font.render(update["word"], True, (255, 255, 0))
            screen.blit(word_surface, (update["posx"] - 200, y))

            description_surface = font.render(update["description"], True, (255, 255, 255))
            screen.blit(description_surface, (update["posx"] - 200, y + 30))

            date_surface = font.render(f"Date: {update['date']}", True, (255, 255, 255))
            screen.blit(date_surface, (update["posx"] - 200, y + 55))

    exit_rect = pygame.Rect(50, 50, 30, 30)
    pygame.draw.rect(screen, (255, 0, 0), exit_rect, border_radius=8)
    exit_text2 = small.render("X", True, (255, 255, 255))
    screen.blit(exit_text2, (60, 60))
    pygame.display.update()
        


icon1 = pygame.image.load("images/shop.png")
icon = pygame.transform.scale(icon1, (200, 60))


pro_level = 1
kirbyy = False
victory = pygame.mixer.Sound("Sounds/kirbys.mp3")
boom = pygame.mixer.Sound("Sounds/boom.mp3")
season_color = "background.png"
background = pygame.image.load(f"images/{season_color}")
hit =  False
shock = False
shock_now = pygame.time.get_ticks()
supe = "super.png"
pressed = False
left = False

def beyond():
    global pressed, shop, shopping, kirbyy, kirby, kirby_rect, money, click_power, upgrade_cost
    global pause, elapsed_time, start_time, exit_rect, exit2_rect, hit, shock
    global background, season_color, upgrading, battle, background_img, index, kirby, kirby_rect, pro_level
    draw_shop()
    if not sending_message and not kirbyy and not shop and not shopping and not battle and not season_page and not updating:
        change_button = pygame.draw.rect(screen, (255, 25, 0), (width - 400, 90, 370, 70))
        name_display = font.render(name, True, (0, 0, 0))
        screen.blit(name_display, (width - 320, 105))
        eye = font.render(avatar["eyes"], True, avatar["color"])
        screen.blit(eye, (width - 381, 105))

    if not shop and not shopping and not kirbyy and not battle and not season_page and not sending_message:
        screen.blit(icon, (100, height / 2 + 90))


    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        shop = False
        shopping = False
        pause = False
    if keys[pygame.K_h] and not pressed:
        pressed = True
        kirbyy = False
        pause = False
        shop = False
        shopping = False
        pro_level = 1


    if elapsed_time >= 200:
        if hit:
            new_x = random.randint(50, width - 50)
            new_y = random.randint(50, height - 50)
            kirby_rect.center = (new_x, new_y)
            start_time = pygame.time.get_ticks()
            hit = False
            
                
    if kirbyy:
        power_up()
        typing = False
    elif not sending_message and not kirbyy and not shop and not shopping and not battle and not season_page:
        power_button = pygame.draw.rect(screen, (128, 0, 128), (100, height / 2 + 160, 200, 50), border_radius=12)  # Purple button
        power_label = font.render("Ability Shop", True, (255, 255, 255))
        screen.blit(power_label, (135, height / 2 + 170))
    if shop:
        exit_rect = pygame.Rect(width - 200, 50, 150, 50)
     

    if battle:
        for boss in bosses:
            if not shop and not shopping and not kirbyy:
                if season_color != "com.png":
                    current_boss = bosses[index]
                    current_boss = bosses[index]
                    current_boss = bosses[index]
                    current_boss = bosses[index]
                    if fight == 8:
                        posi = (100, 100)
                        season_color = "omega.png"
                        background_img = pygame.image.load("images/omega.png")
                        background = pygame.transform.scale(background_img, (width + 100, height + 100))
                      
                    elif fight >= 6:
                        posi = (0, 0)
                        season_color = "super.png"
                        background_img = pygame.image.load(f"images/{season_color}")
                        background = pygame.transform.scale(background_img, (width, height))

                    elif fight >= 4:
                        posi = (0, 0)
                        season_color = "sun.png"
                        background_img = pygame.image.load(f"images/{season_color}")
                        background = pygame.transform.scale(background_img, (width + 100, height + 100))
 
                    elif fight == 1 or fight == 2:
                        posi = (0, 0)
                        season_color = "dun.png"
                        background_img = pygame.image.load(f"images/{season_color}")
                        background = pygame.transform.scale(background_img, (width, height))
                    else:
                        posi = (0, 0)
                        season_color = "arena.png"
                        background_img = pygame.image.load(f"images/{season_color}")
                        background = pygame.transform.scale(background_img, (width + 100, height + 100))
            
                if season_color != "com.png":
                    pygame.draw.rect(screen, (255, 255, 255), (100, height - 30, current_boss["max_health"] / 4, 20))
                    pygame.draw.rect(screen, (255, 0, 0), (100, height - 30, current_boss_health / 4, 20))
                    round1 = need.render(f"Round {fight}", True, (255, 255, 255))
                    screen.blit(round1, (int(center_x - 50), 200))
                    round2 = need.render(f"{name} Vs {current_boss['name']}", True, (255, 255, 0))
                    screen.blit(round2, (int(center_x - 200), 250))
                exit_rect = pygame.draw.rect(screen, (200, 0, 0), (width - 200, 50, 150, 50))
                exit_text = font.render("Exit Arena", True, (255, 255, 255))
                screen.blit(exit_text, (width - 180, 60))
                
  


                    

        if not shop and not shopping and not kirbyy and not battle and not season_page:
            start = font.render(f"The Arena", True, (255, 255, 255))
            battle_rect = pygame.Rect(100, int(height / 2), 200, 60)
            battle_box = pygame.draw.rect(screen, (255, 0, 0), battle_rect, border_radius=12)
            screen.blit(start, (130, height / 2 + 10))
        if battle and season_color == "arena.png":
            posi = (-50, -50)
        elif not battle and season_color == "arena.png":
            season_color = "background.png"
            background = pygame.image.load(f"images/{season_color}")
            kirby = last_kirby
            posi = (0, 0)
            
        if shop or shopping or kirbyy:
            typing = False

        if battle and fight == 7:
            if kirby == pygame.image.load("images/morph.png"):
                index += 1


            


        if kirby_rect.x > width - 20 or kirby_rect.y < 20 or kirby_rect.x < 20 or kirby_rect.y > height - 20:
            kirby_rect.center = (random.randint(30, width - 30), random.randint(30, height - 30))





max_y = 400
max_ys = height + 400
yes = True
icon2 = pygame.image.load("images/icon1.png")
level = 90

ally_turned = False




def ally_shop():
    global ally_sound
    screen.blit(background, (0, 0))



def chapter():
    global pro_level, updating, pause, start_now, sending_message
    if not updating and not pause and start_now and not pro and not sending_message:
        pygame.draw.rect(screen, (150, 150, 150), (center_x + center_x / 2, center_y, 190, 50))
        fonty = font.render("Story Palace", True, (255, 255, 255))
        screen.blit(fonty, (center_x + 260, center_y + 15))

book = 1

def show_story():
    global chapter
    screen.blit(background, (0, 0))
    line_height = need.get_height() + 20
    y = 50
    if book >= 1 and pro_level >= 29 and already_pro:
        for thing in story[book - 1]:
            if len(thing) > 0 and len(thing[0]) == 1:
                text_surface = need.render(thing, True, (0, 0, 0))
                screen.blit(text_surface, (20, y))
                y += line_height
            else:
                i = 0
                while i < len(thing):
                    text_surface = need.render(thing[i], True, (0, 0, 0))
                    screen.blit(text_surface, (20, y))
                    y += line_height
                    i += 1

    exit_rect = pygame.draw.rect(screen, (200, 0, 0), (width - 200, 50, 150, 50))
    exit_text = font.render("Exit", True, (255, 255, 255))
    screen.blit(exit_text, (width - 180, 60))

load_game()
save_game()
reading = False
MAX_COINS = 9999999999999
MAX_CLICK_POWER = 99999999999999
while running:
    instanly_change_season()
    if sending_message:
        owner_page()
    if kirbyy or shop or shopping or battle or pro or reading or updating or season_page:
        typing = False
    if season_page:
        battle = False
        typing = False
        shop = False
        kirbyy = False
        updating = False
    if updating:
        kirbyy = False
        
    if money is None:
        money = 0
    if season_color == "background.png":
        posi = (0, 0)
        background_img = pygame.image.load(f"images/{season_color}")
        background = pygame.transform.scale(background_img, (width, height + 30))
    now = pygame.time.get_ticks()
    elapsed_time = now - start_time
    if typing and not updating:
        add_name()
        pygame.display.update()
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game()
            print(f"{name} Left The Game!")
            battle = False
            
            running = False
        elif event.type == pygame.WINDOWMINIMIZED:
            pause = True
            window_visible = True
        elif event.type == pygame.WINDOWFOCUSLOST:
            if start_now:
                pause = True
                window_visible = True
        elif event.type == pygame.WINDOWFOCUSGAINED or event.type == pygame.WINDOWRESTORED:
            pause = False
            pause = False
            window_visible = True
        elif event.type == pygame.VIDEORESIZE:
            width, height = event.size
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            background = pygame.transform.scale(background_img, (width, height))
            pause_image = pygame.transform.scale(pause_image, (width, height))
            window_visible = True
        elif event.type == pygame.MOUSEWHEEL:
            if updating:
                ak = updates[0]
                ay = updates[-1]

                if event.y > 0:
                    if ak["posy"] < 50:
                        for update in updates:
                            update["posy"] += 20

                elif event.y < 0:
                    if ay["posy"] > height - 100:
                        for update in updates:
                            update["posy"] -= 20
            elif reading:
                if event.y > 0:
                    if y < 20:
                        y += 20

                elif event.y < 0:
                    if y > height - 70:
                        y -= 20
                print("SS")
                       
                    

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            some_rect = pygame.Rect(width - 200, 50, 150, 50)
        
            exit_rect = pygame.Rect(width - 200, 50, 150, 50)
            exit_rect2 = pygame.Rect(width - 310, 240, 40, 40)
            exit_rect3 = pygame.Rect(50, 50, 30, 30)
            update_rect = pygame.Rect(width - 190, height - 50, 190, 60)
            power_button = pygame.Rect(100, height / 2 + 160, 200, 50)
            update_rect = pygame.Rect(width - 190, height - 50, 190, 60)
            battle_rect = pygame.Rect(100, int(height / 2), 200, 60)
            button = pygame.Rect(width - 190, height - 120, 175, 60)
            chapters = pygame.Rect(center_x + center_x / 2 + 109, center_y, 190, 50)
            chapter1rect = pygame.Rect(center_x - 450, height - 70, 180, 50)
            chapter2rect = pygame.Rect(center_x - 200, height - 70, 180, 50)
            chapter3rect = pygame.Rect(center_x, height - 70, 180, 50)
            chapter4rect = pygame.Rect(center_x + 250, height - 70, 180, 50)

            if pygame.Rect(100, height / 2 - 70, 200, 60).collidepoint(pos) and not battle and not shop and not pro and not kirbyy:
                season_page = True
                pro = False
                battle = False
                shop = False
                shopping  = False

            
            
            
            
            if pygame.Rect(200, center_y - 150, 200, 400).collidepoint(pos) and season_page:
                if money >= 1200:
                    selected = season_kirby
                    kirby = pygame.image.load(f"allies/{selected}")
                    
                    kirby_rect = kirby.get_rect()

            if pygame.Rect(490, center_y - 150, 200, 400).collidepoint(pos) and season_page:
                if money >= 1600:
                    selected = season_kirby_two
                    kirby = pygame.image.load(f"allies/{selected}")
                    kirby_rect = kirby.get_rect()


                    


            if chapter1rect.collidepoint(pos) and already_pro:
                book = 1
            elif chapter2rect.collidepoint(pos) and already_pro:
                book = 2
            elif chapter3rect.collidepoint(pos) and already_pro:
                book = 3
            elif chapter4rect.collidepoint(pos) and already_pro:
                book = 4

            if some_rect.collidepoint(pos):
                if reading:
                    reading = False
            
            if chapters.collidepoint(pos):
                reading = True
                
            
            if button.collidepoint(pos):
                pro = True
            
            if exit_rect3.collidepoint(pos):
                if updating:
                    updating = False
            if update_rect.collidepoint(pos) and not battle and not kirbyy and not shop and not shopping:
                updating = not updating
            
            if exit_rect2.collidepoint(pos) and shopping and not battle:
                shopping = False
            if exit_rect.collidepoint(pos) and not battle and not pro:
                kirbyy = False
                shop = False
                shopping = False
                battle = False
                season_color = "background.png"
                background = pygame.image.load(f"images/background.png")
                season_page = False
                typing = False
            if exit_rect.collidepoint(pos) and not battle and pro:
                pro = False
            if exit_rect.collidepoint(pos) and battle and not shop and not kirbyy:
                kirbyy = False
                shop = False
                shopping = False
                battle = False
                season_color = "background.png"
                background = pygame.image.load(f"images/background.png")
                posi = (0, 0)
                kirby = last_kirby
            if kirby_rect.collidepoint(pos) and not kirbyy and not shop and not updating and not pro:
                hit = True
                shock = True
                shock_now = pygame.time.get_ticks()
                if ability != None:
                    sound = pygame.mixer.Sound(f"{ability}")
                if not battle:
                    if ability != None:
                        sound.play()
                        money += click_power
                    else:
                        money += click_power
                        poyo.play()
                        
                if battle:
                    if season_color != "com.png":
                        causes = [True, True, True, True, False]
                        cause = random.choice(causes)
                        if cause is True:
                            current_boss_health -= click_power 
                            if ability != None:
                                sound.play()
                                money += click_power
                        else:
                            money -= 1
                        if current_boss_health <= 20:
                            victory.play()
                            if index < 7 and fight < 8:      
                                fight += 1
                                money += current_boss["extra"]
                                index += 1
                                pro_level += 1
                                current_boss = bosses[index]
                                current_boss_health = current_boss["health"]
                                kirby = pygame.image.load(f"images/{current_boss['real']}")
                                kirby_rect = kirby.get_rect(center=(center_x, center_y))
                            else:
                                kirby = last_kirby
                                posi = (0, 0)
                                fight = 1
                                index = 0
                                season_color = "com.png"
                                background = pygame.image.load(f"images/{season_color}")
    
                    if ability != None:
                        sound.play()

                save_game()
            window_visible = True

            if shopping:
                upgrade_button = pygame.Rect(int(center_x - 200), int(center_y + 40), 495, 60)
                if upgrade_button.collidepoint(pos) and money >= upgrade_cost:
                    click_power += random.randint(1, 5)
                    money -= upgrade_cost
                    upgrade_cost = click_power * 3 + 5
                    save_game()

            change_button = pygame.Rect(width - 400, 90, 370, 70)
            if change_button.collidepoint(pos) and not kirbyy and not shop and not battle and not shopping and not updating:
                typing = True
                adding = ""
                add_name()

            shop_rect = pygame.Rect(100, 450, 200, 50)
            if shop_rect.collidepoint(pos) and not kirbyy and not battle:
                shop = not shop
            
            if shop:
                for choice in choices:
                    choice["rect"] = pygame.Rect(choice["pos"], (49, 49))
                    if choice["rect"].collidepoint(pos) and not battle:
                        if not choice["bought"] and money >= choice["cost"]:
                            money -= choice["cost"]
                            choice["bought"] = True
                            choice["color"] = (0, 255, 0)
                            selected = choice["real"]
                            kirby = pygame.image.load(f"images/{selected}")
                            poyo.play()
                        elif choice["bought"]:
                            selected = choice["real"]
                            kirby = pygame.image.load(f"images/{selected}")
                            poyo.play()
              
                        
            if power_button.collidepoint(pos) and not shop and not battle:
                kirbyy = True
                typing = False

            if battle_rect.collidepoint(pos) and not battle and not updating and not shop:
                fight = 1
                pressed = True
                pygame.mixer.music.stop()
                arena()
                boom.play()

            if kirbyy:
                for power1 in abilitys:
                    if power1["rect"].collidepoint(pos) and not battle:
                        if power1["bought"] is False and money >= power1["cost"]:
                            money -= power1["cost"]
                            ability = power1["sound"]
                            copykirby.play()
                        else:
                            if power1["bought"]:
                                money -= power1["cost"]
                                ability = power1["sound"]
                                copykirby.play()
                                
                
            
   
        elif event.type == pygame.KEYUP:
            if battle:
                pressed = False
                battle = False
                sending_message = True
                shopping = False
                shop = False
                reading = False
                kirbyy = False

    delta_time = clock.tick(60) / 1000
    instanly_change_season()
    if  max_y != 400 or max_ys != height + 400:
        max_y = 400
        max_ys = height + 400
    if pause:
        screen.fill((0, 0, 0))
        
        screen.blit(pause_image, (0, 0))
    elif not pause:
        play_sound()
        now = pygame.time.get_ticks()
        elapsed_time = now - start_time
        if ability != None:
            sound = pygame.mixer.Sound(f"{ability}")
        if elapsed_time >= 1300:
            start_now = True
        if not start_now:
            screen.fill((0, 255, 20))
            background_img = pygame.image.load(f"images/{season_color}")
            background = pygame.transform.scale(background_img, (width, height))        
            pause = False
        elif start_now:
            if not battle:
                season_color = "background.png"
            if not season_page and not sending_message:
                draw_screen()
            elif season_page:
                event_draw()
            background_img = pygame.image.load(f"images/{season_color}")
            background = pygame.transform.scale(background_img, (width + 100, height + 100))
            elapsed = pygame.time.get_ticks() - start_time
            if elapsed >= 300000:
                give_daily_bonus()
                current_hour += 1
                current_reward += random.randint(20, 50)
                start_time =  pygame.time.get_ticks()
                
            beyond()
            if not sending_message and not season_page and not shop and not shopping and not battle and not kirbyy and not updating:
                pygame.draw.rect(screen, (255, 255, 0), (width - 190, height - 120, 175, 60), border_radius=9)
                screen.blit(icon2, (width - 150, height - 150))
                
        if shop:
            draw_kirby()
        if not sending_message and not shopping and not kirbyy and not shop and start_now and not battle and not season_page:
            start = font.render(f"The Arena", True, (255, 255, 255))
            battle_rect = pygame.Rect(100, height / 2, 200, 60)
            pygame.draw.rect(screen, (255, 0, 0), battle_rect, border_radius=12)
            screen.blit(start, (130, height / 2 + 10))
            if season != None:
                start2 = bigger.render(f"{season}", True, (255, 255, 255))
                pygame.draw.rect(screen, (234, 4, 255), (100, height / 2 - 70, 200, 60), border_radius=5)
                screen.blit(start2, (110, height / 2 - 51))
        if updating:
            show_updates()
        if not sending_message and not shopping and not shop and not kirbyy and not battle and start_now and not updating and not season_page:
            update_rect = pygame.Rect(width - 190, height - 50, 190, 60)
            pygame.draw.rect(screen, (0, 255, 90), update_rect, border_radius=12)
            up = font.render("Update Log", True, (255, 255, 255))
            screen.blit(up, (width - 170, height - 40))


        if money > MAX_COINS:
            money = MAX_COINS
        if click_power > MAX_CLICK_POWER:
            click_power = MAX_CLICK_POWER

        
        if battle:
            if season_color == "dun.png":
                posi = (0, 0)
            elif season_color == "arena.png":
                posi = (-50, -50)
            elif season_color == "super.png":
                posi = (0, 0)
        if pro and not shop:
            draw_rewards()
            add_reward()
        if not reading and not battle and not shop and not kirbyy and not season_page:
            chapter()
        if reading:
            show_story()
            pygame.draw.rect(screen, (100, 100, 100), (center_x - 450, height - 70, 180, 50))
            pygame.draw.rect(screen, (100, 100, 100), (center_x - 200, height - 70, 180, 50))
            pygame.draw.rect(screen, (100, 100, 100), (center_x, height - 70, 180, 50))
            pygame.draw.rect(screen, (100, 100, 100), (center_x + 250, height - 70, 180, 50))
            label1 = font.render("Chapter 1", True, (255, 255, 255))
            label2 = font.render("Chapter 2", True, (255, 255, 255))
            label3 = font.render("Chapter 3", True, (255, 255, 255))
            label4 = font.render("Chapter 4", True, (255, 255, 255))
            screen.blit(label1, (center_x - 440, height - 60))
            screen.blit(label2, (center_x - 190, height - 60))
            screen.blit(label3, (center_x + 10, height - 60))
            screen.blit(label4, (center_x + 240, height - 60))
            updating = False
            
        
        if not pro and not shop and not season_page and not kirbyy and len(allys) > 0 and not updating and not reading:
            for ally in allys:
                allya = pygame.image.load(f"allies/{ally['image']}")
                screen.blit(allya, (ally["rect"].x, ally["rect"].y))
                ally_sound = pygame.mixer.Sound(f"Sounds/{ally['sound']}")
                if ally["rect"].x < kirby_rect.x:
                    ally["rect"].x += ally["speed"]
                if ally["rect"].x > kirby_rect.x:
                    ally["rect"].x -= ally["speed"]
                if ally["rect"].y < kirby_rect.y:
                    ally["rect"].y += ally["speed"]
                if ally["rect"].y > kirby_rect.y:
                    ally["rect"].y -= ally["speed"]
                if ally["rect"].colliderect(kirby_rect):
                    hit = True
                    shock = True
                    shock_now = pygame.time.get_ticks()
                    if not battle:
                        if ability != None:
                            ally_sound.play()
                            money += ally["damage"]
                        else:
                            money += click_power
                            ally_sound.play()
                    elif battle:
                        if season_color != "com.png":
                            causes = [True, True, True, True, False]
                            cause = random.choice(causes)
                            if cause is True:
                                current_boss_health -= ally["damage"]
                                ally_sound.play()
                            else:
                                money -= 1
                            if current_boss_health <= 0:
                                victory.play()
                                if index < 7:      
                                    fight += 1
                                    money += current_boss["extra"]
                                    index += 1
                                    pro_level += 0.50
                                    current_boss = bosses[index]
                                    current_boss_health = current_boss["health"]
                                    kirby = pygame.image.load(f"images/{current_boss['real']}")
                                    kirby_rect = kirby.get_rect(center=(center_x, center_y))
                                else:
                                    kirby = last_kirby
                                    posi = (0, 0)
                                    fight = 1
                                    index = 0
                                    season_color = "com.png"
                                    background = pygame.image.load(f"images/{season_color}")
                        if ability != None:
                            sound.play()


                        
        pygame.display.update()

save_game()
pygame.quit()
