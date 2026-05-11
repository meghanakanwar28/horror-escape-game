import tkinter as tk
import os
import threading
import time
import random
import winsound

# --- WINDOW ---
root = tk.Tk()
root.title("😈 Horror Escape")
root.geometry("700x520")
root.configure(bg="#050505")
root.attributes("-fullscreen", True)

# --- GAME STATE ---
time_left = 60
health = 3
current_room = "Room 1"
inventory = []

# --- IMAGE LOAD ---
try:
    current_folder = os.path.dirname(__file__)
    image_path = os.path.join(current_folder, "image.png")

    ghost_img = tk.PhotoImage(file=image_path)
    ghost_img = ghost_img.subsample(2, 2)

    print("✅ Image loaded successfully")

except Exception as e:
    print("❌ Image error:", e)
    ghost_img = None

# --- UI ---
title = tk.Label(
    root,
    text="😈 HORROR ESCAPE",
    font=("Arial", 24, "bold"),
    fg="red",
    bg="#050505"
)
title.pack(pady=10)

info = tk.Label(
    root,
    text="",
    font=("Consolas", 12, "bold"),
    fg="lime",
    bg="#050505"
)
info.pack(pady=5)

image_label = tk.Label(root, bg="#050505")
image_label.pack(pady=10)

msg = tk.Label(
    root,
    text="Find a way to escape...",
    font=("Arial", 13, "bold"),
    fg="orange",
    bg="#050505",
    wraplength=700
)
msg.pack(pady=10)

# --- BUTTON FRAME ---
frame = tk.Frame(root, bg="#050505")
frame.pack(pady=10)

# --- FUNCTIONS ---
def is_game_active():
    return health > 0 and time_left > 0

def update_ui():
    info.config(
        text=f"⏳ Time: {time_left}   ❤️ Health: {health}   🚪 {current_room}   🎒 {inventory}"
    )

def flicker():
    colors = ["red", "darkred", "white"]
    title.config(fg=random.choice(colors))
    root.after(300, flicker)

def flash_screen():
    root.configure(bg="darkred")

    title.configure(bg="darkred")
    info.configure(bg="darkred")
    msg.configure(bg="darkred")
    frame.configure(bg="darkred")
    image_label.configure(bg="darkred")

    root.after(120, reset_flash)

def reset_flash():
    root.configure(bg="#050505")

    title.configure(bg="#050505")
    info.configure(bg="#050505")
    msg.configure(bg="#050505")
    frame.configure(bg="#050505")
    image_label.configure(bg="#050505")

def disable_buttons():
    next_btn.config(state="disabled")
    search_btn.config(state="disabled")
    escape_btn.config(state="disabled")
    jump_btn.config(state="disabled")

# --- JUMPSCARE ---
def show_jumpscare():
    if ghost_img:
        image_label.config(image=ghost_img)
        image_label.image = ghost_img
    else:
        image_label.config(
            text="👻 IMAGE ERROR",
            fg="red",
            bg="#050505"
        )

    flash_screen()

    if os.path.exists("horror.wav"):
        winsound.PlaySound("horror.wav", winsound.SND_ASYNC)

# --- TIMER ---
def timer():
    global time_left, health

    if time_left > 0 and health > 0:
        time_left -= 1

        # Random horror attack
        if random.randint(1, 5) == 3:
            health -= 1

            scares = [
                "👻 Something attacked you!",
                "💀 You heard footsteps...",
                "😨 Something is watching you...",
                "🔪 A shadow moved nearby...",
                "🩸 You feel cold breath..."
            ]

            msg.config(text=random.choice(scares))

            show_jumpscare()

        update_ui()

        root.after(1000, timer)

    else:
        game_over()

# --- BACKGROUND SOUND ---
def play_sound():
    while True:
        if os.path.exists("horror.wav"):
            winsound.PlaySound("horror.wav", winsound.SND_ASYNC)

        time.sleep(6)

threading.Thread(target=play_sound, daemon=True).start()

# --- GAME ACTIONS ---
def next_room():
    global current_room

    if not is_game_active():
        return

    current_room = "Room " + str(random.randint(1, 5))

    msg.config(text="🚪 You moved to another room...")

    image_label.config(image="")
    image_label.config(text="")

    update_ui()

def search():
    if not is_game_active():
        return

    items = ["Key", "Torch", "Map", "Knife"]

    found = random.choice(items)

    inventory.append(found)

    msg.config(text=f"🔍 You found: {found}")

    update_ui()

def escape():
    if not is_game_active():
        return

    if "Key" in inventory:
        msg.config(text="🏃 You escaped successfully! YOU WIN 😈")

        disable_buttons()

    else:
        msg.config(text="🚫 You need a key!")

    update_ui()

def game_over():
    msg.config(text="💀 GAME OVER")

    image_label.config(image="")
    image_label.config(text="")

    disable_buttons()

# --- BUTTONS ---
next_btn = tk.Button(
    frame,
    text="Next Room 🚪",
    command=next_room,
    bg="#222222",
    fg="red",
    activebackground="darkred",
    activeforeground="white",
    font=("Arial", 11, "bold"),
    width=15,
    relief="raised",
    bd=3
)
next_btn.grid(row=0, column=0, padx=5)

search_btn = tk.Button(
    frame,
    text="Search 🔍",
    command=search,
    bg="#222222",
    fg="gold",
    activebackground="darkred",
    activeforeground="white",
    font=("Arial", 11, "bold"),
    width=15,
    relief="raised",
    bd=3
)
search_btn.grid(row=0, column=1, padx=5)

escape_btn = tk.Button(
    frame,
    text="Escape 🏃",
    command=escape,
    bg="#222222",
    fg="lime",
    activebackground="darkred",
    activeforeground="white",
    font=("Arial", 11, "bold"),
    width=15,
    relief="raised",
    bd=3
)
escape_btn.grid(row=0, column=2, padx=5)

jump_btn = tk.Button(
    frame,
    text="Jumpscare 😱",
    command=show_jumpscare,
    bg="#222222",
    fg="purple",
    activebackground="darkred",
    activeforeground="white",
    font=("Arial", 11, "bold"),
    width=15,
    relief="raised",
    bd=3
)
jump_btn.grid(row=0, column=3, padx=5)

# --- EXIT FULLSCREEN ---
def exit_fullscreen(event=None):
    root.attributes("-fullscreen", False)

root.bind("<Escape>", exit_fullscreen)

# --- START GAME ---
flicker()
update_ui()
timer()

root.mainloop()