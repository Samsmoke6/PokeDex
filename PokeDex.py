from customtkinter import *
import tkinter as tk
import pyglet
import requests
from PIL import Image, ImageTk
from urllib.request import urlopen

# IMPORT CUSTOM FONT
pyglet.options['win32_gdi_font'] = True
font_file_path = 'PixelifySans.ttf'
pyglet.font.add_file(font_file_path)

# WINDOW
window = tk.Tk()
window.geometry("550x700")
window.resizable(width=False, height=False)
window.title("PokeDex")

# PokeAPI
def get_overview():
    # CURSOR
    square_frame = CTkFrame(master=info_frame,
                            width=5,
                            height=5,
                            fg_color="white",
                            corner_radius=0,
                            )
    square_frame.place(x=12, y=19)
    topics = ["Stats", "Moves", "Abilities", "Games", "- - - - - - - - - - - - - - - - - -  "]
    # NAME + ID
    poke_name_input = (pokemon_entry.get()).lower()
    url = f"{base_url}pokemon/{poke_name_input}"
    response = requests.get(url)
    poke_data = response.json()

    global current_info
    current_info = topics
    info_label_var.set(("\n\n".join(current_info)))
    # ELEMENT
    if len(poke_data['types']) == 1:
        overview_label_var.set(
            f"{poke_data['name'].capitalize()}\n"
            f"ID: {poke_data['id']}\n\n"
            f"{poke_data['types'][0]['type']['name']}\n")
    else:
        overview_label_var.set(
            f"{poke_data['name'].capitalize()}\n"
            f"ID: {poke_data['id']}\n\n"
            f"{poke_data['types'][0]['type']['name']}\n"
            f"{poke_data['types'][1]['type']['name']}")

def get_image():
    poke_name_input = (pokemon_entry.get()).lower()
    url = f"{base_url}pokemon/{poke_name_input}"
    response = requests.get(url)
    poke_data = response.json()

    global sprite1
    global sprite2

    # FRONT IMAGE
    poke_front = poke_data["sprites"]["front_default"]
    imageUrl1 = poke_front
    u = urlopen(imageUrl1)
    raw_data = u.read()
    u.close()
    photo1 = ImageTk.PhotoImage(data=raw_data)
    sprite1.config(image = photo1)
    sprite1.image = photo1

    # BACK IMAGE
    poke_back = poke_data["sprites"]["back_default"]
    print(poke_back)
    if poke_back:
        imageUrl2 = poke_back
        u = urlopen(imageUrl2)
        raw_data = u.read()
        u.close()
        photo2 = ImageTk.PhotoImage(data=raw_data)
        photo1 = ImageTk.PhotoImage(data=raw_data)
        sprite2.config(image=photo2)
        sprite2.image = photo2
        sprite1.place(x=0, y=20)
    else:
        sprite1.place(x=40, y=20)
        sprite2.config(image = "")

def update_screen():
    get_overview()
    get_image()

def scroll_down():
    current_info_save = current_info.pop(0)
    current_info.append(current_info_save)

    info_label_var.set(("\n\n".join(current_info)))

def scroll_up():
    current_info_save = current_info.pop(len(current_info) - 1)
    current_info.insert(0, current_info_save)

    info_label_var.set(("\n\n".join(current_info)))

def stats_info():
    stats_list = []
    stats_base_list = []
    stats_name_list = []
    poke_name_input = (pokemon_entry.get()).lower()
    url = f"{base_url}pokemon/{poke_name_input}"
    response = requests.get(url)
    poke_data = response.json()

    count = 0
    while count < len(poke_data['stats']):
        stats_base_list.append(poke_data['stats'][count]['base_stat'])
        stats_name_list.append(poke_data['stats'][count]['stat']['name'])
        count += 1
    count = 0
    while count <= 5:
        stats_list.append(f"{stats_name_list[count]}: {stats_base_list[count]}")
        count += 1
    stats_list.append("- - - - - - - - - - - - - - - - - -  ")
    global current_info
    current_info = stats_list
    info_label_var.set(("\n\n".join(current_info)))

def topic_pick():
    if current_info[0] == "Stats":
        stats_info()
    elif current_info[0] == "Moves":
        moves_info()
    elif current_info[0] == "Abilities":
        abilities_info()
    elif current_info[0] == "Games":
        games_info()

def moves_info():
    moves_list = []
    poke_name_input = (pokemon_entry.get()).lower()
    url = f"{base_url}pokemon/{poke_name_input}"
    response = requests.get(url)
    poke_data = response.json()

    count = 0
    while count < len(poke_data['moves']):
        moves_list.append(poke_data['moves'][count]['move']['name'])
        count += 1
    count = 0
    moves_list.append("- - - - - - - - - - - - - - - - - -  ")
    global current_info
    current_info = moves_list
    info_label_var.set(("\n\n".join(current_info)))

def abilities_info():
    abilities_list = []
    poke_name_input = (pokemon_entry.get()).lower()
    url = f"{base_url}pokemon/{poke_name_input}"
    response = requests.get(url)
    poke_data = response.json()

    count = 0
    print(len(poke_data['abilities']))
    while count < len(poke_data['abilities']):
        abilities_list.append(poke_data['abilities'][count]['ability']['name'])
        count += 1
    abilities_list.append("- - - - - - - - - - - - - - - - - -  ")
    global current_info
    current_info = abilities_list
    info_label_var.set(("\n\n".join(current_info)))

