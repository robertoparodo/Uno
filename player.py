import random
from card import Deck, Card

class Player(object):
    def __init__(self, name: str):
        self.name = name
        self.cards_in_hand = []
        self.flag_one = False

    def add_card(self, card: Card):
        self.cards_in_hand.append(card)

    def play_card(self, card: Card):
        self.cards_in_hand.remove(card)

    def said_one(self):
        self.flag_one = True

    def check_seed(self, seed: str):
        for card in self.cards_in_hand:
            if card.get_item["Seed"] == seed:
                return True
        return False

    def check_color(self, color: str):
        for card in self.cards_in_hand:
            if card.get_item["Color"] == color:
                return True
        return False

    def two_card(self) -> bool:
        return len(self.cards_in_hand) == 2


class Desk(object):
    def __init__(self, players: list[Player]):
        self.players, self.deck = players, Deck()
        self.last_card = None
        self.start()
        self.player_turn = random.randint(0, len(players)-1)
        self.turn_direction = "clockwise"

    def start(self):
        count = 0
        while count < self.deck.startingHandSize:
            for player in self.players:
                player.add_card(self.deck.draws_a_card())
            count += 1
        aus = []
        self.last_card = self.deck.draws_a_card()
        while self.last_card.get_item['Category'] == "Action" or self.last_card.get_item['Category'] == "Jolly":
            aus.append(self.last_card)
            self.last_card = self.deck.draws_a_card()
        self.deck.add_card_played(self.last_card)
        self.deck.deck.extend(aus)
        aus.clear()

    def update_turn(self):
        if self.turn_direction == "clockwise":
            self.player_turn += 1
            if self.player_turn > len(self.players)-1:
                self.player_turn = 0
        else:
            self.player_turn -= 1
            if self.player_turn < 0:
                self.player_turn = len(self.players)-1

    def play(self, card: Card):
        self.players[self.player_turn].play_card(card)
        self.deck.add_card_played(card)
        self.last_card = card
        self.update_turn()

    def draw_x_cards(self, number: int):
        for i in range(number):
            self.players[self.player_turn].add_card(self.deck.draws_a_card())

    def reverse_turn(self):
        self.turn_direction = "anticlockwise" if self.turn_direction == "clockwise" else "clockwise"
        if len(self.players) == 2:
            self.stop_player()
        else:
            self.update_turn()
            self.update_turn()

    def stop_player(self):
        self.update_turn()