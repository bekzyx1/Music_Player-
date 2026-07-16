import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
import design
from pygame import mixer


class Player(QMainWindow, design.Ui_MainWindow):

    def __init__(self):
        super(Player, self).__init__()
        self.setupUi(self)

        self.current_dir = ""
        self.playlist = []
        self.audio_available = False

        try:
            mixer.init()
            self.audio_available = True
        except Exception as exc:
            QMessageBox.warning(self, "Audio Initialization Error", str(exc))

        self.pushButton.clicked.connect(self.prev_sound)
        self.pushButton_2.clicked.connect(self.play_sound)
        self.pushButton_3.clicked.connect(self.next_sound)
        self.pushButton_4.clicked.connect(self.add_sound)
        self.pushButton_5.clicked.connect(self.remove_sound)
        self.listWidget.doubleClicked.connect(self.play_sound)

        self.update_buttons()

    def update_buttons(self):
        has_items = self.listWidget.count() > 0
        self.pushButton.setEnabled(has_items)
        self.pushButton_2.setEnabled(has_items)
        self.pushButton_3.setEnabled(has_items)
        self.pushButton_4.setEnabled(True)
        self.pushButton_5.setEnabled(has_items)

    def play_sound(self):
        if self.listWidget.count() == 0:
            return

        item = self.listWidget.currentItem()
        if item is None:
            self.listWidget.setCurrentRow(0)
            item = self.listWidget.currentItem()
            if item is None:
                return

        filename = os.path.join(self.current_dir, item.text())
        if not os.path.isfile(filename):
            QMessageBox.warning(self, "Playback Error", f"File not found:\n{filename}")
            return

        if not self.audio_available:
            QMessageBox.warning(self, "Playback Error", "Audio device is not available.")
            return

        try:
            mixer.music.load(filename)
            mixer.music.play()
        except Exception as exc:
            QMessageBox.warning(self, "Playback Error", str(exc))

    def stop_sound(self):
        if self.audio_available:
            mixer.music.stop()

    def remove_sound(self):
        self.stop_sound()
        self.listWidget.clear()
        self.playlist = []
        self.current_dir = ""
        self.update_buttons()

    def prev_sound(self):
        if self.listWidget.count() == 0:
            return
        row = self.listWidget.currentRow()
        if row > 0:
            self.listWidget.setCurrentRow(row - 1)
            self.play_sound()

    def next_sound(self):
        if self.listWidget.count() == 0:
            return
        row = self.listWidget.currentRow()
        if row < self.listWidget.count() - 1:
            self.listWidget.setCurrentRow(row + 1)
            self.play_sound()

    def add_sound(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if not directory:
            return

        self.current_dir = directory
        self.playlist = []
        self.listWidget.clear()

        supported = (".wav", ".mp3", ".ogg", ".flac")
        for filename in sorted(os.listdir(directory)):
            if filename.lower().endswith(supported):
                self.playlist.append(filename)
                self.listWidget.addItem(filename)

        if not self.playlist:
            QMessageBox.information(self, "No Audio Files", "No supported audio files found in the selected folder. Use .wav, .mp3, .ogg, or .flac.")
        else:
            self.listWidget.setCurrentRow(0)

        self.update_buttons()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    player = Player()
    player.show()
    app.exec()
 
