
import os, sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import webbrowser
from .desk import Desk

root_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '../..'))
root_dir = '.'
desk = []

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Due Deskdue'
        self.left = 0
        self.top = 0
        screen = QApplication.primaryScreen()
        self.width = screen.size().width()
        self.height = screen.size().height()
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.drawMenu()
        self.showFullScreen()
        #self.setFixedSize(self.layout.sizeHint())
        pass


    def drawMenu(self):
        self.menu_widget = menuScreen(self)
        self.setCentralWidget(self.menu_widget)
        pass


    def drawTable(self):
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        pass

    def drawZen(self):
        #this method will take the desk from table widget, resize it, and draw it, in addition to the current task, a back button, and starting a timer
        #disable drag and drop for items
        pass

class menuScreen(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.setAutoFillBackground(True)
        p = self.palette()
        color = QColor().fromRgb(qRgb(210, 180, 140))
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)

        img_path = root_dir + "/resources/title.png" 
        c_pixmap = QPixmap(img_path)
        c = QLabel(self)
        screen = QApplication.primaryScreen()
        c.resize(int(screen.size().width() * 0.3), int(screen.size().height() * 0.3))        
        c_scaledPixmap = c_pixmap.scaled(int(screen.size().width() * 0.4), int(screen.size().height() * 0.4), Qt.KeepAspectRatio, Qt.FastTransformation)        
        c.setPixmap(c_scaledPixmap)
        c.setScaledContents(True)
        c.move(int(screen.size().width()/2 - c.width()/2), int(screen.size().height()/2 - c.height()*1.2))

        start_button = QPushButton(self)
        start_button.setText("Start")
        start_button.move(int(screen.size().width()/2 - start_button.width() * 1.5), int(screen.size().height()/2))
        start_button.clicked.connect(lambda:self.enterDesk(parent))

        help_button = QPushButton(self)
        help_button.setText("Help")
        help_button.move(int(screen.size().width()/2), int(screen.size().height()/2))
        help_button.clicked.connect(self.help)
        pass

    def enterDesk(self, parent):
        self.close()
        parent.drawTable()
        return True


    def help(self):
        webbrowser.open('https://github.com/CEN3031-G33/due-desk')
        return 'https://github.com/CEN3031-G33/due-desk'


class MyTableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        # boot up the due desk!
        self._dd = Desk('./tests/data.json', parent)
        self._dd.load_from_file()

        self._parent = parent
        self.__initTable__()
        # allow drops on application window
        self.setAcceptDrops(True)
        pass

    
    def __initTable__(self):
        '''Initialize supportive gui elements around the desk.'''
        # desk background image
        img_path = root_dir + "/resources/emptydesk.png" 
        c_pixmap = QPixmap(img_path)
        c = QLabel(self)
        screen = QApplication.primaryScreen()
        c.resize(int(screen.size().width() * 0.8), int(screen.size().height() * 0.8))        
        c_scaledPixmap = c_pixmap.scaled(int(screen.size().width() * 0.8), int(screen.size().height() * 0.8), Qt.KeepAspectRatio, Qt.FastTransformation)        
        c.setPixmap(c_scaledPixmap)        
        c.setScaledContents(True)

        # background paint color
        paint_path = root_dir + "/resources/paint-bucket.png"
        paint_icon = QIcon(paint_path)
        paint = QPushButton(self)
        paint.setIcon(paint_icon)
        paint.setIconSize(QSize(int(screen.size().width() * 0.05), int(screen.size().height() * 0.05)))
        paint.move(int(screen.size().width() * 0.75), 10)
        paint.clicked.connect(self.setColor)
        paint.setStyleSheet("border: none;")

        # exit button
        exit_button = QPushButton(self)
        exit_button.setText("Exit")
        exit_button.clicked.connect(self.exitDesk)

        # trash can
        trash_path = root_dir + "/resources/trash.png"
        trash_widget = QLabel(self)
        trash_widget_pixmap = QPixmap(trash_path)
        trash_widget.resize(int(screen.size().width() * 0.15), int(screen.size().height() * 0.15))
        trash_widget.setPixmap(trash_widget_pixmap.scaled(int(screen.size().width() * 0.15), int(screen.size().height() * 0.15), Qt.KeepAspectRatio, Qt.FastTransformation))
        trash_widget.move(0, int(screen.size().height() * 0.65))
        pass


    def dragEnterEvent(self, event):
        event.accept()
        pass


    def dropEvent(self, event):
        screen = QApplication.primaryScreen()
        position = event.pos()
        trash_size = QSize(int(screen.size().width() * 0.15), int(screen.size().height() * 0.15))
        trash_point = QPoint(0, int(screen.size().height() * 0.65) )
        trash_rect = QRect(trash_point, trash_size)
        # check if contains trash can dimensions to remove it from the desk
        if(trash_rect.contains(position)):
            print("remove resourcegui object", event.source())
            event.source().tell_rg_to_remove()
            event.source().deleteLater()
        else:
            event.source().move(position)
            event.accept()
        pass


    def setColor(self):
        '''Change the main window's background color.'''
        self.setAutoFillBackground(True)
        p = self.palette()
        color = QColorDialog.getColor()
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)
        pass


    def exitDesk(self):
        '''Close the application and save the desk contents.'''
        self.close()
        self._dd.save_to_file()
        QApplication.quit()
        return True
    pass