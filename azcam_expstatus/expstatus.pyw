"""
Exposure status GUI.
Usage example: pythonw -m azcam_expstatus.expstatus -port 2452
"""

import sys
import time

from PySide6 import QtCore
from PySide6.QtWidgets import QMainWindow, QApplication

import azcam
import azcam.exceptions
import azcam_console
from azcam_console.tools.console_tools import create_console_tools
from azcam_expstatus.expstatus_ui import Ui_ExposureStatus


class ExposureStatus(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()

        MainWindow = QMainWindow()
        self.ui = Ui_ExposureStatus()
        self.ui.setupUi(self)

        self.update_interval = 300  # update time ms
        self.flags = azcam.db.exposureflags

        # blank text on indicators
        self.ui.label_integrating.setText("")
        self.ui.label_reading.setText("")

        # make a timer
        self.timerID = self.ctimer = QtCore.QTimer()

        # connect timer
        QtCore.QObject.connect(
            self.ctimer, QtCore.SIGNAL("timeout()"), self.timer_update
        )

        # start timer
        self.ctimer.start(self.update_interval)

    def timer_update(self):
        """
        Called by timer.
        """

        return self.update()

    def update(self):
        """
        Update GUI indicators.
        """

        # set status text
        status = azcam.db.parameters.get_par("exposureflag")

        for key in self.flags:
            if self.flags[key] == status:
                if key == "NONE":
                    self.ui.label_status.setText("")
                    self.ui.label_reading.setStyleSheet("background-color: none;")
                    self.ui.label_integrating.setStyleSheet("background-color: none;")
                    self.ui.label_integrating.setText("")
                    self.ui.label_reading.setText("")
                else:
                    # set status text
                    self.ui.label_status.setText(key)
                    # set indicator colors
                    if key == "EXPOSING":
                        self.ui.label_integrating.setStyleSheet(
                            "background-color: green;"
                        )
                        self.ui.label_reading.setStyleSheet("background-color: none;")
                        self.ui.label_integrating.setText("Exposing")
                        self.ui.label_reading.setText("")
                    elif key == "READOUT":
                        self.ui.label_reading.setStyleSheet("background-color: red;")
                        self.ui.label_integrating.setStyleSheet(
                            "background-color: none;"
                        )
                        self.ui.label_reading.setText("Reading")
                        self.ui.label_integrating.setText("")
                    else:
                        self.ui.label_reading.setStyleSheet("background-color: none;")
                        self.ui.label_integrating.setStyleSheet(
                            "background-color: none;"
                        )
                        self.ui.label_integrating.setText("")
                        self.ui.label_reading.setText("")

                break

        return

    def create(self):
        # create
        if getattr(azcam.db, "qtapp", None) is None:
            azcam.db.qtapp = QApplication(["ExpStatus"])

        # set window location
        self.move(50, 50)

        # show GUI
        self.show()

        return


def start():
    """
    Command to start expstatus GUI.
    """

    # ****************************************************************
    # parse command line arguments
    # ****************************************************************
    try:
        i = sys.argv.index("-host")
        host = sys.argv[i + 1]
    except ValueError:
        host = "localhost"
    try:
        i = sys.argv.index("-port")
        port = int(sys.argv[i + 1])
    except ValueError:
        port = 2402

    # ****************************************************************
    # create Qt app
    # ****************************************************************
    if azcam.db.get("atapp") is None:
        qtapp = QtCore.QCoreApplication.instance()
        if qtapp is None:
            qtapp = QApplication(sys.argv)
        azcam.db.qtapp = qtapp

    # console tools
    create_console_tools()
    connected = azcam.db.server.connect(host=host, port=port)  # default host and port
    if connected:
        print("Connected to azcamserver")
    else:
        print("Not connected to azcamserver")
        time.sleep(2)
        raise azcam.exceptions.AzcamError("Could not connect to azcamserver")

    gui = ExposureStatus()
    gui.create()

    qtapp.exec()


# execute when run directly
if __name__ == "__main__":
    start()
