from pygame import init
from pygame import mixer

import os
import logging

init()
mixer.init()

logging.basicConfig(
    level=logging.DEBUG,
    filename='audioDriver.log',  # ← вот это важно
    filemode='w',  # 'w' - перезаписывать, 'a' - дописывать
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class AudioDriver():
    def __init__(self):
        logging.debug('init audio driver')
        self.cashFile_path = os.path.join(os.path.dirname(__file__), "cashFile")
        self.muiscDriver = mixer.music
        
        self._isNewSong = True
        logging.debug('_isNewSong = True')

    def load(self, treack_name):
        self._isNewSong = True
        self.muiscDriver.load(f'{self.cashFile_path}/{treack_name}')
        logging.debug(f'load {self.cashFile_path}/{treack_name}')

    def pause(self):
        logging.debug('pasue audio')
        self.muiscDriver.pause()

    def unpauseOrPlay(self):
        if self._isNewSong == True:
            self.muiscDriver.play()
            logging.debug('start audio')
            self._isNewSong = False
        else:
            self.muiscDriver.unpause()
            logging.debug('unpause audio')
    
    def set_pos(self,pos:float):
        self.muiscDriver.set_pos(pos)
    