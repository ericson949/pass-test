from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton,QHBoxLayout
from PyQt5.QtCore import Qt, QPoint
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QColor, QPainter

class NotificationBarWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        screen_geometry = QApplication.desktop().screenGeometry()
        width, height = screen_geometry.width(), screen_geometry.height()

        # Set window position and size
        self.setGeometry(width - 700, height - 200, 300, 50)

        # self.setGeometry(100, 100, 100, 50)
        
        # Rendre le fond transparent
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        

        # Création du layout
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Bouton rond
        self.button_record = QPushButton("C")
        self.button_record.setFixedSize(50, 50)
        self.button_record.setStyleSheet("QPushButton { border-radius: 25px; background-color: green; font: bold 16px; }")
        layout.addWidget(self.button_record, alignment=Qt.AlignLeft)
        
        # Bouton rond
        self.button_ok = QPushButton("OK")
        self.button_ok.setFixedSize(50, 50)
        self.button_ok.setStyleSheet("QPushButton { border-radius: 25px; background-color: green; font: bold 16px; }")
        layout.addWidget(self.button_ok, alignment=Qt.AlignLeft)
        
        
        # Bouton rond
        self.button = QPushButton("S")
        self.button.setFixedSize(50, 50)  # Définit la taille du bouton
        self.button.setStyleSheet("QPushButton { border-radius: 25px; background-color: cyan; font: bold 12px; }")  # Style pour arrondir les coins et centrer le texte
        self.button.clicked.connect(self.toggle_label)
        layout.addWidget(self.button, alignment=Qt.AlignLeft)  # Alignement à droite pour le bouton

        # Zone de texte
        self.label = QLabel("Ceci est une notification fdfdsfs sdsqdq qdqsdsqdsqd")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background-color: white;")
        font = QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.hide()
        layout.addWidget(self.label)
        
        # Créer un effet de flou
        # self.blur_effect = QGraphicsBlurEffect()
        # self.blur_effect.setBlurRadius(5)
        # self.label.setGraphicsEffect(self.blur_effect)
        
         # **Appel à paintEvent pour initialiser l'affichage**
        # self.update()
            
        self.setLayout(layout)

        # Variables pour le déplacement
        self.dragging = False
        self.offset = QPoint()

        # Gestionnaires d'événements pour le déplacement
        layout.mousePressEvent = self.mousePressEvent
        layout.mouseMoveEvent = self.mouseMoveEvent
        layout.mouseReleaseEvent = self.mouseReleaseEvent
        
    
        self.adjustSize()
        self.setLayout(layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()
    def toggle_label(self):
            if self.label.isVisible():
                self.label.hide()
                self.button.setText("S")
                self.adjustSize()
            else:
                self.label.show()
                self.button.setText("P")
                self.adjustSize()
                
    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.dragging = False
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 5))  # Couleur de fond semi-transparente
        super().paintEvent(event)
        
    @QtCore.pyqtSlot(str)
    def updateStatus(self, status):
        self.label.setText(status)
        self.label.show()
        self.button.setText("P")
        self.adjustSize()
