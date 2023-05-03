from PyQt5.QtWidgets import *
from view import *
import csv

"""
This application runs PyQt5 for GUI.
It includes main.py, controller.py, and view.py.
The program outputs to books.csv within the same folder.
"""

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class Controller(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        """
        book: is a list for storing retrieved information from the
        input text boxes.
        Initial setup for the application by clearing the text input boxes,
        then establishing commands to run when each respective button is clicked.
        """
        self.book = []
        self.clear()
        self.buttonClear.clicked.connect(lambda: self.clear())
        self.buttonExit.clicked.connect(lambda: exit(code=0))
        self.buttonSubmit.clicked.connect(lambda: self.submit())

    def submit(self):
        """
        Initiated by pressing the submit button.
        This currently retrieves data typed in the text boxes.
        The data is stored in a list, copied to books.csv and then
        confirmation output is displayed.
        The input boxes are cleared at the end of this.
        :return: There is no return
        """
        self.book = [self.entryISBN.text(), self.entryAuthor.text(), self.entryTitle.text()]
        with open('books.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(self.book)
        self.output.setText(f'This book has been added:'
                            f'\nISBN:    {self.book[0]}'
                            f'\nAuthor:  {self.book[1]}'
                            f'\nTitle:   {self.book[2]}')
        self.entryISBN.setText('')
        self.entryAuthor.setText('')
        self.entryTitle.setText('')

    def clear(self):
        """
        Initiated by pressing the clear button.
        Used to clear the information in each text input box
        and the output screen
        :return: There is no return
        """
        self.output.setText('')
        self.entryISBN.setText('')
        self.entryAuthor.setText('')
        self.entryTitle.setText('')
