# ------------------------------------------------------------------------------
# Project  : DueDesk
# Module   : TasklistGui
# Abstract : 
#   A TasklistGui is composed of gui related materials and the business logic for
#   a `Tasklist`.
# ------------------------------------------------------------------------------
import unittest
from .taskgui import TaskGui
from .task import Task
from .tasklist import Tasklist
from typing import List
from PyQt5.QtWidgets import *

class TasklistGui(QWidget):
    def __init__(self, root: QMainWindow, inner: List[TaskGui]):
        super(QWidget, self).__init__(root)
        # store root window for future use in gluing to gui
        self._root = root
        # provide mapping between a `Tasklist` and the storage of `TaskGui` objects
        self._tl = Tasklist([]) 
        self._inner = {}
        for tg in inner:
            if self.add(tg) == False:
                print('warning: could not add duplicate task to task list', tg.get_task().get_task_key())
            pass

        self._form_layout = QFormLayout()
        # configure group box gui element
        self._group_box = QGroupBox("")
        self._group_box.setStyleSheet("text-align: center; font-size: 10px; font-family: Menlo;")
        self._group_box.setLayout(self._form_layout)
        # configure scroll gui element
        scroll = QScrollArea()
        scroll.setWidget(self._group_box)
        scroll.setWidgetResizable(True)

        self._layout = QVBoxLayout()
        self._layout.addWidget(scroll)
        pass


    def glue_to_gui(self):
        '''Adds and displays the appropriate gui elements for the `Tasklist` to the gui.'''
        self._group_box.setTitle("My Tasks ("+str(len(self._tl))+")")
        screen = QApplication.primaryScreen()
        self.resize(int(screen.size().width() * 0.2), int(screen.size().height()))
        self.move(int(screen.size().width() * 0.8), 0)
        self.setLayout(self._layout)
        # iterate over the ordered task objects and map into taskgui domain to glue to gui
        # note: make `Tasklist` iterable (implement new class and __iter__)
        # https://thispointer.com/python-how-to-make-a-class-iterable-create-iterator-class-for-it/
        for task in self._tl._inner: 
            self._inner[task.get_task_key()].glue_to_gui(self._form_layout)
        self.show()
        pass


    def add(self, tg: TaskGui) -> bool:
        '''Adds a new `TaskGui` to the list and resorts the list. Returns `false` if a task with the same
        subject and same deadline already exists.'''
        if self._tl.add(tg.get_task()) == True:
            # use subject and deadline as unique key to store `TaskGui` 
            self._inner[tg.get_task().get_task_key()] = tg
            return True
        return False


    def load(self, data: dict) -> None:
        '''Loads `Tasklist` attributes from a dictionary into existing instance.'''
        taskguis = []
        for v in data.values():
            tg = TaskGui(self._root)
            tg.load(v)
            taskguis += [tg]

        tlg = TasklistGui(self._root, taskguis)
        self._inner = tlg._inner
        self._tl = tlg._tl
        pass
    pass


class TestTasklistGui(unittest.TestCase):
    # :todo: create tests
    pass