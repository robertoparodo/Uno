from tkinter import messagebox
from player import Desk
from card import Card
import tkinter as tk
from PIL import Image, ImageTk

class Gui(object):
    def __init__(self, desk: Desk, new_color: str, count_draw_card: int):
        self.desk = desk
        self.root = tk.Tk()
        self.new_color = new_color
        self.count_draw_card = count_draw_card
        self.said_one = False

        self.root.title(f"Turno giocatore: {self.desk.players[self.desk.player_turn].name}")
        self.root.geometry("1000x600")

        self.upper_frame = tk.Frame(self.root, width=1000, height=400, relief="ridge", bd=2, bg="lightgreen")
        self.upper_frame.pack(side="top", fill="x")
        self.upper_frame.pack_propagate(False)

        self.upper_frame_card = tk.Frame(self.upper_frame, width=500, height=400, relief="ridge", bd=2, bg="lightgreen")
        self.upper_frame_card.pack(side="left", fill="x")
        self.upper_frame.pack_propagate(False)

        self.upper_frame_color = tk.Frame(self.upper_frame, width=500, height=400, relief="ridge", bd=2, bg="lightgreen")
        self.upper_frame_color.pack(side="right", fill="x")
        self.upper_frame_color.pack_propagate(False)

        self.lower_frame = tk.Frame(self.root, width=1000, height=200, relief="ridge", bd=2, bg="lightgray")
        self.lower_frame.pack(side="bottom", fill="x")
        self.lower_frame.pack_propagate(False)

        self.canvas = tk.Canvas(self.lower_frame, width=1000, height=140, bg="lightgray", bd=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="x", expand=True)
        self.h_scrollbar = tk.Scrollbar(self.lower_frame, orient="horizontal", command=self.canvas.xview)
        self.h_scrollbar.pack(side="top", fill="x")
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set)
        self.cards_frame = tk.Frame(self.canvas, bg="lightgray")
        self.canvas.create_window((0, 0), window=self.cards_frame, anchor="nw")
        self.cards_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.bind_all("<Shift-MouseWheel>", lambda e: self.canvas.xview_scroll(int(-1 * (e.delta / 120)), "units"))

        self.button_frame = tk.Frame(self.lower_frame, width=1000, height=60, relief="ridge", bd=2, bg="lightgray")
        self.button_frame.pack(side="bottom", fill="x")
        self.button_frame.pack_propagate(False)

        self.inner_button_frame = tk.Frame(self.button_frame)
        self.inner_button_frame.pack(expand=True)

        self.button_next = tk.Button(self.inner_button_frame, text="Passa", command=self.next)
        self.button_next.pack(side="left", padx=10)
        self.button_next.config(state="disabled")

        self.button_one = tk.Button(self.inner_button_frame, text="Uno", command=self.one)
        self.button_one.pack(side="left", padx=10)
        if self.desk.players[self.desk.player_turn].one_card():
            self.button_one.config(state="active")
        else:
            self.button_one.config(state="disabled")

        self.__print_last_card()
        self.__print_retro_card()
        self.__print_cards()

        self.color_label = tk.Label(self.upper_frame_color,
                                    text=self.desk.last_card.get_item['Color'],
                                    fg=self.desk.last_card.get_item['Color'],
                                    font=("Helvetica", 16, "bold"))
        if self.new_color != "empty":
            self.color_label = tk.Label(self.upper_frame_color,
                                        text=self.new_color,
                                        fg=self.new_color,
                                        font=("Helvetica", 16, "bold"))
        self.color_label.pack(pady=10, expand=True)

        self.root.mainloop()

    def next(self):
        self.desk.update_turn()
        self.root.destroy()

    def one(self):
        self.said_one = True
        self.button_one.config(state="disabled")

    def __print_retro_card(self):
        img_path = "cards/retro.png"
        pil_image = Image.open(img_path).resize((80, 80))
        self.card_image = ImageTk.PhotoImage(pil_image)
        self.card_button_draw = tk.Button(
            self.upper_frame_card,
            image=self.card_image,
            command=self.draws_a_card
        )
        self.card_button_draw.pack(side="left", padx=5)

    def draws_a_card(self):
        self.card_button_draw.config(state="disabled")
        self.button_next.config(state="active")
        card = self.desk.deck.draws_a_card()
        self.desk.players[self.desk.player_turn].add_card(card)

        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        self.__print_cards()

    def __print_last_card(self):
        img_path = self.desk.last_card.get_item["Path"]
        card_img = Image.open(img_path)
        card_img = card_img.resize((80, 80))
        card_tk = ImageTk.PhotoImage(card_img)
        label_card = tk.Label(self.upper_frame_card, image=card_tk, bg="white")
        label_card.image = card_tk
        label_card.pack(side="left", padx=5)

    def __print_cards(self):
        drew_card_4 = False
        drew_card_2 = False
        have_another_4 = False
        have_another_2_4 = False
        if self.desk.last_card.get_item["Category"] == "Jolly" and self.desk.last_card.get_item["Seed"] == "+4":
            self.count_draw_card += 4
            if not self.desk.players[self.desk.player_turn].check_jolly_draw("+4"):
                messagebox.showinfo(title="", message=f"Hai pescato {self.count_draw_card} carte")
                self.desk.draw_x_cards(self.count_draw_card)
                drew_card_4 = True
            else:
                have_another_4 = True

        if self.desk.last_card.get_item["Seed"] == "+2":
            self.count_draw_card += 2
            if not (self.desk.players[self.desk.player_turn].check_jolly_draw("+2") or self.desk.players[self.desk.player_turn].check_jolly_draw("+4")):
                messagebox.showinfo(title="", message=f"Hai pescato {self.count_draw_card} carte")
                self.desk.draw_x_cards(self.count_draw_card)
                drew_card_2 = True
            else:
                have_another_2_4 = True

        self.card_images = []
        self.card_buttons = []

        self.position_card_draw_four = []
        self.position_card_draw_two = []
        index=0
        for card in self.desk.players[self.desk.player_turn].cards_in_hand:
            if card.get_item["Color"] == "Black" and card.get_item["Seed"] == "+4":
                self.position_card_draw_four.append(index)
            elif card.get_item["Seed"] == "+2":
                self.position_card_draw_two.append(index)
            img_path = card.get_item["Path"]
            pil_image = Image.open(img_path).resize((80, 80))
            card_image = ImageTk.PhotoImage(pil_image)
            self.card_images.append(card_image)
            card_button = tk.Button(
                self.cards_frame,
                image=card_image,
                command=lambda c=card: self.play_card(c)
            )
            self.card_buttons.append(card_button)
            card_button.pack(side="left", padx=5)
            index += 1

        if drew_card_4:
            self.card_button_draw.config(state="disabled")
            for btn in self.card_buttons:
                btn.config(state="disabled")
            self.desk.last_card = Card("-1", self.new_color, "Jolly", 50, "cards/draw4.png")
            self.button_next.config(state="active")
            self.count_draw_card = 0
        elif have_another_4:
            messagebox.showinfo(title="", message="Rispondi al +4 con il tuo +4")
            self.card_button_draw.config(state="disabled")
            counter = 0
            for btn in self.card_buttons:
                if counter not in self.position_card_draw_four:
                    btn.config(state="disabled")
                counter += 1
        elif drew_card_2:
            self.card_button_draw.config(state="disabled")
            for btn in self.card_buttons:
                btn.config(state="disabled")
            self.desk.last_card = Card("-1", self.desk.last_card.get_item["Color"], self.desk.last_card.get_item["Category"], self.desk.last_card.get_item["Value"], self.desk.last_card.get_item["Path"])
            self.button_next.config(state="active")
            self.count_draw_card = 0
        elif have_another_2_4:
            messagebox.showinfo(title="", message="Rispondi al +2 con il tuo +4 o +2")
            self.card_button_draw.config(state="disabled")
            counter = 0
            self.position_card_draw_four.extend(self.position_card_draw_two)
            for btn in self.card_buttons:
                if counter not in self.position_card_draw_four:
                    btn.config(state="disabled")
                counter += 1

    def action_change_color(self):
        popup = tk.Toplevel(self.root)
        popup.title("Scegli un colore")
        choise = tk.StringVar(value="")
        color = [("Giallo", "Yellow"), ("Blu", "Blue"), ("Rosso", "Red"), ("Verde", "Green")]
        tk.Label(popup, text="Seleziona un colore:").pack(pady=10)
        for name, value in color:
            tk.Radiobutton(popup, text=name, variable=choise, value=value).pack(anchor="w")

        def confirm():
            if choise.get():
                self.new_color = choise.get()
                popup.destroy()
            else:
                messagebox.showwarning("Attenzione", "Seleziona un colore prima di confermare!")

        tk.Button(popup, text="Conferma", command=confirm).pack(pady=10)
        popup.transient(self.root)
        popup.grab_set()
        self.root.wait_window(popup)

    def play_card(self, card: Card):
        if card.get_item["Category"] == "Jolly":
            self.check_one(card)
            self.desk.play(card)
            self.action_change_color()
            self.root.destroy()
        elif self.new_color in ["Red", "Blue", "Green", "Yellow"]:
            if card.get_item["Seed"] == "Stop" and self.new_color == card.get_item["Color"]:
                self.check_one(card)
                self.desk.play(card)
                self.desk.stop_player()
                self.root.destroy()
            elif card.get_item["Seed"] == "Reverse" and self.new_color == card.get_item["Color"]:
                self.check_one(card)
                self.desk.play(card)
                self.desk.reverse_turn()
                self.root.destroy()
            elif self.new_color == card.get_item["Color"]:
                self.check_one(card)
                self.desk.play(card)
                self.new_color = "empty"
                self.root.destroy()
        elif card.get_item["Seed"] == self.desk.last_card.get_item["Seed"] or card.get_item["Color"] == self.desk.last_card.get_item["Color"]:
            if card.get_item["Seed"] == "Stop":
                self.check_one(card)
                self.desk.play(card)
                self.desk.stop_player()
                self.root.destroy()
            elif card.get_item["Seed"] == "Reverse":
                self.check_one(card)
                self.desk.play(card)
                self.desk.reverse_turn()
                self.root.destroy()
            else:
                self.check_one(card)
                self.desk.play(card)
                self.root.destroy()
        elif card.get_item["Seed"] == "+2" and self.desk.last_card.get_item["Seed"] == "-1":
            self.desk.play(card)
            self.check_one(card)
            self.root.destroy()

    def check_one(self, card: Card):
        if self.desk.players[self.desk.player_turn].one_card():
            if not self.said_one:
                messagebox.showinfo(title="", message=f"Non hai detto UNO, peschi 2 carte")
                self.desk.draw_x_cards(2)
            elif card.get_item["Seed"] in ["+2", "+4" , "Stop", "Reverse", "ChangeColor"]:
                messagebox.showinfo(title="", message=f"Non puoi chiudere con una carta speciale")
                self.draws_a_card()
