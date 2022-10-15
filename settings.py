import os
settingsPath = os.path.join(os.path.dirname(__file__), 'settings')

class Settings():
    def __init__(self,guildID):
        self.guild = guildID
        self.settings = self.getSettings()

    def setSettings(self,settings):
        with open(os.path.join(settingsPath, str(self.guild) + ".json"), 'w') as f:
            json.dump(settings, f, indent=4)

    def getSettings(self):
        with open(os.path.join(settingsPath, str(self.guild) + ".json"), 'r') as f:
            settings = json.load(f)
        return settings

    def setVoteGap(self,count):
        self.settings["voteGap"] = count
        self.setSettings(self.settings)
    
    def getVoteGap(self):
        return self.settings["voteGap"]
    
    def setBotChannel(self,channel):
        self.settings["botChannel"] = channel
        self.setSettings(self.settings)
    
    def getBotChannel(self):
        return self.settings["botChannel"]