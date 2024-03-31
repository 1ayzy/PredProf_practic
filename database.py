import sqlite3 as sql
import logging
import main


class DatabaseOperations():
    def __log(self, message: str) -> None:
        logging.getLogger(__name__).info(message)

    def __getConnectionAndCursor(self, name: str) -> (sql.Connection, sql.Cursor):
        connection = sql.connect(name)
        cursor = connection.cursor()

        self.__log(f"Created (sql.Connection and sql.Cursor) with db name {name}")

        return (connection, cursor)

    def __closeConnection(self, connection: sql.Connection) -> None:
        connection.commit()
        connection.close()

    def createAllDatesDatabase(self) -> None:
        connection, cursor = self.__getConnectionAndCursor('AllDates.db')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS AllDates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT
        )
        ''')

        self.__closeConnection(connection)

        self.__log(f"Created AllDates table")

    def createDateInfoDatabase(self) -> None:
        connection, cursor = self.__getConnectionAndCursor('DateInfo.db')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS DateInfo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT
        )
        ''')

        self.__closeConnection(connection)

        self.__log(f"Created DateInfo table")

    def addDates(self, message) -> None:
        connection, cursor = self.__getConnectionAndCursor('AllDates.db')

        cursor.execute('INSERT INTO AllDates (message) VALUES (?)', (f"{message}",))

        self.__closeConnection(connection)

        self.__log(f"Inserted {message} to AllDates")

    def addDateInfo(self, message) -> None:
        connection, cursor = self.__getConnectionAndCursor('DateInfo.db')

        cursor.execute('INSERT INTO DateInfo (message) VALUES (?)', (f"{message}",))

        self.__closeConnection(connection)

        self.__log(f"Inserted {message} to DateInfo")

    def fetchAllDates(self) -> None:
        connection, cursor = self.__getConnectionAndCursor('AllDates.db')

        cursor.execute('SELECT * FROM AllDates')
        allDates = cursor.fetchall()

        for date in allDates:
            print(date)

        self.__closeConnection(connection)

    def fetchAllDateInfos(self) -> None:
        connection, cursor = self.__getConnectionAndCursor('DateInfo.db')

        cursor.execute('SELECT * FROM DateInfo')
        dateInfos = cursor.fetchall()

        for dateInfo in dateInfos:
            print(dateInfo)

        self.__closeConnection(connection)


#USAGE
# DatabaseOperations().createAllDatesDatabase()
# DatabaseOperations().createDateInfoDatabase()
#
# DatabaseOperations().addDates(["1", "2", "3"])
# DatabaseOperations().addDateInfo(main.get_date_info('25-01-23').json())
#
# DatabaseOperations().fetchAllDates()
# DatabaseOperations().fetchAllDateInfos()