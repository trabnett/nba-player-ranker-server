import json
import os

class Playersonly:
    def formatName(self):
        names = self.name.split(" ")
        self.name = ""
        url = []
        for word in names:
            word = word.lower()
            url.append(word.lower())
            def changeChar(s, p, r):
                return s[:p]+r+s[p+1:]
            firstLetter = word[0].upper()
            self.name += changeChar(word, 0, firstLetter) + " "

        self.url = url[-1][:5] + url[0][:2]
        self.name = self.name[:-1]

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)



