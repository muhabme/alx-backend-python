import sqlite3

class DatabaseConnection:
    """Custom context manager for database connections"""
    
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        """Enter the runtime context and return the cursor"""
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self.cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the runtime context and close the connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

# Example usage with the 'with' statement
if __name__ == "__main__":
    with DatabaseConnection('users.db') as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)