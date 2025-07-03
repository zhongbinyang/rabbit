#!flask/bin/python
import sys
import threading
import time
from PyQt5 import QtWidgets
from RSETAPI import *
from MainFrom import *

def runUI():
    app = QtWidgets.QApplication(sys.argv)
    main_app = MainFrom()
    main_app.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    thread = threading.Thread(target=lambda: api.run('0.0.0.0', 5001,debug=False))
    thread.start()
    time.sleep(1)
    runUI()
    thread.join()
