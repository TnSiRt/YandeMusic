from kivymd.app import MDApp

class PlayListManager():
    def __init__(self):
        self.treacks = []
        self.index = 0
        self.app = MDApp.get_running_app()
    
    def getTitleByCurrentIndex(self):
        return self.treacks[self.index]['title']

    def getArtistByCurrentIndex(self):
        return self.treacks[self.index]['artist']

    def getFileByCurrentIndex(self):
        return self.treacks[self.index]['fileDownload']

    def getDurationByCurrentIndex(self):
        return self.treacks[self.index]['duration']
    
    def getImageByCurrentIndex(self):
        return f'http://{self.treacks[self.index]['image'].replace("%%",'100x100')}'

    def next(self):
        self.index += 1
        self.app.audioDriver.set_pos(0.0)
        return {
            "title":self.getTitleByCurrentIndex(),
            "artist":self.getArtistByCurrentIndex(),
            "duration":self.getDurationByCurrentIndex(),
            "image":self.getImageByCurrentIndex(),
            'file':self.getFileByCurrentIndex()
        }

    def prev(self):
        self.index -= 1
        return {
            "title":self.getTitleByCurrentIndex(),
            "artist":self.getArtistByCurrentIndex(),
            "duration":self.getDurationByCurrentIndex(),
            "image":self.getImageByCurrentIndex(),
            'file':self.getFileByCurrentIndex()
        }
    
    def load(self, data):
        self.treacks = data
    
    def getAllInfoByCurrentIndex(self):
        return {
            "title":self.getTitleByCurrentIndex(),
            "artist":self.getArtistByCurrentIndex(),
            "duration":self.getDurationByCurrentIndex(),
            "image":self.getImageByCurrentIndex(),
            'file':self.getFileByCurrentIndex()
        }
    
    def setIndex(self, index:int):
        self.index = index