# ------------------------------------------------------------------------------
# Project  : DueDesk
# Module   : TaskGui
# Abstract : 
#   A TaskGui is composed of gui related materials and the business logic for
#   a `Task`.
# ------------------------------------------------------------------------------
from .task import Task
from .deadline import Deadline
from PyQt5.QtWidgets import *
from .taskrunner import Taskrunner

class TaskGui(QWidget):
    def __init__(self, root: QMainWindow):
        '''Creates a `TaskGui' instance.'''
        super(QWidget, self).__init__(root)
        self._task = Task("sample", Deadline.from_str("2022-01-01"))
        # configure the task's gui label
        self._label = QLabel(self._task.get_subject())
        self._deadline_label = QLabel("Due: "+str(self._task.get_deadline()))
        self._minutes_label = QLabel("Minutes Worked: " + str(round(self._task.get_minutes(),2)))
        # configure the task's 'is complete' checkbox
        self._status_box = QCheckBox("")
        self._status_box.setChecked(self._task.is_complete())
        # configure the task's gui button
        self._begin_btn = QPushButton("Start")
        self._begin_btn.clicked.connect(self.toggle_task)
        # internal instance variable to remember if we are currently the task with lock on timer
        self._is_running = False
        pass


    def track_runner(self, tr: Taskrunner):
        '''Remember the task runner.'''
        self._trunner = tr
        pass
    

    def glue_to_gui(self, layout: QFormLayout, row: int):
        '''Adds the appropriate gui elements for this task to the gui. TODO: create one widget that is glued to the gui'''

        sublay = QFormLayout()
        sublay.addRow(self._begin_btn, self._status_box)
        layout.insertRow(row, self._label)
        layout.insertRow(row + 1, self._deadline_label, sublay)
        layout.insertRow(row + 2, self._minutes_label)
        layout.insertRow(row + 3, QLabel('-'*30))
        pass
    

    def load(self, data: dict):
        '''Loads `Task` attributes from a dictionary into existing instance.'''
        self._task = Task.from_dict(data)
        # update gui elements
        self._label.setText(self._task.get_subject())
        self._deadline_label.setText("Due: "+str(self._task.get_deadline()))
        self._status_box.setChecked(self._task.is_complete())
        self._minutes_label.setText("Minutes Worked: " + str(round(self._task.get_minutes(),2)))
        pass


    def get_status_box(self) -> QCheckBox:
        return self._status_box


    def save(self) -> dict:
        '''Saves `Task` attributes to a dictionary.'''
        self._task.set_complete(self._status_box.isChecked())
        print(self._status_box.isChecked())
        self._task.to_dict()


    def get_task(self) -> Task:
        return self._task


    def toggle_task(self):
        '''Handles starting/stopping task timer and logging new minutes.'''
        # lock the task runner to this task
        if self._trunner.is_running() == False:
            print('info: entering zen mode for task', self._task.get_subject())
            self._begin_btn.setText("End")
            self._trunner.enable()
            self._is_running = True
            self._status_box.setCheckable(False) # cannot say done with task if still working on it!
        # release the lock on the task runner
        elif self._is_running == True:
            print('info: ending zen mode for task', self._task.get_subject())
            self._begin_btn.setText("Start")
            working = self._trunner.disable()
            # store the worked minutes
            self._task.add_minutes(working)
            # update the minutes gui element
            self._minutes_label.setText("Minutes Worked: " + str(round(self._task.get_minutes(),2)))
            self._is_running = False
            self._status_box.setCheckable(True) # allow user to mark as complete
        pass
    pass