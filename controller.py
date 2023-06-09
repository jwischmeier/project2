from PyQt5.QtWidgets import *
from view import *
import csv, urllib.request, json

"""
Some of this code is credit to GitHub user AO8, specifically within isbn_lookup.
https://gist.github.com/AO8/faa3f52d3d5eac63820cfa7ec2b24aa7#file-isbn_lookup-py
AO8 code is used to link ISBN through Google API.
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
        self.buttonLookup.clicked.connect(lambda: self.isbn_lookup())

    def submit(self):
        """
        Initiated by pressing the submit button.
        This currently retrieves data typed in the text boxes.
        The data is stored in a list, copied to books.csv and then
        confirmation output is displayed.
        The input boxes are cleared at the end of this.
        If the ISBN is already in the books.csv file, it does not add
        the book and informs the user it already exists.
        :return: There is no return
        """
        self.book = [self.entryISBN.text().strip(), self.entryAuthor.text(), self.entryTitle.text()]
        csvfile = csv.reader(open('books.csv', 'r'))
        for row in csvfile:
            if self.book[0] == row[0]:
                self.output.setText('You already have this book.\nPress clear to continue.')
        if self.output.text() != 'You already have this book.\nPress clear to continue.':
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

    def isbn_lookup(self):
        """
        Initiated by pressing the Lookup button.
        This retrieves the information from the ISBN text box
        and checks it against the Google API.
        If information is found it populates the text boxes.
        If information is not found, it informs the user.
        :return: There is no return
        """
        try:
            base_api_link = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
            user_input = self.entryISBN.text().strip()
            with urllib.request.urlopen(base_api_link + user_input) as f:
                text = f.read()
            decoded_text = text.decode("utf-8")
            obj = json.loads(decoded_text)  # deserializes decoded_text to a Python object
            volume_info = obj["items"][0]
            authors = obj["items"][0]["volumeInfo"]["authors"]
            self.entryTitle.setText(f'{volume_info["volumeInfo"]["title"]}')
            self.entryAuthor.setText(f'{",".join(authors)}')
            self.output.setText('')
        except:
            self.output.setText('Unable to find this ISBN')

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
