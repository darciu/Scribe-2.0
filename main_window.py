from PyQt5.QtWidgets import (QGridLayout, QApplication, QLabel, QWidget, QPushButton, QTextEdit, QMessageBox, QStyleFactory,
                             QListWidget, QTabWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QMainWindow, QAction, QColorDialog,
                             QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys
import sqlite3
from sqlite3 import Error
import datetime
from app_windows import SettingsWindow, AboutWindow




class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        conn = create_connection("database.db")

        self.set_settings(conn)



        self.setWindowTitle("Scribe 2.0")

        self.tab_widget = Tabs(self)
        self.setCentralWidget(self.tab_widget)

        # Menu Bar

        self.statusBar()

        #print(self.style().objectName())   #print application style

        menuSettings = QAction("&Settings", self)
        menuSettings.setStatusTip("Set settings...")
        menuSettings.triggered.connect(self.menuSettings_opt)

        menuImport = QAction("&Import database", self)
        menuImport.setStatusTip("Import notes from other source...")
        menuImport.triggered.connect(lambda: self.menuImport_opt(conn))

        menuAbout = QAction("&About", self)
        menuAbout.setStatusTip("Information about the application...")
        menuAbout.triggered.connect(self.menuAbout_opt)

        menuExit = QAction("&Exit",self)
        menuExit.setStatusTip("Exit application...")
        menuExit.triggered.connect(self.menuExit_opt)

        mainMenu = self.menuBar()

        optionsMenu = mainMenu.addMenu('&Application')
        optionsMenu.addAction(menuSettings)
        optionsMenu.addAction(menuImport)
        optionsMenu.addAction(menuAbout)
        optionsMenu.addAction(menuExit)

    def menuSettings_opt(self):
        self.display = SettingsWindow()
        self.display.show()


    def menuImport_opt(self,conn_old):
        file_path = QFileDialog.getOpenFileName(self, 'Select database...', 'c:\\',"Database (*.db)")
        if file_path[0] == "":
            return

        try:
            conn_new = sqlite3.connect(file_path[0])

            cursor_new = conn_new.cursor()
            cursor_new.execute("SELECT title,tag1,tag2,content,datetime FROM notes")
            store_content = cursor_new.fetchall()

            cursor_old = conn_old.cursor()

            for row in store_content:
                cursor_old.execute("INSERT INTO notes(title,tag1,tag2,content,datetime) VALUES(?,?,?,?,?)", row)

            conn_old.commit()
            conn_old.close()
        except:
            QMessageBox.about(self,"Invalid Input Error","There is something wrong with format of a database you want to merge with local database.\n"
                                                         "Database should contain 'notes' table with id[PK], title [text], tag1[text], tag2[text], content"
                                                         "[text], datetime[text] columns.")



    def menuAbout_opt(self):
        self.display = AboutWindow()
        self.display.show()



    def menuExit_opt(self):
        choice = QMessageBox.question(self, 'Exit Scribe', 'Do you want to exit Scribe?',
                                      QMessageBox.Yes | QMessageBox.No)

        if choice == QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def set_settings(self, conn):
        sql_statement = "SELECT stay_on_top, style, size FROM settings WHERE id = 1"

        cur = conn.cursor()
        cur.execute(sql_statement)

        rows = cur.fetchall()

        if rows[0][0] == 2:
            QMainWindow.__init__(self, None, Qt.WindowStaysOnTopHint)

        if rows[0][1] == 0:
            QApplication.setStyle(QStyleFactory.create("Windows"))
        elif rows[0][1] == 1:
            QApplication.setStyle(QStyleFactory.create("WindowsVista"))
        elif rows[0][1] == 2:
            QApplication.setStyle(QStyleFactory.create("Fusion"))

        if rows[0][2] == 0:
            self.setGeometry(300, 100, 300, 350)
        elif rows[0][2] == 1:
            self.setGeometry(300, 100, 700, 600)
        elif rows[0][2] == 2:
            self.setGeometry(300, 100, 1000, 700)


class Tabs(QWidget):


    indexList = []

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        conn = create_connection("database.db")

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.layout = QHBoxLayout()


        self.tabs.addTab(self.tab1, "Search")
        self.tabs.addTab(self.tab2, "Add")



        self.tabSearch(conn)
        self.tabAddEdit(conn)


        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    @classmethod
    def indexList_append(cls, value):
        cls.indexList.append(value)

    @classmethod
    def indexList_clear(cls):
        cls.indexList = []



    def tabSearch(self,conn):
        """
        create Search Tab
        :param conn: connection with database
        """
        #Layouts declarations
        self.layoutSearch1 = QGridLayout()
        self.layoutSearch1_2 = QHBoxLayout()
        self.layoutSearch1_3 = QVBoxLayout()

        #Widgets
        self.display_notepadSearch = QTextEdit() #main text field to write a note
        titleSearchLabel = QLabel("Title")
        self.titleSearchField = QLineEdit()
        tag1SearchLabel = QLabel("Tag1")
        self.tag1SearchField = QLineEdit()
        tag2SearchLabel = QLabel("Tag2")
        self.tag2SearchField = QLineEdit()


        self.searchBTN = QPushButton("Search")
        self.searchList = QListWidget()
        self.editBTN = QPushButton("Edit")
        self.searchField = QLineEdit()
        self.deleteBTN = QPushButton("Delete")



        #Widgets behaviour
        self.searchBTN.clicked.connect(lambda: self.click_searchBTN(conn))
        self.editBTN.clicked.connect(lambda: self.click_editBTN(conn))
        self.searchList.doubleClicked.connect(lambda: self.doubleClickDisplay(conn))
        self.deleteBTN.clicked.connect(lambda: self.click_deleteBTN(conn))

        self.display_notepadSearch.setReadOnly(True)
        self.titleSearchField.setReadOnly(True)
        self.tag1SearchField.setReadOnly(True)
        self.tag2SearchField.setReadOnly(True)



        #layout construction
        self.layoutSearch1.addWidget(self.display_notepadSearch,0,0)
        self.layoutSearch1.addItem(self.layoutSearch1_2,1,0)
        self.layoutSearch1.addItem(self.layoutSearch1_3,0,1)

        self.layoutSearch1_2.addWidget(titleSearchLabel,1, Qt.AlignRight)
        self.layoutSearch1_2.addWidget(self.titleSearchField,1)
        self.layoutSearch1_2.addWidget(tag1SearchLabel,1, Qt.AlignRight)
        self.layoutSearch1_2.addWidget(self.tag1SearchField,1)
        self.layoutSearch1_2.addWidget(tag2SearchLabel,1, Qt.AlignRight)
        self.layoutSearch1_2.addWidget(self.tag2SearchField,1)

        self.layoutSearch1_3.addWidget(self.searchBTN)
        self.layoutSearch1_3.addWidget(self.searchField)
        self.layoutSearch1_3.addWidget(self.searchList)
        self.layoutSearch1_3.addWidget(self.editBTN)
        self.layoutSearch1_3.addWidget(self.deleteBTN)



        #set Search Layout
        self.tab1.setLayout(self.layoutSearch1)





    def doubleClickDisplay(self,conn):
        sql_statement = "SELECT * FROM notes WHERE id = {}".format(self.indexList[self.searchList.currentRow()])

        cur = conn.cursor()
        cur.execute(sql_statement)

        rows = cur.fetchall()

        self.titleSearchField.setText(rows[0][1])
        self.tag1SearchField.setText(rows[0][2])
        self.tag2SearchField.setText(rows[0][3])
        self.display_notepadSearch.setHtml(rows[0][4])






    def click_searchBTN(self, conn):

        if self.searchField.text().upper() == "ALL":
            sql_statement = "SELECT id, title, tag1, tag2, content, datetime FROM notes"
        else:
            sql_statement = "SELECT id, title, tag1, tag2, content, datetime FROM notes WHERE title LIKE UPPER('%{}%')".format(
                self.searchField.text())



        if self.searchField.text() != "":

            cur = conn.cursor()
            cur.execute(sql_statement)

            rows = cur.fetchall()

            self.searchList.clear()
            self.indexList_clear()

            for row in rows:
                self.searchList.addItem(row[1] + "; 1#" + row[2] + "; 2#" + row[3] + "; || last edit: " + row[5])
                self.indexList_append(int(row[0]))
        else:
            self.searchList.clear()
            return None



    def clear_Search(self):
        self.titleSearchField.setText("")
        self.tag1SearchField.setText("")
        self.tag2SearchField.setText("")
        self.display_notepadSearch.setPlainText("")
        self.searchList.clear()



    def click_editBTN(self,conn):
        if self.searchList.currentRow() == -1:
            return None

        self.tabs.setCurrentIndex(1)
        self.tabs.setTabText(1,"Edit")
        self.tabs.setTabEnabled(0,False)
        self.addeditBTN.setText("Edit (save)")
        self.backBTN.setEnabled(True)



        #Extract appropriate record to edit
        sql_statement = "SELECT * FROM notes WHERE id = {}".format(self.indexList[self.searchList.currentRow()])

        cur = conn.cursor()
        cur.execute(sql_statement)

        rows = cur.fetchall()

        self.titleAddEdithField.setText(rows[0][1])
        self.tag1AddEditField.setText(rows[0][2])
        self.tag2AddEditField.setText(rows[0][3])
        self.display_notepadAddEdit.setHtml(rows[0][4])




    def click_deleteBTN(self, conn):
        if self.searchList.currentRow() == -1:
            return None

        choice = QMessageBox.question(self, 'Delete', 'Do you really want to delete this record?',
                                      QMessageBox.Yes | QMessageBox.No)

        if choice == QMessageBox.Yes:
            self.deleteRecord(conn)
        else:
            pass


    def deleteRecord(self,conn):

        sql_statement = "DELETE FROM notes WHERE id = {}".format(self.indexList[self.searchList.currentRow()])

        cur = conn.cursor()
        cur.execute(sql_statement)
        self.searchList.clear()

    #=====================ADD EDIT TAB=============================





    def tabAddEdit(self, conn):

        #Layouts declarations
        self.layoutAddEdit1 = QGridLayout()
        self.layoutAddEdit1_2 = QHBoxLayout()
        self.layoutAddEdit1_3 = QGridLayout()
        self.layoutAddEdit1_3_1 = QHBoxLayout()
        self.layoutAddEdit1_3_2 = QHBoxLayout()



        #Widgets
        self.display_notepadAddEdit = QTextEdit() #main text display while add edit

        self.boldBTN = QPushButton("B")
        self.underlineBTN = QPushButton("U")
        self.italicBTN = QPushButton("I")

        self.changecolorBTN = QPushButton("Change font color")
        self.changecolorBgBTN = QPushButton("Change background color")

        self.addeditBTN = QPushButton("Add")
        self.backBTN = QPushButton("Back w/o saving")




        titleAddEditLabel = QLabel("Title")
        self.titleAddEdithField = QLineEdit()
        tag1AddEditLabel = QLabel("Tag1")
        self.tag1AddEditField = QLineEdit()
        tag2AddEditLabel = QLabel("Tag2")
        self.tag2AddEditField = QLineEdit()

        # Buttons functionality

        self.boldBTN.clicked.connect(self.click_boldBTN)
        self.underlineBTN.clicked.connect(self.click_underlineBTN)
        self.italicBTN.clicked.connect(self.click_italicBTN)

        self.changecolorBTN.clicked.connect(self.click_changecolorBTN)
        self.changecolorBgBTN.clicked.connect(self.click_changecolorBgBTN)

        self.backBTN.setEnabled(False)
        self.addeditBTN.clicked.connect(lambda: self.click_addeditBTN(conn))
        self.backBTN.clicked.connect(self.click_backBTN)





        #layout construction
        self.layoutAddEdit1.addWidget(self.display_notepadAddEdit,0,0)
        self.layoutAddEdit1.addItem(self.layoutAddEdit1_2,1,0)
        self.layoutAddEdit1.addItem(self.layoutAddEdit1_3,0,1)

        self.layoutAddEdit1_3.addItem(self.layoutAddEdit1_3_1,0,0)
        self.layoutAddEdit1_3.addWidget(self.changecolorBTN,1,0)
        self.layoutAddEdit1_3.addWidget(self.changecolorBgBTN, 2, 0)
        self.layoutAddEdit1_3.addItem(self.layoutAddEdit1_3_2, 3, 0)



        self.layoutAddEdit1_2.addWidget(titleAddEditLabel,1, Qt.AlignRight)
        self.layoutAddEdit1_2.addWidget(self.titleAddEdithField,1)
        self.layoutAddEdit1_2.addWidget(tag1AddEditLabel,1, Qt.AlignRight)
        self.layoutAddEdit1_2.addWidget(self.tag1AddEditField,1)
        self.layoutAddEdit1_2.addWidget(tag2AddEditLabel,1, Qt.AlignRight)
        self.layoutAddEdit1_2.addWidget(self.tag2AddEditField,1)

        self.layoutAddEdit1_3_1.addWidget(self.boldBTN)
        self.layoutAddEdit1_3_1.addWidget(self.underlineBTN)
        self.layoutAddEdit1_3_1.addWidget(self.italicBTN)

        self.layoutAddEdit1_3_2.addWidget(self.addeditBTN)
        self.layoutAddEdit1_3_2.addWidget(self.backBTN)



        # set AddEdit Layout
        self.tab2.setLayout(self.layoutAddEdit1)

    def click_boldBTN(self):
        w = self.display_notepadAddEdit.fontWeight()
        if w == 50:
            self.display_notepadAddEdit.setFontWeight(QFont.Bold)
        elif w == 75:
            self.display_notepadAddEdit.setFontWeight(QFont.Normal)





    def click_underlineBTN(self):
        ul = self.display_notepadAddEdit.fontUnderline()

        if ul == False:
            self.display_notepadAddEdit.setFontUnderline(True)
        elif ul == True:
            self.display_notepadAddEdit.setFontUnderline(False)

    def click_italicBTN(self):
        i = self.display_notepadAddEdit.fontItalic()

        if i == False:
            self.display_notepadAddEdit.setFontItalic(True)
        elif i == True:
            self.display_notepadAddEdit.setFontItalic(False)


    def click_changecolorBTN(self):
        c = QColorDialog.getColor()

        self.display_notepadAddEdit.setTextColor(c)

    def click_changecolorBgBTN(self):
        c = QColorDialog.getColor()

        self.display_notepadAddEdit.setTextBackgroundColor(c)






    def click_addeditBTN(self, conn):

        if self.tabs.tabText(1) == "Add":
            self.addRecord(conn)
        elif self.tabs.tabText(1) =="Edit":
            self.editRecord(conn)





    def addRecord(self,conn):


        if self.checkAddEditConditions():
            QMessageBox.about(self,"Empty fields","Some of required fields are empty. You cannot add this record!")
            return None


        sql_sentence = ''' INSERT INTO notes(title,tag1,tag2,content,datetime)
                  VALUES(?,?,?,?,?) '''
        now = datetime.datetime.now()


        task = ()
        task = task + (self.titleAddEdithField.text(),)
        task = task + (self.tag1AddEditField.text(),)
        task = task + (self.tag1AddEditField.text(),)
        task = task + (self.display_notepadAddEdit.toHtml(),)
        task = task + (now.strftime("%Y-%m-%d %H:%M:%S"),)

        cur = conn.cursor()
        cur.execute(sql_sentence, task)
        conn.commit()

        self.clear_AddEdit()


    def editRecord(self,conn):

        if self.checkAddEditConditions():
            QMessageBox.about(self,"Empty fields","Some of required fields are empty. You cannot edit this record!")
            return None

        sql_sentence = ''' UPDATE notes
                        SET title = ? ,
                            tag1 = ? ,
                            tag2 = ?,
                            content = ?
                      WHERE id = ?'''

        task = ()
        task = task + (self.titleAddEdithField.text(),)
        task = task + (self.tag1AddEditField.text(),)
        task = task + (self.tag1AddEditField.text(),)
        task = task + (self.display_notepadAddEdit.toHtml(),)
        task = task + (self.indexList[self.searchList.currentRow()],)


        cur = conn.cursor()
        cur.execute(sql_sentence, task)
        conn.commit()

        self.click_backBTN()
        self.clear_Search()


    def click_backBTN(self):
        self.tabs.setCurrentIndex(0)
        self.tabs.setTabText(1,"Add")
        self.tabs.setTabEnabled(0,True)
        self.addeditBTN.setText("Add")
        self.backBTN.setEnabled(False)

        self.clear_AddEdit()



    def clear_AddEdit(self):
        """
        clears Add or Edit Tab
        """

        self.titleAddEdithField.setText("")
        self.tag1AddEditField.setText("")
        self.tag2AddEditField.setText("")
        self.display_notepadAddEdit.setPlainText("")


    def checkAddEditConditions(self):
        """
        check if any of obligatory fields isn't fulfilled
        :return: True if conditions are not fulfilled
        """
        if self.titleAddEdithField.text() == "":
            return True
        elif self.tag1AddEditField.text() == "":
            return True
        elif self.tag2AddEditField.text() == "":
            return True
        elif self.display_notepadAddEdit.toPlainText() == "":
            return True
        return False








def create_connection(db_file):
    """ create connection to sqlite database
        db_file - path to the database
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def create_table(conn, sql_create_table):
    """ create table with given SQL statement
        conn - connection object
        sql_create_table - SQL statement
    """
    try:
        c = conn.cursor()
        c.execute(sql_create_table)
    except Error as e:
        print(e)

def check_if_empty(conn):

    sql_sentence = """SELECT count(*) as total FROM settings"""

    c = conn.cursor()
    c.execute(sql_sentence)
    k = c.fetchone()

    if k[0] == 0:
        return True
    return False

def populate_settings(conn):
    sql_sentence = ''' INSERT INTO settings(stay_on_top,style,size)
                      VALUES(?,?,?) '''

    task = (False,1,1)

    cur = conn.cursor()
    cur.execute(sql_sentence, task)
    conn.commit()


def main():

    sql_create_table = """CREATE TABLE IF NOT EXISTS notes(
                            id integer PRIMARY KEY,
                            title text NOT NULL,
                            tag1 text NOT NULL,
                            tag2 text,
                            content text NOT NULL,
                            datetime text NOT NULL
                            );
                        """
    sql_create_settings = """CREATE TABLE IF NOT EXISTS settings(
                            id integer PRIMARY KEY,
                            stay_on_top integer,
                            style integer ,
                            size integer
                             );
                            """


    conn = create_connection("database.db")
    if conn is not None:
        create_table(conn,sql_create_table)
        create_table(conn,sql_create_settings)
        if check_if_empty(conn):
            populate_settings(conn)

    else:
        print("Error! Application couldn't run the database.")
    conn.close()
    app = QApplication([])
    window = MainWindow()
    window.show()
    window.raise_()
    app.exec_()





if __name__ == '__main__':
    main()




