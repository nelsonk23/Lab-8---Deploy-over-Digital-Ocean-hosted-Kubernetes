import sqlite3

# Database Schema
class Schema:
    def __init__(self):
        """Initialize and create tables if they don't exist"""
        self.conn = sqlite3.connect('todo.db')
        self.create_user_table()
        self.create_to_do_table()

    def __del__(self):
        """Commit changes and close connection when done"""
        self.conn.commit()
        self.conn.close()

    def create_to_do_table(self):
        """Creates the 'Todo' table"""
        query = """
        CREATE TABLE IF NOT EXISTS Todo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT NOT NULL,
            Description TEXT,
            _is_done BOOLEAN DEFAULT 0,
            _is_deleted BOOLEAN DEFAULT 0,
            CreatedOn DATE DEFAULT CURRENT_DATE,
            DueDate DATE,
            UserId INTEGER,
            FOREIGN KEY (UserId) REFERENCES User(_id)
        );
        """
        self.conn.execute(query)

    def create_user_table(self):
        """Creates the 'User' table"""
        query = """
        CREATE TABLE IF NOT EXISTS User (
            _id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Email TEXT,
            CreatedOn DATE DEFAULT CURRENT_DATE
        );
        """
        self.conn.execute(query)


# To-Do Model
class ToDoModel:
    TABLENAME = "Todo"

    def __init__(self):
        """Initialize the database connection"""
        self.conn = sqlite3.connect('todo.db')
        self.conn.row_factory = sqlite3.Row

    def __del__(self):
        """Commit changes and close connection when done"""
        self.conn.commit()
        self.conn.close()

    def get_by_id(self, _id):
        """Fetches a To-Do item by ID"""
        query = f"SELECT * FROM {self.TABLENAME} WHERE id=? AND _is_deleted=0"
        result = self.conn.execute(query, (_id,)).fetchone()
        return dict(result) if result else None

    def create(self, params):
        """Creates a new To-Do item"""
        query = f"""
        INSERT INTO {self.TABLENAME} (Title, Description, DueDate, UserId)
        VALUES (?, ?, ?, ?)
        """
        cursor = self.conn.execute(query, (
            params.get("Title"),
            params.get("Description"),
            params.get("DueDate"),
            params.get("UserId"),
        ))
        self.conn.commit()
        return self.get_by_id(cursor.lastrowid)

    def delete(self, item_id):
        """Soft deletes a To-Do item by setting _is_deleted to 1"""
        query = f"UPDATE {self.TABLENAME} SET _is_deleted = 1 WHERE id = ?"
        self.conn.execute(query, (item_id,))
        self.conn.commit()

    def update(self, item_id, update_dict):
        """Updates an existing To-Do item"""
        set_clause = ", ".join([f"{column} = ?" for column in update_dict.keys()])
        values = list(update_dict.values()) + [item_id]

        query = f"UPDATE {self.TABLENAME} SET {set_clause} WHERE id = ?"
        self.conn.execute(query, values)
        self.conn.commit()
        return self.get_by_id(item_id)

    def list_items(self):
        """Lists all non-deleted To-Do items"""
        query = f"SELECT * FROM {self.TABLENAME} WHERE _is_deleted = 0"
        result_set = self.conn.execute(query).fetchall()
        return [dict(row) for row in result_set]

