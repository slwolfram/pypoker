from player import Player
from table import Table
from game import Game
import asyncio

players = []

for i in range(1, 7):
    players.append(Player(i, "Player " + i, 10000))

table = Table(0, "Heads Up", 6, 10000, 20000, 100, 200)
game = Game(0, table, players)
game.play()