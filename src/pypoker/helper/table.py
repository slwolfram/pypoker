import sqlite3


class Table(object):
    def __init__(self, id, table_name, num_seats, min_buyin, max_buyin, sb, bb):
        self.id = id
        self.table_name = table_name
        self.num_seats = num_seats
        self.min_buyin = min_buyin
        self.max_buyin = max_buyin
        self.small_blind = sb
        self.big_blind = bb
        self.disabled = False


    def asdict(self):
        return {
            'id': self.id,
            'table_name': self.table_name,
            'num_seats': self.num_seats,
            'min_buyin': self.min_buyin,
            'max_buyin': self.max_buyin,
            'small_blind': self.small_blind,
            'big_blind': self.big_blind,
            'disabled': self.disabled
        }


    @classmethod
    def find_by_id(cls, id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM tables WHERE id=?"
        result = cursor.execute(query, (id,))
        row = result.fetchone()
        if row:
            table = Table(row[0], row[1], row[2],
                          row[3], row[4], row[5], row[6])
        else:
            table = None
        connection.commit()
        connection.close()
        return table


    @classmethod
    def find_all_enabled(cls):
        tables = []
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM tables WHERE disabled=?"
        try:
            result = cursor.execute(query, (False,))
            data = result.fetchall()
            for row in data:
                tables.append(
                    Table(row[0], row[1], row[2],
                          row[3], row[4], row[5], row[6]))
        except sqlite3.OperationalError:
            print("Table 'tables' does not exist yet.")
        connection.commit()
        connection.close()
        return tables


    @classmethod
    def find_all(cls):
        tables = []
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM tables"
        try:
            result = cursor.execute(query, (False,))
            data = result.fetchall()
            for row in data:
                tables.append(
                    Table(row[0], row[1], row[2],
                          row[3], row[4], row[5], row[6]))
        except sqlite3.OperationalError:
            print("Table 'tables' does not exist yet.")
        connection.commit()
        connection.close()
        return tables
