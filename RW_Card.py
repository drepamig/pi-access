from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep
import uuid
import MySQLdb


reader = SimpleMFRC522()

dbHost = "localhost"
dbName = "pi-access"
dbUser = "accessadmin"
dbPass = "accesspassword"


def add_user():
    name = input("What is the user's name?: ")
    is_admin = input("Is this user an Admin? (Y/N): ").upper().strip() == "Y"
    print("Place card to write...")
    reader.write(str(uuid.uuid4()).upper())
    _id, key = reader.read()
    dbConnection = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPass, db=dbName)
    cur = dbConnection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(
        f"INSERT INTO access_list SET name = '{name}', card_key = '{key.strip()}', card_id = '{_id}', access = 1, admin = {1 if is_admin else 0}"
    )
    dbConnection.commit()
    print("User added!")
    sleep(1)


def read_card():
    try:

        while True:
            try:
                print("Ready to read card...")
                _id, key = reader.read()
                print(f"ID:  {_id}")
                print(f"Key: {key}")
                print()
                sleep(1)
            except:
                break
    except:
        pass
    finally:
        GPIO.cleanup()


menu = ConsoleMenu("Door Access Control", "")

# Create some items
# Docs: https://github.com/aegirhall/console-menu
# MenuItem is the base class for all items, it doesn't do anything when selected
# menu_item = MenuItem("Add User")

# A FunctionItem runs a Python function when selected
menu.append_item(FunctionItem("Add User and Write Card", add_user))
menu.append_item(FunctionItem("Read Card", read_card))

# Finally, we call show to show the menu and allow the user to interact
menu.show()
