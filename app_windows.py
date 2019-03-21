from PyQt5.QtWidgets import  QFormLayout, QLabel, QCheckBox, QWidget, QComboBox, QPushButton
import sqlite3
from sqlite3 import  Error

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Settings')
        self.setGeometry(600, 150, 400, 300)
        conn = create_connection("C:\\Users\Darciu\PycharmProjects\Scribe 2.0\database.db")



        self.layout = QFormLayout()

        self.labelStay = QLabel("Stay on top")
        self.checkStay = QCheckBox()

        self.labelStyle = QLabel("Choose style")
        self.comboStyle = QComboBox()

        self.labelSize = QLabel("Window size")
        self.comboSize = QComboBox()

        self.save = QPushButton("Save settings")

        #Widgets Behaviour
        self.comboStyle.addItem("Old fashion")
        self.comboStyle.addItem("Fresh")

        self.comboSize.addItem("Small")
        self.comboSize.addItem("Medium")
        self.comboSize.addItem("Large")

        self.save.clicked.connect(lambda: self.save_settings(conn))

        self.get_settings(conn)

        #-----------------------------------
        self.layout.addRow(self.labelStay, self.checkStay)
        self.layout.addRow(self.labelStyle,self.comboStyle)
        self.layout.addRow(self.labelSize,self.comboSize)
        self.layout.addWidget(self.save)



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



    def get_settings(self,conn):
        sql_statement = "SELECT stay_on_top, style, size FROM settings WHERE id = 1"

        cur = conn.cursor()
        cur.execute(sql_statement)

        rows = cur.fetchall()

        self.checkStay.setChecked(bool(rows[0][0]))
        self.comboStyle.setCurrentIndex(rows[0][1])
        self.comboSize.setCurrentIndex(rows[0][2])






def create_connection(db_file):
    """ create connection to sqlite database
        db_file - path to the database
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)