import sqlite3 as lite
import sys


def read_image(filename):
    try:
        fin = open(filename, "rb")
        img = fin.read()
        return img
    finally:
        if fin:
            fin.close()


try:
    con = lite.connect('db/blogs.db')
    cur = con.cursor()
    data = read_image("img.png")
    binary = lite.Binary(data)
    cur.execute("INSERT INTO Images(Data) VALUES (?)", (binary,))
    con.commit()

finally:
    if con:
        con.close()

