import datetime
import sys
import calendar

from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtSql import QSqlTableModel
from PySide6.QtCore import Qt

from view.view import Ui_MainWindow
from view.edit_budget import Ui_Dialog

from bookkeeper.repository.sqlite_repository import SqliteRepository

################################################################################


class ExpenseTracker(QMainWindow):
    def __init__(self):
        super(ExpenseTracker, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        ################################################################################
        self.conf = SqliteRepository()
        ################################################################################
        self.view_data()
        self.view_data_2()
        ################################################################################
        self.ui.pushButton_4.clicked.connect(self.delete_drop_table_budget)
        self.ui.pushButton_3.clicked.connect(self.delete_current_transaction)
        self.ui.pushButton_2.clicked.connect(self.open_new_transaction_window)
        self.ui.pushButton.clicked.connect(self.add_new_transaction)
        ################################################################################


    ################################################################################
    def add_new_transaction(self):
        summa = int(self.ui.lineEdit.text())
        date = str(datetime.date.today())
        category = self.ui.comboBox.currentText()
        comment = self.ui.textEdit.toPlainText()
        self.conf.add_new_transaction_query(date, summa, category, comment)
        self.view_data()
        self.view_data_2()
        self.updateBudget()

    def add_new_transaction_1(self):
        Day = "День"
        Summa = 0
        Budget = self.ui_window.lineEdit.text()
        self.conf.add_new_transaction_query1(Budget, Day, Summa)
        self.view_data_2()

    def add_new_transaction_2(self):
        Day = "Неделя"
        Summa = 0
        Budget = self.ui_window.lineEdit_2.text()
        self.conf.add_new_transaction_query1(Budget, Day, Summa)
        self.view_data_2()

    def add_new_transaction_3(self):
        Day = "Месяц"
        Summa = 0
        Budget = self.ui_window.lineEdit_3.text()
        self.conf.add_new_transaction_query1(Budget, Day, Summa)
        self.view_data_2()

    ################################################################################

    ################################################################################

    def view_data(self):
        self.model = QSqlTableModel(self)
        self.model.setQuery('SELECT id,date,summa,category,comment FROM expenses')
        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "Дата")
        self.model.setHeaderData(2, Qt.Horizontal, "Сумма")
        self.model.setHeaderData(3, Qt.Horizontal, "Категория")
        self.model.setHeaderData(4, Qt.Horizontal, "Комментарий")
        self.model.select()
        self.ui.tableView_2.setModel(self.model)
        self.ui.tableView_2.setColumnWidth(0, 10)
        self.ui.tableView_2.setColumnWidth(4, 190)

        # Обновление бюджета (день, неделя)
        self.updateBudget()

    def view_data_2(self):
        self.model = QSqlTableModel(self)
        self.model.setQuery(
            'SELECT day,summa,budget FROM expenses1')
        self.model.setHeaderData(0, Qt.Horizontal, " ")
        self.model.setHeaderData(1, Qt.Horizontal, "Сумма")
        self.model.setHeaderData(2, Qt.Horizontal, "Бюджет")
        self.model.select()
        self.ui.tableView.setModel(self.model)
        self.ui.tableView.setColumnWidth(1, 211)
        self.ui.tableView.setColumnWidth(2, 211)

    ################################################################################

    ################################################################################
    def delete_current_transaction(self):
        index = self.ui.tableView_2.selectedIndexes()[0]
        id = str(self.ui.tableView_2.model().data(index))
        self.conf.delete_transaction_query(id)
        self.view_data()
        self.view_data_2()

    def delete_drop_table_budget(self):
        self.conf.drop_table_budget()
        self.view_data()
        self.view_data_2()

    ################################################################################

    ################################################################################
    def open_new_transaction_window(self):
        self.new_window = QtWidgets.QDialog()
        self.ui_window = Ui_Dialog()
        self.ui_window.setupUi(self.new_window)
        self.new_window.show()
        self.ui_window.pushButton.clicked.connect(self.add_new_transaction_1)
        self.ui_window.pushButton_2.clicked.connect(self.add_new_transaction_2)
        self.ui_window.pushButton_3.clicked.connect(self.add_new_transaction_3)
    ################################################################################

    def updateBudget(self):
        summa_day = self.conf.total_date_day()
        self.conf.update_transaction_query(summa_day, 1)
        summa_month = self.conf.total_balance()
        self.conf.update_transaction_query(summa_day, 3)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpenseTracker()
    window.show()

    sys.exit(app.exec())
