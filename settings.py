import os
import json

settingsPath = os.path.join(os.path.dirname(__file__), 'settings')

class Settings():
    def __init__(self,guildID):
        self.guild = guildID
        self.settings = self.getSettings()

    def setSettings(self):
        with open(os.path.join(settingsPath, str(self.guild) + ".json"), 'w+'
        ) as f:
            json.dump(self.settings, f, indent=4)

    def getSettings(self):
        if os.path.exists(os.path.join(settingsPath, str(self.guild) + ".json")):
            with open(os.path.join(settingsPath, str(self.guild) + ".json"), 'r+') as f:
                self.settings = json.load(f)
            return self.settings
        else:
            return {"botChannel":None,"voteGap":4}

    def setVoteGap(self,count):
        self.settings["voteGap"] = count
        self.setSettings()
    
    def getVoteGap(self):
        return self.settings["voteGap"]
    
    def setBotChannel(self,channel):
        self.settings["botChannel"] = channel
        self.setSettings()
    
    def getBotChannel(self):
        return self.settings["botChannel"]