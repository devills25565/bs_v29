from database.DataBase import DataBase
from Utils.Reader import BSMessageReader
from Server.Login.LoginFailedMessage import LoginFailedMessage

class LogicSetPlayerNameColorCommand(BSMessageReader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
        self.read_Vint()
        self.read_Vint()
        self.read_Vint()
        self.read_Vint()
        self.read_Vint()
        self.name_color = self.read_Vint()


    def process(self):
        DataBase.replaceValue(self, 'name_color', self.name_color)