def games_info():
    games_list = []
    poke_name_input = (pokemon_entry.get()).lower()
    url = f"{base_url}pokemon/{poke_name_input}"
    response = requests.get(url)
    poke_data = response.json()

    count = 0
    while count < len(poke_data['game_indices']):
        games_list.append(poke_data['game_indices'][count]['version']['name'])
        count += 1
    count = 0
    games_list.append("- - - - - - - - - - - - - - - - - -  ")
    global current_info
    current_info = games_list
    info_label_var.set(("\n\n".join(current_info)))

# VARIABLES
poke_name = tk.StringVar()
poke_ID = tk.StringVar()
poke_element = tk.StringVar()
topic_save = ""
topics = ["Stats","Moves","Abilities","Games","- - - - - - - - - - - - - - - - - -  "]
info_label_var = tk.StringVar()
base_url = "https://pokeapi.co/api/v2/"
overview_label_var = tk.StringVar()
stats_base_list = []
stats_name_list = []
stats_list = []
moves_list = []
abilities_list = []
games_list = []
dpad = CTkImage(light_image=Image.open('d-pad.png'),dark_image=Image.open('d-pad.png'),size=(160,145))
details = CTkImage(light_image=Image.open('details.png'),dark_image=Image.open('details.png'),size=(238,130))
global current_info


# FRAMES + BUTTONS
side = CTkFrame(master=window,
                 width=550,
                 height=700,
                 fg_color="#8E3433",
                 corner_radius=0,
                 border_color="black",
                 border_width=5,
                 )
side.place(x=0, y=0)
front = CTkFrame(master=window,
                 width=500,
                 height=700,
                 fg_color="#C04C4B",
                 corner_radius=0,
                 border_color="black",
                 border_width=5
                 )
front.place(x=50, y=0)
screen_front = CTkFrame(master=front,
                 width=413,
                 height=462,
                 fg_color="#B9B9B9",
                 border_color="black",
                 corner_radius=0,
                 border_width=4
                 )
screen_front.place(x=48, y=45)
screen = CTkFrame(master=front,
                 width=400,
                 height=450,
                 fg_color="#D9D9D9",
                 border_color="black",
                 corner_radius=0,
                 border_width=4
                 )
screen.place(x=60, y=45)
text_area = CTkFrame(master=front,
                 width=350,
                 height=340,
                 fg_color="#464646",
                 border_color="#B9B9B9",
                 corner_radius=0,
                 border_width=8
                 )
text_area.place(x=85, y=70)
pokemon_entry = CTkEntry(master=screen,
                        placeholder_text="Pokemon Name/ID",
                        placeholder_text_color="white",
                        height=50,
                        width=180,
                        border_color="black",
                        border_width=4,
                        corner_radius=0,
                        fg_color="#38A710",
                        justify="center",
                        font=("Pixelify Sans", 18))
pokemon_entry.place(x=194, y=380)
dpad_image = CTkLabel(master=front, text="",image=dpad)
dpad_image.place(x=300,y=530)
details_image = CTkLabel(master=front, text="",image=details)
details_image.place(x=50,y=528)
search_button = CTkButton(master=screen,
                          height=50,
                          width=50,
                          corner_radius=50,
                          text="",
                          fg_color="#D84644",
                          border_color="black",
                          border_width=4,
                          command=update_screen)
search_button.place(x=130, y=380)
up_button = CTkButton(master=front,
                          height=30,
                          width=30,
                          corner_radius=0,
                          text="",
                          fg_color="#464646",
                          border_color="black",
                          hover_color= "#464646",
                          border_width=0,
                          command=scroll_up)
up_button.place(x=370, y=540)
down_button = CTkButton(master=front,
                          height=30,
                          width=30,
                          corner_radius=0,
                          text="",
                          fg_color="#464646",
                          border_color="black",
                          hover_color= "#464646",
                          border_width=0,
                          command=scroll_down)
down_button.place(x=370, y=625)
enter_button = CTkButton(master=front,
                          height=22,
                          width=22,
                          corner_radius=0,
                          text="",
                          fg_color="#464646",
                          border_color="#464646",
                          border_width=1,
                          hover_color= "#464646",
                          command=topic_pick)
enter_button.place(x=375, y=586)
overview_frame = CTkFrame(master=text_area,
                 width=120,
                 height=140,
                 fg_color="#242424",
                 corner_radius=0,
                 )
overview_frame.place(x=17,y=17)
pic_frame = CTkFrame(master=text_area,
                 width=188,
                 height=140,
                 fg_color="#242424",
                 corner_radius=0,
                 )
pic_frame.place(x=145,y=17)
info_frame = CTkFrame(master=text_area,
                 width=317,
                 height=157,
                 fg_color="#242424",
                 corner_radius=0,
                 )
info_frame.place(x=17,y=165)


# TEXT
overview_label = CTkLabel(master=overview_frame,
                          textvariable=overview_label_var,
                          fg_color="transparent",
                          font=('Pixelify Sans', 18),
                          justify="left")
overview_label.place(x=10,y=10)
info_label = CTkLabel(master=info_frame,
                          textvariable=info_label_var,
                          fg_color="transparent",
                          font=('Pixelify Sans', 18),
                          justify="left")
info_label.place(x=25,y=10)

# SPRITES
sprite1 = tk.Label(master=pic_frame, bg="#242424")
sprite1.place(x=0, y=20)
sprite2 = tk.Label(master=pic_frame, bg="#242424")
sprite2.place(x=90, y=20)

# RUN
window.mainloop()