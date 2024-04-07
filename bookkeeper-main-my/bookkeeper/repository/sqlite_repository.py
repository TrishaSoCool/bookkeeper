from PySide6 import QtWidgets, QtSql
import datetime

class SqliteRepository:

    def __init__(self):
        super(SqliteRepository, self).__init__()
        self.create_connection()
        self.date = str(datetime.date.today())

    def create_connection(self):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('expense_db.db')
        if not db.open():
            QtWidgets.QMessageBox.critical(None, "Cannot open database",
                                           "Click Cancel to exit.", QtWidgets.QMessageBox.Cancel)
            return False
        query = QtSql.QSqlQuery()
        query.exec("CREATE TABLE IF NOT EXISTS expenses (ID integer primary key AUTOINCREMENT, Date VARCHAR(20), "
                   "Category VARCHAR(20), Comment VARCHAR(20), Summa REAL)")
        query.exec("CREATE TABLE IF NOT EXISTS expenses1 (ID integer primary key AUTOINCREMENT,"
                   "Budget VARCHAR(20), Summa REAL, Day VARCHAR(20))")
        return True

    def execute_query_with_params(self, sql_query, query_values=None):
        query = QtSql.QSqlQuery()
        query.prepare(sql_query)
        if query_values is not None:
            for query_value in query_values:
                query.addBindValue(query_value)
        query.exec()
        return query

    def add_new_transaction_query(self,date,summa,category,comment):
        sql_query = "INSERT INTO expenses (Date,Summa,Category,Comment) VALUES (?,?,?,?)"
        self.execute_query_with_params(sql_query, [date,summa,category,comment])

    def add_new_transaction_query1(self,budget,day,summa):
        sql_query = "INSERT INTO expenses1 (Budget,Day,Summa) VALUES (?,?,?)"
        self.execute_query_with_params(sql_query, [budget,day,summa])

    def add_new_transaction_query2(self,summa):
        sql_query = "INSERT INTO expenses1 (Summa) VALUES (?)"
        self.execute_query_with_params(sql_query, [summa])

    def delete_transaction_query(self, id):
        sql_query = "DELETE FROM expenses WHERE ID=?"
        self.execute_query_with_params(sql_query, [id])

    def drop_table_budget(self):
        sql_query = "DROP TABLE expenses1"
        self.execute_query_with_params(sql_query)
        self.create_connection()

    def update_transaction_query(self,summa,id):
        sql_query = "UPDATE expenses1 SET Summa=? WHERE ID=?"
        self.execute_query_with_params(sql_query, [summa, id])

    def get_total(self, column, filter=None, value=None):
        sql_query = f"SELECT SUM({column}) FROM expenses"
        if filter is not None and value is not None:
            sql_query += f" WHERE {filter} = ?"
        query_values = []
        if value is not None:
            query_values.append(value)
        query = self.execute_query_with_params(sql_query, query_values)
        if query.next():
            return str(query.value(0)) + ' '
        return '0'

    def total_balance(self):
        return self.get_total(column="Summa")

    def total_date_day(self):
        return self.get_total(column="Summa", filter="Date", value=self.date)
