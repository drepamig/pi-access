import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep
import MySQLdb
from typing import Type

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

    def __init__(self, db_cursor, card_key, card_id):
        if db_cursor.rowcount != 0:
            if db_cursor.rowcount != 1:
                print("WARNING: Multiple matches returned for: {card_id}, {card_key}")
            db_row = db_cursor.fetchone()
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


def ReaderAccess():
    def log_access(u: Type[user_info]):
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
        dbConnection = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPass, db=dbName)
        cur = dbConnection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(f"SELECT * FROM access_list WHERE card_key = '{card_key}' and card_id = '{card_id}'")
        u = user_info(cur, card_key, card_id)
        log_access(u)
        dbConnection.close()

        if u.has_access:
            print(f"\tACCESS GRANTED for {u.name}")
            door.open()
        else:
            print("\tACCESS DENIED")
            sleep(RELAY_TIMEOUT)

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