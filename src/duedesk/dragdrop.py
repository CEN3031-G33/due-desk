import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag

# QMimeData: 
# used to describe information that can be stored 
# in the clipboard and transfered via drag and drop 

class Button(QPushButton):
    def __init__(self, button_text, parent):
        super().__init__(button_text, parent)
        

    def mouseMoveEvent(self, event):
        # if left mouse button is clicked 
        if event.buttons() == Qt.LeftButton:
            
            # create a mime object
            mimeData = QMimeData()
            
            # create a qdrag object
            drag = QDrag(self)

            # set mime object as the drag mime data 
            drag.setMimeData(mimeData)

            # give drag the mouse transformation 
            dropAction = drag.exec_(Qt.MoveAction)


def savePosition(x,y):
            print(x,y)
#### application template ####
class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 400)

        # needed to allow drops on application window
        self.setAcceptDrops(True)

        self.button = Button('My Image', self)
        self.button.move(50,50)

    #### drag and drop events ####
    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        position = event.pos()
        self.button.move(position)
        #print(self.button.x(), self.button.y())
        savePosition(self.button.x(),self.button.y())
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = AppDemo()
    demo.show()
    sys.exit(app.exec_())