from controller import *


def main():
    """main function to start book application"""
    app = QApplication([])
    window = Controller()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()