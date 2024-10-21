import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import time
import tkinter as tk
from tkinter import Tk, Button
from PIL import Image, ImageTk
from master_mind import play, select_colors 
from colors import Colors  
from status import Status  
from match import Match 


class MasterMindGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MasterMind Game")

        self.root.geometry("1200x1000")  

        self.combination = select_colors(time.time())  
        self.tries = 0
        self.max_attempts = 20
        self.selected_colors = []
        self.color_buttons = []  

        self.canvas = tk.Canvas(root, bg="lightblue")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.scrollable_frame = tk.Frame(self.canvas, bg="lightblue")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.create_color_buttons()

        self.create_control_buttons()

        self.message_label = tk.Label(self.scrollable_frame, text="", font=("Arial", 14), bg="lightblue")
        self.message_label.grid(row=3, column=0, columnspan=2, pady=10)

        self.guess_frame = tk.Frame(self.scrollable_frame, bg="lightblue")
        self.guess_frame.grid(row=4, column=0, padx=(10, 5), pady=20, sticky="e")
        self.guess_slots = self.create_guess_slots()

        self.feedback_frame = tk.Frame(self.scrollable_frame, bg="lightblue")
        self.feedback_frame.grid(row=4, column=1, padx=(5, 10), pady=20, sticky="w")
        self.feedback_slots = self.create_feedback_slots()

    def create_color_buttons(self):
        color_frame = tk.Frame(self.scrollable_frame,bg='lightblue') 
        color_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        for color in Colors:
            img = Image.new('RGB', (100, 50), color=color.value) 
            img_tk = ImageTk.PhotoImage(img) 

            color_button_frame = tk.Frame(color_frame,bg='lightblue')
            color_button_frame.pack(side=tk.LEFT, padx=5, pady=5)

            button = tk.Button(
                color_button_frame,
                image=img_tk, 
                width=100, height=50,
                relief=tk.RAISED,
                command=lambda col=color: self.select_color(col)
            )
            button.image = img_tk  
            button.pack()  

            label = tk.Label(color_button_frame, text=color.value, font=("Arial", 12, "bold"),bg='lightblue')
            label.pack() 

            self.color_buttons.append(button)

    def create_guess_slots(self):
        slots = []
        for row in range(self.max_attempts):
            row_guess = []
            for i in range(6):  
                slot = tk.Label(self.guess_frame, width=4, height=2, bg="white", relief=tk.SUNKEN)  
                slot.grid(row=row, column=i, padx=2, pady=2)  
                row_guess.append(slot)
            slots.append(row_guess)
        return slots

    def create_feedback_slots(self):
        feedback = []
        for row in range(self.max_attempts):
            row_feedback = []
            for i in range(6):  
                slot = tk.Label(self.feedback_frame, width=4, height=2, bg="gray", relief=tk.SUNKEN)  
                slot.grid(row=row, column=i, padx=2, pady=2)  
                row_feedback.append(slot)
            feedback.append(row_feedback)
        return feedback

    def update_guess_display(self):
        current_row = self.tries
        for i, color in enumerate(self.selected_colors):
            self.guess_slots[current_row][i].config(bg=color.value)

    def update_feedback_display(self, response):
        feedback = []
        for match, count in response.items():
            feedback.extend([match] * count)

        current_row = self.tries
        for i in range(len(feedback)):
            match_type = feedback[i]
            color = "black" if match_type == Match.EXACT else "silver" if match_type == Match.PARTIAL else "gray"
            self.feedback_slots[current_row - 1][i].config(bg=color)
        self.selected_colors = []  

    def select_color(self, color):
        if len(self.selected_colors) < 6:
            self.selected_colors.append(color)
            self.update_guess_display()
            self.update_color_buttons(color)
        elif len(self.selected_colors) == 6:
            self.message_label.config(text="Please submit your guess.", fg="red")
        else:
            self.message_label.config(text="Please choose 6 colors.", fg="red")

    def update_color_buttons(self, color):
        for button in self.color_buttons:
            if button.cget("text") == color.value:
                button.config(bg=color.value)  

    def submit_guess(self):
        if len(self.selected_colors) != 6:
            self.message_label.config(text="Please select 6 colors.", fg="red")
            return

        response, self.tries, status = play(self.combination, self.selected_colors, self.tries)
        self.update_feedback_display(response)
        self.check_status(status)

    def reset_game(self):
        self.combination = select_colors(time.time())
        self.tries = 0
        self.guess_slots = self.create_guess_slots()
        self.feedback_slots = self.create_feedback_slots()
        self.selected_colors = []
        self.reset_color_buttons()
        self.message_label.config(text="")  

    def reset_color_buttons(self):
        for button in self.color_buttons:
            button.config(bg=button.cget("bg"))  

    def give_up(self):
        self.message_label.config(text=f"You gave up! The correct combination was: {', '.join([color.value for color in self.combination])}", fg="blue")

    def check_status(self, status):
        if status == Status.WON:
            self.won_output()
        elif status == Status.LOST:
            self.reset_game()
            self.lost_output()
        elif self.tries >= self.max_attempts:
            self.reset_game()
            self.lost_output()
            
            

    def won_output(self):
        self.message_label.config(text=f"Congratulations! You won! The correct combination was: {', '.join([color.value for color in self.combination])}", fg="green")

    def lost_output(self):
        self.message_label.config(text=f"You lost! The correct combination was: {', '.join([color.value for color in self.combination])}", fg="red")


    def used_all_tries_output(self):
        self.message_label.config(text=f"You've used all {self.max_attempts} tries! The correct combination was: {', '.join([color.value for color in self.combination])}", fg="red")

    def create_control_buttons(self):
        button_frame = tk.Frame(self.scrollable_frame, bg='lightblue')
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        submit_button = tk.Button(button_frame, text="Submit Guess", command=self.submit_guess)
        submit_button.grid(row=0, column=0, padx=10)

        reset_button = tk.Button(button_frame, text="Restart Game", command=self.reset_game)
        reset_button.grid(row=0, column=1, padx=10)

        give_up_button = tk.Button(button_frame, text="Give Up", command=self.give_up)
        give_up_button.grid(row=0, column=2, padx=10)


if __name__ == "__main__":
    root = tk.Tk()
    gui = MasterMindGUI(root)
    root.mainloop()