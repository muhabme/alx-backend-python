import sqlite3

class ExecuteQuery:
    def __init__(self, query, params=()):
        self.query = query
        self.params = params
    
    def __enter__(self):
        self.conn = sqlite3.connect('users.db')
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        self.results = cursor.fetchall()
        return self.results
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

# Example usage
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    with ExecuteQuery(query, (25,)) as results:
        print(results)