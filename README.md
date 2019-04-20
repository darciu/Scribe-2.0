# Scribe 2.0

## Brief description

Scribe is a useful application which allows to store text based notes with formatting. It uses sqlite3 database which is provided with Python installation. You don't need to configure anything before usage of the application.

## Prerequisites
This code was written in Python ver. 3.7.
For use, install PyQt5 ('pip install PyQt5').

## Start up

Run main_window.py in your IDE

## Features

Scribe 2.0 main features are:

- add notes,

- search and display notes (double click on list of results),

- edit notes,

- format text within notes,

Settings tab:

- stay on top (application's window stays over other windows),

- set style of application,

- set size of application,

Other:

-you can import records from other database by 'Import database' function. Other database must be in the same format as local,

## Search engine

Typing 'all' in search field there will be displayed all records.

## Executable version

1. Install pyinstaller. For this purpose you can use pip installer. Type 'pip install pyinstaller' in your Command Prompt.

2. Add new path to 'PATH' Environment Variable to C:\Python3.x\Scripts\ location. This depends on where your Python is installed.

3. Go to the folder where your python script is located in. Open command window in this folder (shift + right click).

4. Type in 'pyinstaller -w[python_script_name].

5. You can find executable file in folder 'dist'. In this case it will be named 'main_window.exe'. You can rename it and make Desktop shortcut.

## Author

Dariusz Giemza 2019