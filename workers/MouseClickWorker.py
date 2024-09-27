from PyQt5 import QtCore
from PyQt5.QtCore import QRect, QPoint
from pynput import mouse
import PIL
import pyscreenshot
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)
# Choose a Gemini API model.

class MouseClickWorker(QtCore.QObject):
    signalStatus = QtCore.pyqtSignal(str)
    coord = []
    rect = QRect()
    isActive = True
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        
    
    def on_click(self,x, y, button, pressed):
        point = QPoint(x, y)
        is_contained = self.rect.contains(point)
        if not is_contained and  self.isActive and pressed and button == mouse.Button.left:
            self.coord.append(x)
            self.coord.append(y)
            print(f"Position enregistrée : ({x, y, self.coord})")
            
       
    @QtCore.pyqtSlot()  
    def startMouseListening(self):
        print(f'start Listening ')
        self.isActive = True
        with mouse.Listener(on_click=self.on_click) as listener:
            listener.join()
    @QtCore.pyqtSlot()  
    def stopListener(self):
        self.isActive= False
        if(len(self.coord)>=6):
            pic = pyscreenshot.grab(bbox=(self.coord[-6], self.coord[-5], self.coord[-4], self.coord[-3]))
            pic.save("ss.png")
            sample_file_2 = PIL.Image.open('ss.png')
            self.signalStatus.emit('Calling gemini')
            response = self.model.generate_content(["determine all correct answers of the MCQ, ignore all incorrect answer",
								sample_file_2
								],
                                safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                })
            self.signalStatus.emit('response >: {}'.format(response.text))