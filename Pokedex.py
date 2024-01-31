import pypokedex
import PIL.Image, PIL.ImageTk
import tkinter as tk
from tkinter import *
import urllib3 
from io import BytesIO
from PIL import Image

img_ref = None #this is to help with the image error
global_image_list = [] # making an empty global image list
background_list = [] #not optimized but a solution to the background

#initiallize direction of sprite
global direction
direction = "front"

#Dex Entry Window
class dexEntry(Toplevel):
    
    def __init__(self, master = None):
            
        super().__init__(master = master)
        self.geometry("512x364")
        self.resizable(width=False, height=False)
        
        # Create Window Canvas
        self.my_canvas = Canvas(self, width=512, height=364, bd=0, highlightthickness=0)
        self.my_canvas.pack(fill="both", expand=True)
        
        # Set Pokedex Entry background
        image = Image.open("images/Pokedex Screen.png")
        resize_image = image.resize((512, 364))
        img = PIL.ImageTk.PhotoImage(resize_image)
        c = self.my_canvas.create_image(0, 0, image=img, anchor="nw")
        
        def add_image_to_background_list(image):
            global background_list
            background_list.append(image)

        add_image_to_background_list(img)
        

        #Pokemon Information
        self.pokemon_info = self.my_canvas.create_text(380, 60, text=f" ", font=("Consolas", 12), fill= "black")
        self.pokemon_image = self.my_canvas.create_image(150,152)
        self.pokemon_type = self.my_canvas.create_text(375, 95, text=f" ", font=("Consolas", 12))
        self.pokemon_height = self.my_canvas.create_text(395, 185, text=f" ", font=("Consolas", 12), fill= "black")
        self.pokemon_weight = self.my_canvas.create_text(395, 215, text=f" ", font=("Consolas", 12), fill= "black")
        self.pokemon_basestats1 = self.my_canvas.create_text(256, 280, text=f" ", font=("Consolas", 14), fill= "black", width=500)
        self.pokemon_basestats2 = self.my_canvas.create_text(256, 305, text=f" ", font=("Consolas", 14), fill= "black", width=500)
        self.pokemon_speed = self.my_canvas.create_text(256, 330, text=f" ", font=("Consolas", 14), fill= "black", width=400)
        self.error_message = self.my_canvas.create_text(256, 300, text=f" ", font=("Consolas", 12), fill= "red")
        self.sprite_error = self.my_canvas.create_text(120,8, text=f" ", font=("Consolas", 10), fill = "red")

        self.front_img = None
        self.back_img = None
        self.missingno_img = None

        def add_image_to_global_list(image):
            global global_image_list
            global_image_list.append(image)
    
        def load_pokemon(Pokemon_Entry):
            try: 
                pokemon = pypokedex.get(name=Pokemon_Entry.get())
                self.title(f"Pokedex Entry No.{pokemon.dex} - {pokemon.name}".title())
                http = urllib3.PoolManager()
                #get front sprite (if there is one) and display it
                if pokemon.sprites.front.get('default'):
                    response = http.request('GET', pokemon.sprites.front.get('default'), preload_content=False)
                    if response.status == 200:
                        image = PIL.Image.open(BytesIO(response.data))
                        resize_image = image.resize((200, 200))
                        self.front_img = PIL.ImageTk.PhotoImage(resize_image)
                        add_image_to_global_list(self.front_img)
                        self.my_canvas.itemconfig(self.pokemon_image, image=self.front_img)
                        response.release_conn()  # Release the connection
                #get back sprite (if there is one) and implement turn sprite button
                    if pokemon.sprites.back.get('default'):
                        response = http.request('GET', pokemon.sprites.back.get('default'), preload_content=False)
                        if response.status == 200:
                            image2 = PIL.Image.open(BytesIO(response.data))
                            resize_image2 = image2.resize((200, 200))
                            self.back_img = PIL.ImageTk.PhotoImage(resize_image2)
                            add_image_to_global_list(self.back_img)
                            response.release_conn()  # Release the connection

                                #function for turn sprite button
                            def switchsprite():
                                global direction
                                if direction == "front":
                                    self.my_canvas.itemconfig(self.pokemon_image, image=self.back_img)
                                    direction = "back"
                                    return
                                if direction == "back":
                                    self.my_canvas.itemconfig(self.pokemon_image, image =self.front_img)
                                    direction = "front"
                                    return
                        
                        #turn sprite button
                        sprite_btn = Button(self.my_canvas, text= "TURN SPRITE", font=("Consolas", 8), width = 15, command=switchsprite)
                        back_sprite_btn_window = self.my_canvas.create_window(66,50, window=sprite_btn)
                else: 
                    # Handle unsuccessful response in sprite fetching
                    image = PIL.Image.open("images/MissingNo.png")
                    resize_image = image.resize((200, 200))
                    self.missingno_img = PIL.ImageTk.PhotoImage(resize_image)
                    add_image_to_global_list(self.missingno_img)
                    self.my_canvas.itemconfig(self.pokemon_image, image=self.missingno_img)
                    self.my_canvas.itemconfig(self.sprite_error, text="Sprite does not exist in API.")
                    print("No Pokemon sprite in API")    

                #function for displaying the Pokemon Type(s)
                def Type_Colors():
                    #changing pokemon.types list of strings so that it is just words                        
                    poke_types = f"{pokemon.types}"
                    modified_list = poke_types.strip("[]").replace("'","").replace(", "," - ")

                    #18 pokemon types
                    primary_types = ["grass","poison","water","fire","normal","psychic","electric","fighting","bug",
                                        "fairy","dragon","ice","steel","rock","flying","ground","ghost","dark"]
                    # Color palette for each Pokemon type
                    color_palette = {"grass": "green","poison": "purple","water": "blue", "fire": "red", "normal": "gray","psychic": "violet red", "electric": "yellow",
                                        "fighting": "brown4", "bug": "yellow green", "fairy": "light pink", "dragon": "goldenrod", "ice": "cyan", "steel": "dim gray",
                                        "rock": "tan2", "flying": "Skyblue1", "ground": "sienna4", "ghost": "purple4", "dark": "midnight blue"}
                    #nested for loop, checking the type or dual-type of the pokemon, and assigning the text a color from the color pallette
                    for type1 in primary_types:
                        for type2 in primary_types:
                            if f"{type1}" == f"{modified_list}":
                                primary_color = color_palette.get(type1)
                                self.my_canvas.itemconfig(self.pokemon_type, fill=primary_color)
                                self.my_canvas.itemconfig(self.pokemon_type, text=" - ".join([t for t in pokemon.types]).title())
                                return
                            if f"{type1} - {type2}" == f"{modified_list}":
                                primary_color = color_palette.get(type1)
                                secondary_color = color_palette.get(type2)
                                pokemon_type1 = self.my_canvas.create_text(330, 95, text=f" ", font=("Consolas", 12))
                                self.my_canvas.itemconfig(pokemon_type1, text=f"{type1}".title(), fill=primary_color)
                                pokemon_type2 = self.my_canvas.create_text(420, 95, text=f" ", font=("Consolas", 12))
                                self.my_canvas.itemconfig(pokemon_type2, text=f"{type2}".title(), fill=secondary_color)
                                return
                        
                self.my_canvas.itemconfig(self.pokemon_info, text=f"No.{pokemon.dex} - {pokemon.name}".title())
                Type_Colors()
                self.my_canvas.itemconfig(self.pokemon_height, text=f"Height: {pokemon.height}0 cm")
                self.my_canvas.itemconfig(self.pokemon_weight, text=f"Weight: {pokemon.weight}00 g")
                self.my_canvas.itemconfig(self.pokemon_basestats1, text=f"HP: {pokemon.base_stats.hp} - Attack: {pokemon.base_stats.attack} - Defense: {pokemon.base_stats.defense}")
                self.my_canvas.itemconfig(self.pokemon_basestats2, text=f"Special Attack: {pokemon.base_stats.sp_atk} - Special Defense: {pokemon.base_stats.sp_def}")
                self.my_canvas.itemconfig(self.pokemon_speed, text=f"Speed: {pokemon.base_stats.speed}")
                

            except pypokedex.exceptions.PyPokedexHTTPError as e: #this is the error message that this api returns if it didnt find the pokemon it was looking for
                self.title("MISSINGNO.")
                image = PIL.Image.open("images/MissingNo.png")
                resize_image = image.resize((200, 200))
                self.missingno_img = PIL.ImageTk.PhotoImage(resize_image)
                add_image_to_global_list(self.missingno_img)

                self.my_canvas.itemconfig(self.pokemon_info, text="MISSINGNO.")
                self.my_canvas.itemconfig(self.pokemon_image, image=self.missingno_img)
                self.my_canvas.itemconfig(self.pokemon_type, text="???? - ????")
                self.my_canvas.itemconfig(self.pokemon_height, text="Height: ????")
                self.my_canvas.itemconfig(self.pokemon_weight, text="Weight: ????")
                self.my_canvas.itemconfig(self.sprite_error, text="The requested Pokemon was not found. Please try again.", font= ("Consolas", 10))
                print(e)

            except Exception as e: #if an error occurred and who on earth knows what it was, just tell the user an error occurred
                image = PIL.Image.open("images/MissingNo.png")
                resize_image = image.resize((200, 200))
                self.missingno_img = PIL.ImageTk.PhotoImage(resize_image)
                add_image_to_global_list(self.missingno_img)

                self.my_canvas.itemconfig(self.pokemon_info, text="MISSINGNO.")
                self.my_canvas.itemconfig(self.pokemon_image, image=self.missingno_img)
                self.my_canvas.itemconfig(self.pokemon_type, text="???? - ????")
                self.my_canvas.itemconfig(self.pokemon_height, text="Height: ????")
                self.my_canvas.itemconfig(self.pokemon_weight, text="Weight: ????")
                self.my_canvas.itemconfig(self.error_message, text="An error occurred. Please Try Again.", font= ("Consolas", 10))
                print(e)

        load_pokemon(Pokemon_Entry)

#Home Screen
Home = tk.Tk()
Home.geometry("360x640")
Home.resizable(width=False, height=False)
Home.title("Python Pokedex")

# Create Main Window Canvas
main = Canvas(Home, width=360, height=640, bd=0, highlightthickness=0)
main.pack(fill="both", expand=True)

# Set Pokedex background
image = Image.open("images/Home.png")
resize_image = image.resize((360, 640))
img = PIL.ImageTk.PhotoImage(resize_image)
c = main.create_image(0, 0, image=img, anchor="nw")

#Add Texts
title_text = main.create_text(180, 290, text="Python Pokedex", font=("Consolas", 30), fill="black")
main.create_text(180, 420, text="Enter Name or Pokedex #:", font=("Consolas", 15), fill= "black")
#Add Entry box
Pokemon_Entry = Entry(Home, font=("Consolas", 24), width=15, fg="black", bd=2)
Pokemon_window=main.create_window(180,460, window=Pokemon_Entry)
#Add Button
btn = Button(Home, text= "LOAD POKEMON", font=("Consolas", 20), width = 18, command = dexEntry)
load_btn_window = main.create_window(180,578, window=btn)

Home.mainloop()