import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import mariadb
import sqlite3
import cx_Oracle
import psycopg2

class DatabaseManager:
    def __init__(self, db_type, **kwargs):
        self.db_type = db_type
        self.connection = self.connect_to_database(**kwargs)

    def connect_to_database(self, **kwargs):
        if self.db_type == 'mysql':
            return mysql.connector.connect(**kwargs)
        elif self.db_type == 'mariadb':
            return mariadb.connect(**kwargs)
        elif self.db_type == 'sqlite':
            return sqlite3.connect(kwargs['database'])
        elif self.db_type == 'oracle':
            dsn = cx_Oracle.makedsn(kwargs['host'], kwargs['port'], service_name=kwargs['service_name'])
            return cx_Oracle.connect(user=kwargs['user'], password=kwargs['password'], dsn=dsn)
        elif self.db_type == 'postgresql':
            return psycopg2.connect(**kwargs)
        else:
            raise ValueError("Unsupported database type")

    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        cursor.execute(query, params or ())
        if query.strip().lower().startswith("select"):
            return cursor.fetchall()
        else:
            self.connection.commit()

    def close(self):
        self.connection.close()

class DatabaseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Manager")
        self.db_manager = None

        # Create UI components
        self.create_widgets()

    def create_widgets(self):
        # Database type selection
        self.db_type_label = ttk.Label(self.root, text="Database Type:")
        self.db_type_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        
        self.db_type_var = tk.StringVar()
        self.db_type_combo = ttk.Combobox(self.root, textvariable=self.db_type_var)
        self.db_type_combo['values'] = ("mysql", "mariadb", "sqlite", "oracle", "postgresql")
        self.db_type_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Host
        self.host_label = ttk.Label(self.root, text="Host:")
        self.host_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.host_entry = ttk.Entry(self.root)
        self.host_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # User
        self.user_label = ttk.Label(self.root, text="User:")
        self.user_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.user_entry = ttk.Entry(self.root)
        self.user_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Password
        self.password_label = ttk.Label(self.root, text="Password:")
        self.password_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.password_entry = ttk.Entry(self.root, show="*")
        self.password_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Database
        self.database_label = ttk.Label(self.root, text="Database:")
        self.database_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.database_entry = ttk.Entry(self.root)
        self.database_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Service Name (for Oracle)
        self.service_name_label = ttk.Label(self.root, text="Service Name (Oracle):")
        self.service_name_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.service_name_entry = ttk.Entry(self.root)
        self.service_name_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        # Port
        self.port_label = ttk.Label(self.root, text="Port:")
        self.port_label.grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.port_entry = ttk.Entry(self.root)
        self.port_entry.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        # Connect button
        self.connect_button = ttk.Button(self.root, text="Connect", command=self.connect_to_database)
        self.connect_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        # Query entry
        self.query_label = ttk.Label(self.root, text="SQL Query:")
        self.query_label.grid(row=8, column=0, padx=5, pady=5, sticky="e")
        self.query_entry = ttk.Entry(self.root, width=50)
        self.query_entry.grid(row=8, column=1, padx=5, pady=5, sticky="w")

        # Execute button
        self.execute_button = ttk.Button(self.root, text="Execute", command=self.execute_query)
        self.execute_button.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

        # Query results
        self.results_text = tk.Text(self.root, height=10, width=70)
        self.results_text.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

    def connect_to_database(self):
        db_type = self.db_type_var.get()
        host = self.host_entry.get()
        user = self.user_entry.get()
        password = self.password_entry.get()
        database = self.database_entry.get()
        service_name = self.service_name_entry.get()
        port = self.port_entry.get()

        try:
            if db_type in ['mysql', 'mariadb', 'postgresql']:
                self.db_manager = DatabaseManager(db_type, host=host, user=user, password=password, database=database, port=int(port))
            elif db_type == 'sqlite':
                self.db_manager = DatabaseManager(db_type, database=database)
            elif db_type == 'oracle':
                self.db_manager = DatabaseManager(db_type, host=host, user=user, password=password, service_name=service_name, port=int(port))
            else:
                raise ValueError("Unsupported database type")
            messagebox.showinfo("Connection", "Connected to database successfully")
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))

    def execute_query(self):
        query = self.query_entry.get()
        if self.db_manager:
            try:
                results = self.db_manager.execute_query(query)
                self.results_text.delete(1.0, tk.END)
                for row in results:
                    self.results_text.insert(tk.END, str(row) + "\n")
            except Exception as e:
                messagebox.showerror("Query Error", str(e))
        else:
            messagebox.showerror("Connection Error", "Not connected to any database")

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseGUI(root)
    root.mainloop()
