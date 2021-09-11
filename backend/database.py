import sys
import uuid

sys.path.append('../../')
import sqlite3


def keygen():
    return str(uuid.uuid4())[:8]


class Database:
    def __init__(self):
        try:
            # connects to, or creates the file
            self.connection = sqlite3.connect("items.db")
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(e)

        # create the table if it doesnt exist
        with self.connection:
            self.cursor.execute("""
                Create table if not exists items (
                  post_id text primary key,
                  username text,
                  title text,
                  description text
                );

            """)

    def add_item(self, username, title, description):
        with self.connection:
            self.cursor.execute("insert into items(post_id, username, title, description) values (?,?,?,?)",
                                (keygen(), username, title, description))

    def get_all_items(self):
        self.cursor.execute("select * from items")
        items = self.cursor.fetchall()
        item_list = []
        for item in items:
            item_list.append({'post_id': item[0], 'username': item[1], 'title': item[2], 'description': item[3]})
        return item_list

    def get_item(self, post_id):
        try:
            self.cursor.execute("select post_id, username, title, description from items where post_id=?", (post_id,))
        except Exception as e:
            print(e)
        else:
            try:
                note = self.cursor.fetchall()[0]
            except Exception as e:
                print(e)
            else:
                note_dict = {'post_id': note[0], 'username': note[1], 'title': note[2], 'description': note[3]}
                return note_dict

    def delete_item(self, post_id):
        with self.connection:
            self.cursor.execute("DELETE FROM items where post_id=?", (post_id,))

    def close_conn(self):
        self.connection.close()
