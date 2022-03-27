# ------------------------------------------------------------------------------
# Project  : DueDesk
# Module   : TaskGui
# Abstract : 
#   A TaskGui is composed of gui related materials and the business logic for
#   a `Task`.
# ------------------------------------------------------------------------------
import unittest
from .task import Task
from .deadline import Deadline
from PyQt5.QtWidgets import *

class TaskGui(QWidget):
    def __init__(self, root: QMainWindow):
        '''Creates a `TaskGui' instance.'''
        super(QWidget, self).__init__(root)
        self._task = Task("sample", Deadline.from_str("2022-01-01"))
        # configure the task's gui label
        self._label = QLabel(self._task.get_subject())
        self._deadline_label = QLabel("Due: "+str(self._task.get_deadline()))
        # configure the task's 'is complete' checkbox
        self._status_box = QCheckBox("")
        self._status_box.setChecked(self._task.is_complete())
        # configure the task's gui button
        self._begin_btn = QPushButton("Start")
        self._begin_btn.clicked.connect(self.begin_task)
        pass


    def glue_to_gui(self, layout: QFormLayout):
        '''Adds the appropriate gui elements for this task to the gui.'''
        sublay = QFormLayout()
        sublay.addRow(self._begin_btn, self._status_box)
        layout.addRow(self._label)
        layout.addRow(self._deadline_label, sublay)
        layout.addRow(QLabel('-'*30))
        pass


    def load(self, data: dict):
        '''Loads `Task` attributes from a dictionary into existing instance.'''
        self._task = Task.from_dict(data)
        # update gui elements
        self._label.setText(self._task.get_subject())
        self._deadline_label.setText("Due: "+str(self._task.get_deadline()))
        self._status_box.setChecked(self._task.is_complete())
        pass


    def save(self) -> dict:
        '''Saves `Task` attributes to a dictionary.'''
        self._task.to_dict()


    def get_task(self) -> Task:
        return self._task


    # method bound to clicking 'start' button for `TaskGui` object
    def begin_task(self):
        print('info: entering zen mode for task', self._task.get_subject())
        pass
    pass


class TestTaskGui(unittest.TestCase):
    pass