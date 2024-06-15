import sys
import os
import signal
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy, QFrame, QSplitter, QTextEdit, QDesktopWidget, QShortcut
)
from PyQt5.QtGui import QTextCursor, QKeySequence, QIcon, QFont
from PyQt5.QtCore import Qt, QProcess, pyqtSignal
from ansi2html import Ansi2HTMLConverter


class DetailLabel(QLabel):
    detail_changed = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setStyleSheet("QLabel { color: black; text-decoration: none; }")
        self.setMouseTracking(True)
        self.setCursor(Qt.PointingHandCursor)
        self.is_expanded = False
        self.update_label_text()

    def update_label_text(self):
        if self.is_expanded:
            self.setText("\u25b2 Détail")  # Flèche vers le haut
        else:
            self.setText("\u25bc Détail")  # Flèche vers le bas

    def mousePressEvent(self, event):
        self.is_expanded = not self.is_expanded
        self.update_label_text()
        self.detail_changed.emit(self.is_expanded)


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.server_state = "Serveur inactif"

        # Création du texte d'explication général
        self.explanation_label = QLabel("<b> Contrôle du serveur Kombucha</b><br>Démarrez le serveur afin de commencer les enregistrements du formulaire.")
        self.explanation_label.setAlignment(Qt.AlignCenter)

        # Création des boutons
        self.start_button = QPushButton('Démarrer', self)
        self.stop_button = QPushButton('Arrêter', self)

        # Ajout d'un petit espace entre les deux boutons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addSpacing(10)  # Ajout d'un espace de 10 pixels entre les boutons
        button_layout.addWidget(self.stop_button)

        # Connexion des boutons aux fonctions
        self.start_button.clicked.connect(self.start_process)
        self.stop_button.clicked.connect(self.stop_process)
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

        # Création du label "Serveur inactif" ou "Serveur actif"
        self.server_status_label = QLabel(self.server_state)
        self.server_status_label.setAlignment(Qt.AlignCenter)
        if self.server_state == "Serveur inactif":
            self.server_status_label.setStyleSheet("QLabel { color: red; font-weight: bold; }")
        else:
            self.server_status_label.setStyleSheet("QLabel { color: green; font-weight: bold; }")

        # Création du label "Détail" personnalisé
        self.detail_label = DetailLabel()
        self.detail_label.detail_changed.connect(self.toggle_console)

        # Fenêtre de console déroulante avec QTextEdit
        self.console_output = QTextEdit(self)
        # Rend la fenêtre de console en lecture seule
        self.console_output.setReadOnly(True)
        # Ne conserve que les 100 dernières entrées
        self.console_output.document().setMaximumBlockCount(100)  # Limite de lignes
        self.console_output.setVisible(False)
        self.console_output.setStyleSheet("background-color: black; color: white;")
        self.console_output.setFont(QFont("Arial", 12))


        # Layout vertical pour organiser les boutons et la fenêtre de console
        button_console_layout = QVBoxLayout()
        button_console_layout.addWidget(self.explanation_label)
        button_console_layout.addLayout(button_layout)
        button_console_layout.addWidget(self.server_status_label)
        button_console_layout.addWidget(self.detail_label)
        button_console_layout.addWidget(self.console_output)

        # Création du splitter pour diviser les widgets
        splitter = QSplitter()
        splitter.addWidget(QWidget())  # Widget vide pour la zone gauche
        splitter.addWidget(QWidget())  # Widget vide pour la zone droite
        splitter.setSizes([1, 0])  # Tailles initiales pour les deux zones
        splitter.setCollapsible(0, False)  # Empêche le widget gauche de se rétracter

        # Layout vertical pour organiser les boutons et le label "Détail"
        main_layout = QVBoxLayout()
        main_layout.addLayout(button_console_layout)
        main_layout.addWidget(splitter)
        main_layout.setContentsMargins(10, 10, 10, 10)  # Marges de 20 pixels
        main_layout.setSpacing(10)  # Espacement de 10 pixels entre les widgets

        # Faire en sorte que la position verticale des éléments reste fixe
        main_layout.setAlignment(Qt.AlignTop)

        self.setLayout(main_layout)
        self.setWindowTitle('Serveur Kombucha')
        self.setMinimumWidth(600)  # Largeur minimale de la fenêtre

        self.ansi2html = Ansi2HTMLConverter()

        # Centrer la fenêtre au démarrage
        self.center_on_screen()
        # Icone
        self.setWindowIcon(QIcon('favicon.ico'))
        
        # Créer un raccourci clavier pour Ctrl+C
        shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_C), self)
        shortcut.activated.connect(self.stop_process)
        

    def center_on_screen(self):
        # Centrer la fenêtre sur l'écran
        screen_geo = QApplication.desktop().screenGeometry()
        x = (screen_geo.width() - self.width()) // 2
        y = (screen_geo.height() - self.height()) // 2
        self.move(x, y)

    def start_process(self):
        # Action lorsque le bouton "Démarrer" est cliqué
        self.process = QProcess()
        self.process.setProcessChannelMode(QProcess.MergedChannels)  # Pour afficher stdout et stderr ensemble

        self.process.readyReadStandardOutput.connect(self.handle_output)
        self.process.readyReadStandardError.connect(self.handle_output)
        self.process.finished.connect(self.process_finished)
        
        self.console_output.append("Démarrage du serveur ...\n")
        self.process.start("python3", ["-u","Kombucha_server.py"])
        if self.process.waitForStarted():
            self.server_state = "Serveur actif"
            self.server_status_label.setText(self.server_state)
            self.server_status_label.setStyleSheet("QLabel { color: green; font-weight: bold; }")
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
        else:
            self.console_output.append('Impossible de démarrer le server...')

    def stop_process(self):
        # Action lorsque le bouton "Arrêter" est cliqué
        if self.server_state == "Serveur actif":
            self.console_output.setStyleSheet("background-color: black; color: white;") 
            self.console_output.setFont(QFont("Arial", 12)) # Réinitialise les styles CSS à vide
            self.console_output.append('Arrêt du serveur ...')
            self.process.terminate()
            self.process.waitForFinished()
            self.server_state = "Serveur inactif"
            self.server_status_label.setText(self.server_state)
            self.server_status_label.setStyleSheet("QLabel { color: red; font-weight: bold;}")
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
        else:
            self.console_output.append('Le serveur est déjà arrêté.')
            
    def process_finished(self):
        self.console_output.setStyleSheet("background-color: black; color: white;") 
        self.console_output.setFont(QFont("Arial", 12)) # Réinitialise les styles CSS à vide
        self.console_output.append('Serveur arrêté.\n')

    def toggle_console(self, show_console):
        # Afficher ou masquer la fenêtre de console en fonction de l'état du label "Détail"
        if show_console:
            self.console_output.setVisible(True)
            self.resize(self.width(), 600)  # Augmente la hauteur de la fenêtre
        else:
            self.console_output.setVisible(False)
            self.resize(0, 0)  # Réduit la hauteur de la fenêtre
            self.resize(0, 0)  # Réduit la hauteur de la fenêtre

        # Scroller jusqu'au bas de la fenêtre de console
        self.console_output.moveCursor(QTextCursor.End)
        
    def handle_output(self):
        # Gestion de la sortie du processus Flask
        data = self.process.readAll()
        if data:
            text = bytes(data).decode('utf-8')
            # Convertir les séquences ANSI en HTML
            html_output = self.ansi2html.convert(text)
            # Ajouter le texte à la console
            self.append_text_to_console(html_output)

    def append_text_to_console(self, text):
        cursor = self.console_output.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertHtml(text)
        self.console_output.setTextCursor(cursor)
        self.console_output.ensureCursorVisible()
        
        
# Lancement de l'application principale
if __name__ == '__main__':
    appli = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(appli.exec_())

