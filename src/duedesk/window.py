
import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import webbrowser


root_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '../..'))
inventory = []
desk = []
trash_pos = QRect()

@pyqtSlot()
def start_task():
    print("hello")   

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

    def drawMenu(self):
        self.menu_widget = menuScreen(self)
        self.setCentralWidget(self.menu_widget)

    def drawTable(self):
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

class menuScreen(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.setAutoFillBackground(True)
        p = self.palette()
        color = QColor().fromRgb(qRgb(210, 180, 140))
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)

        img_path = root_dir + "\\resources\\title.png" 
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

    def enterDesk(self, parent):
        self.close()
        parent.drawTable()

    def help(self):
        webbrowser.open('https://github.com/CEN3031-G33/due-desk') 

class MyTableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.__initTable__()
        self.__initInventoryList__()
        self.__initTaskList__()
        self.__initDragButtons__()

    def __initTable__(self):
        img_path = root_dir + "\\resources\desk.png" 
        
        c_pixmap = QPixmap(img_path)
        c = QLabel(self)
        screen = QApplication.primaryScreen()
        c.resize(int(screen.size().width() * 0.8), int(screen.size().height() * 0.8))        
        c_scaledPixmap = c_pixmap.scaled(int(screen.size().width() * 0.8), int(screen.size().height() * 0.8), Qt.KeepAspectRatio, Qt.FastTransformation)        
        c.setPixmap(c_scaledPixmap)        
        c.setScaledContents(True)

        paint_path = root_dir + "\\resources\\paint-bucket.png"
        paint_icon = QIcon(paint_path)
        paint = QPushButton(self)
        paint.setIcon(paint_icon)
        paint.setIconSize(QSize(int(screen.size().width() * 0.05), int(screen.size().height() * 0.05)))
        paint.move(int(screen.size().width() * 0.75), 10)
        paint.clicked.connect(self.setColor)
        paint.setStyleSheet("border: none;")

        exit_button = QPushButton(self)
        exit_button.setText("Exit")
        exit_button.clicked.connect(self.exitDesk)

        trash_path = root_dir + "\\resources\\trash.png"
        trash_widget = QLabel(self)
        trash_widget_pixmap = QPixmap(trash_path)
        trash_widget.resize(int(screen.size().width() * 0.15), int(screen.size().height() * 0.15))
        trash_widget.setPixmap(trash_widget_pixmap.scaled(int(screen.size().width() * 0.15), int(screen.size().height() * 0.15), Qt.KeepAspectRatio, Qt.FastTransformation))
        trash_widget.move(0, int(screen.size().height() * 0.65))

        trash_pos = trash_widget.geometry()

    def __initDeskLayout__():
        foo = 1

# vvvv drag and drop vvvv

    def __initDragButtons__(self):
        # needed to allow drops on application window
        self.setAcceptDrops(True)

        for i in range(len(desk)):
            btn = Button(self)
        #self.button = Button(self)
        #self.button.move(50,50)

        #### drag and drop events ####

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        screen = QApplication.primaryScreen()
        position = event.pos()
        trash_size = QSize(int(screen.size().width() * 0.15), int(screen.size().height() * 0.15))
        trash_point = QPoint(0, int(screen.size().height() * 0.65) )
        trash_rect = QRect(trash_point, trash_size)
        if (trash_rect.contains(position)):
            desk.remove(event.source())
            event.source().deleteLater()
            return
        event.source().move(position)
        event.accept()
            

# ^^^^ drag and drop ^^^^

    def displayButtons(self):
        for i in range(len(desk)):
            desk[i].show()

    def createButton(self):
        desk.append(Button(self))
        self.displayButtons()

    def __initInventoryList__(self):
        screen = QApplication.primaryScreen()
        inv_list = QWidget(self)
        inv_list.resize(int(screen.size().width() * 0.8), int(screen.size().height() * 0.2))
        inv_list.move(0, int(screen.size().height() * 0.8))

        hbox = QHBoxLayout()
        group_box = QGroupBox("Inventory")
        group_box.setStyleSheet("text-align: center; font-size: 20px; font-family: Helevetica;")

        for i in range (0,50):
            item = QPushButton()
            item_pixmap = QIcon(root_dir + "\\resources\lamp.png")
            item.setIcon(item_pixmap)
            item.setIconSize(QSize(int(screen.size().width() * 0.1), int(screen.size().height() * 0.1)))
            item.clicked.connect(self.createButton)
            inventory.append(item)
            hbox.addWidget(inventory[i])

        group_box.setLayout(hbox)
        title = "Inventory (" + str(len(inventory)) + ")"
        group_box.setTitle(title)

        scroll = QScrollArea()
        scroll.setWidget(group_box)
        scroll.setWidgetResizable(True)

        layout = QVBoxLayout()
        layout.addWidget(scroll)

        inv_list.setLayout(layout)

    def __initTaskList__(self):
        screen = QApplication.primaryScreen()
        task_list = QWidget(self)
        task_list.resize(int(screen.size().width() * 0.2), int(screen.size().height()))
        task_list.move(int(screen.size().width() * 0.8), 0)

        form_layout = QFormLayout()
        group_box = QGroupBox("My Tasks")
        group_box.setStyleSheet("text-align: center; font-size: 20px; font-family: Helevetica;")

        tasks = []
        task_buttons = []
        for i in range (0,50):
            label = QLabel("Task - this one is long and should take 2 lines")
            tasks.append(label)
            button = QPushButton("Start")
            #button.clicked.connect(self.buttonClicked)
            task_buttons.append(button)
            form_layout.addRow(tasks[i], task_buttons[i])

        group_box.setLayout(form_layout)
        title = "My Tasks (" + str(len(tasks)) + ")"
        group_box.setTitle(title)
        scroll = QScrollArea()
        scroll.setWidget(group_box)
        scroll.setWidgetResizable(True)

        layout = QVBoxLayout()
        layout.addWidget(scroll)

        task_list.setLayout(layout)

    def setColor(self):
        self.setAutoFillBackground(True)
        p = self.palette()
        color = QColorDialog.getColor()
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)

    def exitDesk(self):
        self.close()
        QApplication.quit()

class Button(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)
        screen = QApplication.primaryScreen()
        QButton_icon = QIcon(root_dir + "\\resources\lamp.png")
        self.setIcon(QButton_icon)
        self.setIconSize(QSize(int(screen.size().width() * 0.1), int(screen.size().height() * 0.1)))
        self.setStyleSheet("border: none;")
        self.resize(QSize(int(screen.size().width() * 0.1), int(screen.size().height() * 0.1)))
        self.move(int(screen.size().width() * 0.8 - self.width()), int(screen.size().height() * 0.8 - self.height()))

    def mouseMoveEvent(self, event):
        # if left mouse button is clicked 
        if event.buttons() == Qt.LeftButton:
            
            # create a mime object
            mimeData = QMimeData()
            
            # create a qdrag object
            drag = QDrag(self)

            # set mime object as the drag mime data 
            drag.setMimeData(mimeData)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)

            # give drag the mouse transformation 
            dropAction = drag.exec_(Qt.MoveAction)