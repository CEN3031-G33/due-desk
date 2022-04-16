# ------------------------------------------------------------------------------
# Project  : DueDesk
# Module   : TasklistGui
# Abstract : 
#   A TasklistGui is composed of gui related materials and the business logic 
#   for a `Tasklist`.
# ------------------------------------------------------------------------------
from .taskgui import TaskGui
from .tasklist import Tasklist
from .task import Task
from typing import List
from PyQt5.QtWidgets import *
from .taskrunner import Taskrunner

class TasklistGui(QWidget):
    def __init__(self, root: QMainWindow, inner: List[TaskGui]):
        super(QWidget, self).__init__(root)
        # store root window for future use in gluing to gui
        self._root = root

        self._task_runner = Taskrunner(False)

        # provide mapping between a `Tasklist` and the storage of `TaskGui` objects
        self._tl = Tasklist([]) 
        self._inner = {}
        for tg in inner:
            if self.add(tg) == False:
                print('warning: could not add duplicate task \"'+tg.get_task().get_subject()+"\" to list")
            pass
        self._form_layout = QFormLayout()
        # configure the add task button at top of task list
        button = QPushButton("Add Task")
        button.clicked.connect(self.add_task)
        self._form_layout.addRow(button)
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
        self._group_box.setTitle("My Tasks ("+str(self._tl.get_amt_todo())+")")
        screen = QApplication.primaryScreen()
        self.resize(int(screen.size().width() * 0.2), int(screen.size().height()))
        self.move(int(screen.size().width() * 0.8), 0)
        self.setLayout(self._layout)
        # iterate over the ordered task objects and map into taskgui domain to glue to gui
        # note: make `Tasklist` iterable (implement new class and __iter__)
        # https://thispointer.com/python-how-to-make-a-class-iterable-create-iterator-class-for-it/
        for task in self._tl._inner: 
            if task.is_complete() == False:
                self._inner[task.get_key()].glue_to_gui(self._form_layout, len(self._form_layout))
        self.show()
        pass


    def add_task(self):
        '''Adds a new `Task` to the `Tasklist` from the gui.'''
        subject = self._root.inputTaskSubject()
        # subject verification failed
        if subject == None:
            return
        deadline = self._root.inputTaskDeadline()
        # deadline verification failed
        if str(deadline) == 'None':
            return
        t = Task(subject, deadline)
        # ensure no similiar task exists
        tg = TaskGui(self._root)
        tg.load(t.to_dict())
        tg.track_runner(self._task_runner)
        success = self.add(tg)
        if success == False:
            QErrorMessage(self._root).showMessage("A similiar task already exists")
            return
        # find where to insert the task into the tasklistgui's rows
        index = 0
        self._group_box.setTitle("My Tasks ("+str(self._tl.get_amt_todo())+")")
        for task in self._tl._inner:
            # guaranteed for unique task to return here because we verified no other task
            # exists that is partially equal to it (see `success` variable in this function)
            if task.partial_eq(t):
                tg.glue_to_gui(self._form_layout, (index * 4) + 1)
                break
            if task.is_complete() == False:
                index += 1
        pass


    def add(self, tg: TaskGui) -> bool:
        '''Adds a new `TaskGui` to the list and resorts the list. Returns `false` if a task with the same
        subject and same deadline already exists.'''
        if self._tl.add(tg.get_task()) == True:
            # use subject and deadline as unique key to store `TaskGui` 
            tg.track_runner(self._task_runner)
            self._inner[tg.get_task().get_key()] = tg
            return True
        return False


    def load(self, data: dict) -> None:
        '''Loads `Tasklist` attributes from a dictionary into existing instance.'''
        taskguis = []
        for v in data.values():
            tg = TaskGui(self._root)
            tg.load(v)
            tg.track_runner(self._task_runner)
            taskguis += [tg]

        tlg = TasklistGui(self._root, taskguis)
        self._inner = tlg._inner
        self._tl = tlg._tl
        pass


    def save(self) -> dict:
        print('info: saving tasks...')
        # update all the task's with the gui information about status box
        for task in self._tl._inner: 
            task.set_complete(self._inner[task.get_key()].get_status_box().isChecked())
        # serialize logic
        return self._tl.to_dict()
    pass