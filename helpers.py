class Playersonly:
    def formatName(self):
        names = self.name.split(" ")
        self.name = ""
        url = []
        for word in names:
            word = word.lower()
            url.append(word.lower())
            self.name += word.replace(word[0], word[0].upper()) + " "

        self.url = url[-1][:5] + url[0][:2]
        self.name = self.name[:-1]

