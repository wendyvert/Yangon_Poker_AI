"""
============================================
THE SECRET POKER DEN OF YANGON
Poker AI with Prolog Integration
============================================


FILE SECTIONS:
- Lines 1-150:   Member 3 (Game Engine)
- Lines 151-280: Member 4 (Prolog Bridge)
- Lines 281-400: Member 5 (UI & Narrative)
============================================
"""

# ============================================
# MEMBER 3: Game Engine (Lines 1-150)
# ============================================

import random
import sys

# Placeholder for Member 3's code

# ============================================
# MEMBER 4: Prolog Bridge (Lines 151-280)
# ============================================

# Placeholder for Member 4's code

# ============================================
# MEMBER 5: UI & Narrative (Lines 281-400)
# ============================================

# ============================================
# MEMBER 5: UI & Narrative
# ============================================

import tkinter as tk
from PIL import Image, ImageTk


def show_yangon_intro():
    """Display the Yangon opening scene."""

    window = tk.Tk()
    window.title("The Secret Poker Den of Yangon")
    window.geometry("1000x700")

    # Load Yangon background image
    image = Image.open("images/yangon.jpg")
    image = image.resize((1000, 600))
    photo = ImageTk.PhotoImage(image)

    # Display image
    image_label = tk.Label(window, image=photo)
    image_label.pack()

    # Story text
    story = (
        "🌃 ရန်ကုန်မြို့ရဲ့ ညတစ်ညမှာ...\n\n"
        "One night in Yangon... a mysterious poker game is about to begin."
    )

    story_label = tk.Label(
        window,
        text=story,
        font=("Arial", 16),
        pady=15
    )
    story_label.pack()

    # Continue button
    continue_button = tk.Button(
        window,
        text="Continue →",
        font=("Arial", 14),
        command=window.destroy
    )
    continue_button.pack(pady=10)

    window.mainloop()

# ============================================
# MAIN ENTRY POINT
# ============================================

if __name__ == "__main__":
    print("🃏 Welcome to The Secret Poker Den of Yangon!")
    print("🚧 Game is under development...")
    show_yangon_intro()
    
