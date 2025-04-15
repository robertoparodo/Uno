import random
import pandas as pd
from pandas import DataFrame


class Card(object):
    def __init__(self, seed, color, category, value, path):
        self.seed, self.color, self.category, self.value, self.path = seed, color, category, value, path

    @property
    def get_item(self) -> dict:
        return {'Seed': self.seed, 'Color': self.color, 'Category': self.category, 'Value': self.value, 'Path': self.path}


class Deck(object):
    def __init__(self):
        read_data: DataFrame = pd.read_csv("deck.csv")
        deck_partition1: list[Card] = [Card(card['Seed'], card['Color'], card['Category'], card['Value'], card['Path']) for card in read_data.to_dict('records')]
        deck_partition2: list[Card] = [Card(card['Seed'], card['Color'], card['Category'], card['Value'], card['Path']) for card in read_data.to_dict('records')]
        self.deck = []
        self.deck.extend(deck_partition1)
        self.deck.extend(deck_partition2)

        self.startingHandSize: int = 7
        self.cards_played = []
        self.__shuffle()

    @property
    def cards_number(self) -> int:
        return len(self.deck)

    def add_card_played(self, card: Card):
        self.cards_played.append(card)

    def __shuffle(self) -> None:
        random.shuffle(self.deck)

    def draws_a_card(self) -> Card:
        if len(self.deck) != 0:
            return self.deck.pop(len(self.deck)-1)
        else:
            self.deck = self.cards_played.copy()
            self.cards_played.clear()
            self.__shuffle()
            return self.draws_a_card()
