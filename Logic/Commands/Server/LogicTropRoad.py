from database.DataBase import DataBase
from Utils.Writer import Writer


class LogicTropRoad(Writer):

    def __init__(self, client, player, boxid=10, ammo=0, who=0, brawler=0):
        super().__init__(client)
        self.id = 24111
        self.player = player
        self.boxid = boxid
        self.ammo = ammo
        self.who = who
        self.brawler = brawler

    def encode(self):
    	LoginFailedMessage(self.client, self.player, "Вы забанены! [code: 0001]\nreason: петух!").send()