import sqlite3

DB_NAME = 'todo.db'

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_table():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0
            )
        ''')
        conn.commit()

def add_task(title):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('INSERT INTO todos (title, done) VALUES (?, 0)', (title,))
        conn.commit()

def delete_task(task_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('DELETE FROM todos WHERE id = ?', (task_id,))
        conn.commit()

def update_task_status(task_id, done):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('UPDATE todos SET done = ? WHERE id = ?', (done, task_id))
        conn.commit()

def get_all_tasks():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT id, title, done FROM todos')
        return c.fetchall() 