from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QWidget
)
from PyQt5.QtGui import QIcon
from datetime import datetime
import sys
import os


class PersistentNotepadApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FastNotes")
        self.setGeometry(100, 100, 400, 500)
        self.setWindowIcon(QIcon("./sources/note_icon.png"))

        self.sources_dir = "sources"
        os.makedirs(self.sources_dir, exist_ok=True)
        self.file_path = os.path.join(self.sources_dir, "FastNotes.txt")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)

        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Escribe tu nota aquí...")
        self.layout.addWidget(self.text_input)

        self.save_button = QPushButton("Guardar Nota")
        self.layout.addWidget(self.save_button)

        self.save_button.clicked.connect(self.save_note)
        self.text_input.returnPressed.connect(self.save_note)
        self.list_widget.itemClicked.connect(self.delete_note)

        self.notes = []
        self.load_notes()

    def load_notes(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as file:
                for line in file:
                    note = line.strip()
                    if note:
                        self.notes.append(note)
                        self.list_widget.addItem(note)

    def save_note(self):
        note = self.text_input.text()
        if note.strip():
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            formatted_note = f"[{timestamp}] {note}"
            self.notes.append(formatted_note)
            self.list_widget.addItem(formatted_note)
            self.write_notes_to_file()
            self.text_input.clear()

    def delete_note(self, item):
        self.notes.remove(item.text())
        self.list_widget.takeItem(self.list_widget.row(item))
        self.write_notes_to_file()

    def write_notes_to_file(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            for note in self.notes:
                file.write(note + "\n")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PersistentNotepadApp()
    window.show()
    sys.exit(app.exec_())
