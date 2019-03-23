from PyQt5.QtWidgets import  QFormLayout, QLabel, QCheckBox, QWidget, QComboBox, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
import sqlite3
from sqlite3 import Error

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Settings')

        conn = create_connection("database.db")



        self.layout = QFormLayout()

        self.labelStay = QLabel("Stay on top")
        self.checkStay = QCheckBox()

        self.labelStyle = QLabel("Choose style")
        self.comboStyle = QComboBox()

        self.labelSize = QLabel("Window size")
        self.comboSize = QComboBox()


        self.save = QPushButton("Save and close settings")

        self.labelNote = QLabel("Changes will be applied when the application is restarted.")

        #Widgets Behaviour
        self.comboStyle.addItem("Windows")
        self.comboStyle.addItem("WindowsVista")
        self.comboStyle.addItem("Fusion")

        self.comboSize.addItem("Small")
        self.comboSize.addItem("Medium")
        self.comboSize.addItem("Large")

        self.save.clicked.connect(lambda: self.save_settings(conn))

        self.get_settings(conn)
        self.setGeometry(600, 150, 400, 300)

        #-----------------------------------
        self.layout.addRow(self.labelStay, self.checkStay)
        self.layout.addRow(self.labelStyle,self.comboStyle)
        self.layout.addRow(self.labelSize,self.comboSize)

        self.layout.addWidget(self.save)

        self.layout.addWidget(self.labelNote)



        self.setLayout(self.layout)





    def save_settings(self, conn):
        sql_sentence = ''' UPDATE settings
                                SET stay_on_top = ? ,
                                    style = ? ,
                                    size = ?
                              WHERE id = 1'''


        task = ()
        task = task + (self.checkStay.checkState(),)
        task = task + (self.comboStyle.currentIndex(),)
        task = task + (self.comboSize.currentIndex(),)

        cur = conn.cursor()
        cur.execute(sql_sentence, task)
        conn.commit()

        self.close()

    def get_settings(self,conn):
        sql_statement = "SELECT stay_on_top, style, size FROM settings WHERE id = 1"

        cur = conn.cursor()
        cur.execute(sql_statement)

        rows = cur.fetchall()

        self.checkStay.setChecked(bool(rows[0][0]))
        self.comboStyle.setCurrentIndex(rows[0][1])
        self.comboSize.setCurrentIndex(rows[0][2])


        if rows[0][0] == 2:
            QWidget.__init__(self, None, Qt.WindowStaysOnTopHint)



class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("About - overall information")

        self.setGeometry(600, 150, 300, 500)

        self.label1 = QLabel("Information about Scribe 2.0")

        self.label2 = QLabel("Scribe 2.0 is Python coded desktop application. It allows you to store, search and edit short notes with formatting.\nIn order "
                             "to add a new note go to the tab 'Add', put in appropriate data (all fields are required) and click add button.\nIn case of "
                             "searching the data, just type in phase, or part of it, into text field, click 'Search' and double click on interesting record.\n"
                             "You can either edit the record selecting it from list of search results and clicking button 'Edit'.\nMore information about "
                             "searching engine you can find in README file.\n\nIf you want to add existing database records to yours, choose Import database from " 
                             "Application menu and find the .db file.\n\nNote: if you want all records to be displayed while searching, type in 'all' into "
                             "the searching field.")

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.label1)

        self.layout.addWidget(self.label2)

        self.setLayout(self.layout)









def create_connection(db_file):
    """ create connection to sqlite database
        db_file - path to the database
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)