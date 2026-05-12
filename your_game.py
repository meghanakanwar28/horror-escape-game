import tkinter as tk
import os
import threading
import time
import random
import winsound

# =========================
# WINDOW
# =========================
root = tk.Tk()
root.title("😈 Horror Escape")
root.geometry("900x600")
root.configure(bg="#050505")
root.attributes("-fullscreen", True)

# =========================
# GAME STATE
# =========================
time_left = 60
health = 3
current_room = 1
inventory = []
game_running = True

# =========================
# PATHS
# =========================
current_folder = os.path.dirname(os.path.abspath(__file__))

image_path = os.path.join(current_folder, "image.png")
sound_path = os.path.join(current_folder, "horror.wav")

# =========================
# LOAD IMAGE
# =========================
ghost_img = None

try:
    ghost_img = tk.PhotoImage(file=image_path)
    ghost_img = ghost_img.subsample(2, 2)
    print("✅ Image Loaded")

except Exception as e:
    print("❌ Image Error:", e)

# =========================
# TITLE
# =========================
title = tk.Label(
    root,
    text="😈 HORROR ESCAPE 😈",
    font=("Arial", 28, "bold"),
    fg="red",
    bg="#050505"
)
title.pack(pady=10)

# =========================
# INFO BAR
# =========================
info = tk.Label(
    root,
    text="",
    font=("Consolas", 14, "bold"),
    fg="lime",
    bg="#050505"
)
info.pack(pady=5)

# =========================
# IMAGE LABEL
# =========================
image_label = tk.Label(
    root,
    bg="#050505"
)
image_label.pack(pady=10)

# =========================
# MESSAGE BOX
# =========================
msg = tk.Label(
    root,
    text="Find the key and escape before the ghost kills you...",
    font=("Arial", 14, "bold"),
    fg="orange",
    bg="#050505",
    wraplength=700,
    justify="center"
)
msg.pack(pady=15)

# =========================
# BUTTON FRAME
# =========================
frame = tk.Frame(root, bg="#050505")
frame.pack(pady=20)

# =========================
# FUNCTIONS
# =========================
def update_ui():
    info.config(
        text=f"⏳ Time: {time_left}   ❤️ Health: {health}   🚪 Room: {current_room}   🎒 Inventory: {inventory}"
    )

def flash_screen():
    root.configure(bg="darkred")

    widgets = [title, info, msg, frame, image_label]

    for widget in widgets:
        widget.configure(bg="darkred")

    root.after(150, reset_flash)

def reset_flash():
    root.configure(bg="#050505")

    widgets = [title, info, msg, frame, image_label]

    for widget in widgets:
        widget.configure(bg="#050505")

def flicker_title():
    colors = ["red", "darkred", "white"]

    title.config(fg=random.choice(colors))

    root.after(300, flicker_title)

def play_sound():
    while game_running:

        if os.path.exists(sound_path):
            try:
                winsound.PlaySound(
                    sound_path,
                    winsound.SND_FILENAME | winsound.SND_ASYNC
                )
            except:
                pass

        time.sleep(8)

def stop_game():
    global game_running

    game_running = False

    next_btn.config(state="disabled")
    search_btn.config(state="disabled")
    escape_btn.config(state="disabled")
    jump_btn.config(state="disabled")

def show_jumpscare():

    flash_screen()

    if ghost_img:
        image_label.config(image=ghost_img)
        image_label.image = ghost_img

    else:
        image_label.config(
            text="👻 IMAGE NOT FOUND",
            fg="red",
            bg="#050505",
            font=("Arial", 20, "bold")
        )

    if os.path.exists(sound_path):
        try:
            winsound.PlaySound(
                sound_path,
                winsound.SND_FILENAME | winsound.SND_ASYNC
            )
        except:
            pass

def next_room():
    global current_room

    if not game_running:
        return

    current_room += 1

    scary_texts = [
        "🚪 You entered a dark room...",
        "💀 You heard footsteps nearby...",
        "🩸 Blood is dripping from the ceiling...",
        "👻 Something moved in the shadows...",
        "😨 The room feels colder..."
    ]

    msg.config(text=random.choice(scary_texts))

    image_label.config(image="")
    image_label.config(text="")

    update_ui()

def search_room():
    if not game_running:
        return

    items = ["Key", "Torch", "Knife", "Map"]

    found = random.choice(items)

    inventory.append(found)

    msg.config(text=f"🔍 You found: {found}")

    update_ui()

def escape_game():
    global game_running

    if not game_running:
        return

    if "Key" in inventory:

        msg.config(
            text="🏆 YOU ESCAPED THE HORROR HOUSE!"
        )

        stop_game()

    else:
        msg.config(
            text="🚫 You need a KEY to escape!"
        )

def game_over():
    global game_running

    game_running = False

    msg.config(
        text="💀 GAME OVER 💀"
    )

    show_jumpscare()

    stop_game()

def timer():
    global time_left
    global health

    if not game_running:
        return

    if time_left > 0 and health > 0:

        time_left -= 1

        # RANDOM ATTACK
        if random.randint(1, 5) == 3:

            health -= 1

            attack_msgs = [
                "👻 A ghost attacked you!",
                "🔪 Something scratched you!",
                "💀 A dark shadow hit you!",
                "😨 You feel something behind you!",
                "🩸 The ghost found you!"
            ]

            msg.config(text=random.choice(attack_msgs))

            show_jumpscare()

        update_ui()

        root.after(1000, timer)

    else:
        game_over()

# =========================
# BUTTONS
# =========================
next_btn = tk.Button(
    frame,
    text="Next Room 🚪",
    command=next_room,
    bg="#222222",
    fg="red",
    font=("Arial", 12, "bold"),
    width=16,
    relief="raised",
    bd=4
)
next_btn.grid(row=0, column=0, padx=8)

search_btn = tk.Button(
    frame,
    text="Search 🔍",
    command=search_room,
    bg="#222222",
    fg="gold",
    font=("Arial", 12, "bold"),
    width=16,
    relief="raised",
    bd=4
)
search_btn.grid(row=0, column=1, padx=8)

escape_btn = tk.Button(
    frame,
    text="Escape 🏃",
    command=escape_game,
    bg="#222222",
    fg="lime",
    font=("Arial", 12, "bold"),
    width=16,
    relief="raised",
    bd=4
)
escape_btn.grid(row=0, column=2, padx=8)

jump_btn = tk.Button(
    frame,
    text="Jumpscare 😱",
    command=show_jumpscare,
    bg="#222222",
    fg="purple",
    font=("Arial", 12, "bold"),
    width=16,
    relief="raised",
    bd=4
)
jump_btn.grid(row=0, column=3, padx=8)

# =========================
# EXIT FULLSCREEN
# =========================
def exit_fullscreen(event=None):
    root.attributes("-fullscreen", False)

root.bind("<Escape>", exit_fullscreen)

# =========================
# START BACKGROUND SOUND
# =========================
threading.Thread(
    target=play_sound,
    daemon=True
).start()

# =========================
# START GAME
# =========================
update_ui()
flicker_title()
timer()

# =========================
# RUN
# =========================
root.mainloop()