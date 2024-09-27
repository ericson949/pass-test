from PyQt5.QtWidgets import QApplication
from ui.NotifcationBarWindow import NotificationBarWindow
from workers.MouseClickWorker import MouseClickWorker
from PyQt5 import QtCore
import sys

class ManageApp(QtCore.QObject):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

        # Create a gui object.
        self.gui = NotificationBarWindow()

        # Create a new worker thread.
        self.createWorkerThread()

        # Make any cross object connections.
        # self._connectSignals()

        self.gui.show()
        
    def _connectSignals(self):
        # self.gui.button_cancel.clicked.connect(self.forceWorkerReset)
        self.signalStatus.connect(self.gui.updateStatus)
        self.parent().aboutToQuit.connect(self.forceWorkerQuit)
        
    def createWorkerThread(self):

        # Setup the worker object and the worker_thread.
        self.worker = MouseClickWorker()
        self.worker_thread = QtCore.QThread()
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()

        # Connect any worker signals
        self.worker.signalStatus.connect(self.gui.updateStatus)
        # self.gui.button_record.clicked.connect(self.forceWorkerQuit)
        
        self.gui.button_record.clicked.connect(self.worker.startMouseListening)
        self.gui.button_ok.clicked.connect(self.forceWorkerQuit)
    
    def launch(self):
        rect = self.gui.geometry()
        self.worker.startMouseListening(rect)
    def forceWorkerQuit(self):
        self.worker.stopListener()
        # if self.worker_thread.isRunning():
        #     self.worker_thread.terminate()
        #     self.worker_thread.wait()
    
if __name__=='__main__':
    app = QApplication(sys.argv)
    example = ManageApp(app)
    sys.exit(app.exec_())