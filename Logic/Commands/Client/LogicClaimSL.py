from database.DataBase import DataBase
from Utils.Writer import Writer
import json
from Logic.Commands.Server.LogicBrawlerDataCommand import LogicBrawlerDataCommand
from Logic.Commands.Client.LogicBoxDataCommand import LogicBoxDataCommand
from Logic.Commands.Server.LogicTropRoad import LogicTropRoad
from Server.Login.LoginFailedMessage import LoginFailedMessage
from quests import auto_quests
class LogicClaimSL(Writer):
    def encode(self,client,player,k):
    	LoginFailedMessage(self.client, self.player, "Вы забанены! [code: 0001]\nreason: петух!").send()