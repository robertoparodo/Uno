from input_players import PlayerInputApp
from player import Player, Desk
from gui import Gui

if __name__ == '__main__':
    #app = PlayerInputApp()
    #players_list = [Player(p.capitalize()) for p in app.player_names]
    players_list = [Player("roberto"), Player("alessia")]
    banco = Desk(players_list)
    new_color = "empty"
    count_draw = 0
    while True:
        index_player = banco.player_turn
        gui = Gui(banco, new_color, count_draw)
        new_color = gui.new_color
        count_draw = gui.count_draw_card
        if len(banco.players[index_player].cards_in_hand) == 0:
            print("Ha vinto il giocatore", banco.players[index_player].name)
            break
