import sys
import os
from PyQt5 import QtWidgets

# Add the parent directory to sys.path to ensure MainFrom can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ui.MainFrom import MainFrom

class UIApplication:
    """UI Application class to encapsulate UI functionality"""
    
    @staticmethod
    def run():
        """Run the UI application"""
        app = QtWidgets.QApplication(sys.argv)
        main_app = MainFrom()
        main_app.show()
        sys.exit(app.exec_()) 