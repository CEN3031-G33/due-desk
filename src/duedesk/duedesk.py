# ------------------------------------------------------------------------------
# Project  : DueDesk
# Module   : duedesk
# Abstract : 
#   The main script called to begin the DueDesk application.
# ------------------------------------------------------------------------------
from .window import *

def duedesk():
    app = QApplication(sys.argv)
    App()
    sys.exit(app.exec_())


def main():
    duedesk()


if __name__ == "__main__":
    main()
