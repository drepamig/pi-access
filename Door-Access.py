import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep
from datetime import datetime
import MySQLdb
from typing import Type

# from cachetools import cached, TTLCache
import threading

# import threading
# import time

DOORPIN = 7
RELAY_TIMEOUT = 2
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(DOORPIN, GPIO.OUT)

dbHost = "localhost"
dbName = "pi-access"
dbUser = "accessadmin"
dbPass = "accesspassword"
dbExpireTime = 60  # minutes
dbRefreshInterval = 10 # minutes


reader = SimpleMFRC522()


class user_info:  # pylint: disable=too-few-public-methods
    """A wrapper for the returned SQL row for user access

    Attributes:
        name: A string representing the user's name.
        has_access: A bool representing the user's access.
        is_admin: A bool representing the user's admin status.
    """

    name = "UNKNOWN"
    has_access = False
    is_admin = False

    def __init__(self, results, card_key, card_id):
        db_row = None
        # results = db_cursor.fetchall()
        if (datetime.now() - results.last_refresh).seconds < (dbExpireTime * 60):
            for row in results.results:
                if row["card_key"] == card_key and row["card_id"] == str(card_id):
                    db_row = row
                    break
            if db_row is not None:
                # if db_cursor.rowcount != 1:
                #     print("WARNING: Multiple matches returned for: {card_id}, {card_key}")

                self.name: str = db_row["name"]
                self.has_access: bool = int(db_row["access"]) == 1
                self.is_admin: bool = int(db_row["admin"]) == 1
        self.card_key: str = card_key[:36] if len(card_key) > 36 else card_key
        self.card_id: int = card_id


class door:
    @staticmethod
    def open(timeout=RELAY_TIMEOUT):
        GPIO.output(DOORPIN, True)
        if timeout is not None:
            sleep(timeout)
            GPIO.output(DOORPIN, False)

    @staticmethod
    def close():
        GPIO.output(DOORPIN, False)


class _cachedDB:  # pylint: disable=too-few-public-methods

    results = None
    last_refresh = datetime(2000, 1, 1, 1, 1, 1)

    def __init__(self):
        threading.Thread(target=self.updateDB).start()

    def updateDB(self):
        while True:
            dbConnection = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPass, db=dbName)
            cur = dbConnection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(f"SELECT * FROM access_list")
            dbConnection.close()
            self.results = cur.fetchall()
            self.last_refresh = datetime.now()
            sleep(dbRefreshInterval * 60)


def ReaderAccess():
    # @cached(cache=TTLCache(maxsize=1024, ttl=3600))
    # def CheckAccess():
    #     dbConnection = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPass, db=dbName)
    #     cur = dbConnection.cursor(MySQLdb.cursors.DictCursor)
    #     cur.execute(f"SELECT * FROM access_list")
    #     dbConnection.close()
    #     return cur.fetchall()

    cachedDB = _cachedDB()

    def log_access(u: Type[user_info]):
        dbConnection = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPass, db=dbName)
        cur = dbConnection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(
            f"INSERT INTO access_log SET card_key_presented = '{u.card_key}', card_key_presented_datetime = NOW(), card_id_presented = '{u.card_id}', access_granted = '{1 if u.has_access else 0}', name_presented = '{u.name}'"
        )
        dbConnection.commit()
        pass

    door.close()

    while True:
        print("Waiting for key card...")
        card_id, card_key = reader.read()
        card_key = card_key.strip()
        u = user_info(cachedDB, card_key, card_id)

        if u.has_access:
            print(f"\tACCESS GRANTED for {u.name}")
            door.open()
        else:
            print("\tACCESS DENIED")
            sleep(RELAY_TIMEOUT)

        threading.Thread(target=log_access, args=[u]).start()

        # dbConnection.commit()


if __name__ == "__main__":
    try:
        ReaderAccess()
    except KeyboardInterrupt:
        print("Stopped because of Keyboard Inturrupt")
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
