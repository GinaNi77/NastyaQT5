import sys
from PyQt5 import QtWidgets, QtSql
from getpass import getpass
from mysql.connector import connect, Error
from PyQt5.QtWidgets import QDialog, QApplication
import menu, w_create_db, w_create_transaction, w_customer, w_products, w_sales, w_transactions, w_full_transaction
import config, db_table, db_triggers, db_procedures
from datetime import date

class Main(QtWidgets.QMainWindow, menu.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init()

    def w_create_db(self):
        self.w_create_db = WCreateDB()
        self.w_create_db.show()
        self.hide()

    def w_create_transaction(self):
        self.w_create_transaction = WCreateTransaction()
        self.w_create_transaction.show()
        self.hide()

    def w_customer(self):
        self.w_customer = WCustomer()
        self.w_customer.show()
        self.hide()

    def w_product(self):
        self.w_product = WProduct()
        self.w_product.show()
        self.hide()

    def w_sale(self):
        self.w_sale = WSale()
        self.w_sale.show()
        self.hide()

    def init(self):
        #назначаем действия по кнопкам
        self.pushButton_5.clicked.connect(self.w_create_db)
        self.pushButton_4.clicked.connect(self.w_create_transaction)
        self.pushButton.clicked.connect(self.w_customer)
        self.pushButton_2.clicked.connect(self.w_product)
        self.pushButton_3.clicked.connect(self.w_sale)

class WCreateDB(QtWidgets.QMainWindow, w_create_db.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init()

    def init(self):
        #назначаем действия по кнопкам
        self.pushButton_4.clicked.connect(self.back)
        self.pushButton.clicked.connect(self.create_table)
        self.pushButton_2.clicked.connect(self.create_triggers)
        self.pushButton_3.clicked.connect(self.create_procedures)

    def back(self):
        self.createDB = Main()
        self.createDB.show()
        self.hide()

    def create_table(self):
        with connect(
                host="localhost",
                user=config.user,
                password=config.password,
        ) as connection:
            query = db_table.script
            with connection.cursor() as cursor:
                cursor.execute(query)

    def create_triggers(self):
        with connect(
                host="localhost",
                user=config.user,
                password=config.password,
                database = config.db,
        ) as connection:
            query = db_triggers.triggers
            with connection.cursor() as cursor:
                cursor.execute(query)

    def create_procedures(self):
        with connect(
                host="localhost",
                user=config.user,
                password=config.password,
                database = config.db,
        ) as connection:
            query = db_procedures.procedures
            with connection.cursor() as cursor:
                cursor.execute(query)

class WCreateTransaction(QtWidgets.QMainWindow, w_create_transaction.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init()

    def w_transactions(self):
        self.w_transactions = WTransactions()
        self.w_transactions.show()
        self.hide()

    def w_full_transaction(self):
        self.w_full_transaction = WFullTransaction()
        self.w_full_transaction.show()
        self.hide()

    def init(self):
        #назначаем действия по кнопкам
        self.pushButton_4.clicked.connect(self.back)
        self.pushButton_2.clicked.connect(self.w_transactions)
        self.pushButton.clicked.connect(self.w_full_transaction)

    def back(self):
        self.driver = Main()
        self.driver.show()
        self.hide()

class WCustomer(QtWidgets.QMainWindow, w_customer.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init()
        self.showdb()

    def init(self):
        #назначаем действия по кнопкам
        self.pushButton_4.clicked.connect(self.back)
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.delete)

    def back(self):
        self.driver = Main()
        self.driver.show()
        self.hide()

    def showdb(self):
        with connect(
                        host="localhost",
                        user=config.user,
                        password=config.password,
                        database=config.db,
                    ) as connection:
                        select_query = "select * from customers"
                        with connection.cursor() as cursor:
                            cursor.execute(select_query)
                            result = cursor.fetchall()
                            self.tableWidget.setRowCount(len(result))
                            b = list()
                            for row in result:
                                for i in row:
                                    b.append(i)

                            k = 0
                            for j in range(0, len(result)):
                                for i in range(0, 5):
                                    self.tableWidget.setItem(j, i, QtWidgets.QTableWidgetItem(str(b[k])))
                                    k += 1

    def add(self):
        nameCustomer = self.lineEdit.text()
        surnameCustomer = self.lineEdit_3.text()
        address = self.lineEdit_4.text()
        phone = self.lineEdit_5.text()
        with connect(
                host="localhost",
                user=config.user,
                password=config.password,
                database=config.db,
            ) as connection:
                insert_query = "INSERT INTO customers (nameCustomer, surnameCustomer, address, phone) VALUES (%s, %s, %s, %s)"
                insert_tuple = [(nameCustomer, surnameCustomer, address, phone)]
                with connection.cursor() as cursor:
                    cursor.execute(insert_query, insert_tuple[0])
                    connection.commit()
        
                    self.lineEdit.setText("")
                    self.lineEdit_3.setText("")
                    self.lineEdit_4.setText("")
                    self.lineEdit_5.setText("")
                    self.showdb()

    def delete(self):
        id = self.lineEdit_2.text()
        with connect(
                host="localhost",
                user=config.user,
                password=config.password,
                database=config.db,
        ) as connection:
            delete_query = "DELETE from customers where idCustomer = %s"
            delete_tuple = [(id,)]
            with connection.cursor() as cursor:
                cursor.execute(delete_query, delete_tuple[0])
                connection.commit()
        
                self.lineEdit_2.setText("")
                self.showdb()   

class WProduct(QtWidgets.QMainWindow, w_products.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init()
        self.showdb()

    def showdb(self):
        with connect(
                host="localhost",
                user=config.user,
                password=config.password,
                database=config.db,
            ) as connection:
                select_query = "select * from products"
                with connection.cursor() as cursor:
                    cursor.execute(select_query)
                    result = cursor.fetchall()
                    self.tableWidget.setRowCount(len(result))
                    b = list()
                    for row in result:
                        for i in row:
                            b.append(i)

                    k = 0
                    for j in range(0, len(result)):
                        for i in range(0, 4):
                            self.tableWidget.setItem(j, i, QtWidgets.QTableWidgetItem(str(b[k])))
                            k += 1        

    def init(self):
        #назначаем действия по кнопкам
        self.pushButton_4.clicked.connect(self.back)
        self.pushButton_2.clicked.connect(self.delete)
        self.pushButton.clicked.connect(self.add)

    def add(self):
        nameProduct = self.lineEdit.text()
        descriptionProduct = self.lineEdit_3.text()
        price = self.lineEdit_4.text()
        with connect(
                host="localhost",
                user=config.user,
                password=config.password,
                database=config.db,
            ) as connection:
                insert_query = "INSERT INTO products (nameProduct, descriptionProduct, price) VALUES (%s, %s, %s)"
                insert_tuple = [(nameProduct, descriptionProduct, price)]
                with connection.cursor() as cursor:
                    cursor.execute(insert_query, insert_tuple[0])
                    connection.commit()
        
                    self.lineEdit.setText("")
                    self.lineEdit_3.setText("")
                    self.lineEdit_4.setText("")
                    self.showdb()

    def delete(self):
        id = self.lineEdit_2.text()
        with connect(
                host="localhost",
                user=config.user,
                password=config.password,
                database=config.db,
        ) as connection:
            delete_query = "DELETE from products where idProduct = %s"
            delete_tuple = [(id,)]
            with connection.cursor() as cursor:
                cursor.execute(delete_query, delete_tuple[0])
                connection.commit()
        
                self.lineEdit_2.setText("")
                self.showdb()

    def back(self):
        self.driver = Main()
        self.driver.show()
        self.hide()

class WSale(QtWidgets.QMainWindow, w_sales.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init()
        self.showdb()

    def showdb(self):
        with connect(
                host="localhost",
                user=config.user,
                password=config.password,
                database=config.db,
            ) as connection:
                select_query = "select * from sales"
                with connection.cursor() as cursor:
                    cursor.execute(select_query)
                    result = cursor.fetchall()
                    self.tableWidget.setRowCount(len(result))
                    b = list()
                    for row in result:
                        for i in row:
                            b.append(i)

                    k = 0
                    for j in range(0, len(result)):
                        for i in range(0, 2):
                            self.tableWidget.setItem(j, i, QtWidgets.QTableWidgetItem(str(b[k])))
                            k += 1

    def init(self):
        #назначаем действия по кнопкам
        self.pushButton_4.clicked.connect(self.back)

    def back(self):
        self.driver = Main()
        self.driver.show()
        self.hide()

class WTransactions(QtWidgets.QMainWindow, w_transactions.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init()
        self.showdb()

    def showdb(self):
        with connect(
                host="localhost",
                user=config.user,
                password=config.password,
                database=config.db,
            ) as connection:
                select_query = "select * from transactions"
                with connection.cursor() as cursor:
                    cursor.execute(select_query)
                    result = cursor.fetchall()
                    self.tableWidget.setRowCount(len(result))
                    b = list()
                    for row in result:
                        for i in row:
                            b.append(i)

                    k = 0
                    for j in range(0, len(result)):
                        for i in range(0, 7):
                            self.tableWidget.setItem(j, i, QtWidgets.QTableWidgetItem(str(b[k])))
                            k += 1
    
    def init(self):
        #назначаем действия по кнопкам
        self.pushButton_4.clicked.connect(self.back)
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.delete)
        self.pushButton_5.clicked.connect(self.saleId)
        self.pushButton_6.clicked.connect(self.sum_w_sale)

    def saleId(self):
        with connect(
                host="localhost",
                user=config.user,
                password=config.password,
                database=config.db,
        ) as connection:
            select_query = "call update_sales()"
            with connection.cursor() as cursor:
                cursor.execute(select_query)
                connection.commit()
                self.showdb()

    def sum_w_sale(self):
        with connect(
                host="localhost",
                user=config.user,
                password=config.password,
                database=config.db,
        ) as connection:
            select_query = "call CalculateDiscountedSumProcedure()"
            with connection.cursor() as cursor:
                cursor.execute(select_query)
                connection.commit()
                self.showdb()

    def add(self):
        idFull_transaction = self.lineEdit.text()
        idProduct = self.lineEdit_3.text()
        amount = self.lineEdit_4.text()
        with connect(
                host="localhost",
                user=config.user,
                password=config.password,
                database=config.db,
            ) as connection:
                insert_query = "INSERT INTO transactions (idFull_transaction, idProduct, amount) VALUES (%s, %s, %s)"
                insert_tuple = [(idFull_transaction, idProduct, amount)]
                with connection.cursor() as cursor:
                    cursor.execute(insert_query, insert_tuple[0])
                    connection.commit()
        
                    self.lineEdit.setText("")
                    self.lineEdit_3.setText("")
                    self.lineEdit_4.setText("")
                    self.showdb()

    def delete(self):
        id = self.lineEdit_2.text()
        with connect(
                host="localhost",
                user=config.user,
                password=config.password,
                database=config.db,
        ) as connection:
            delete_query = "DELETE from transactions where idTransaction = %s"
            delete_tuple = [(id,)]
            with connection.cursor() as cursor:
                cursor.execute(delete_query, delete_tuple[0])
                connection.commit()
        
                self.lineEdit_2.setText("")
                self.showdb()

    def back(self):
        self.driver = WCreateTransaction()
        self.driver.show()
        self.hide()

class WFullTransaction(QtWidgets.QMainWindow, w_full_transaction.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init()
        self.showdb()

    def showdb(self):
        with connect(
                host="localhost",
                user=config.user,
                password=config.password,
                database=config.db,
            ) as connection:
                select_query = "select * from full_transaction"
                with connection.cursor() as cursor:
                    cursor.execute(select_query)
                    result = cursor.fetchall()
                    self.tableWidget.setRowCount(len(result))
                    b = list()
                    for row in result:
                        for i in row:
                            b.append(i)

                    k = 0
                    for j in range(0, len(result)):
                        for i in range(0, 4):
                            self.tableWidget.setItem(j, i, QtWidgets.QTableWidgetItem(str(b[k])))
                            k += 1

    def full_transaction_sum(self):
        with connect(
                host="localhost",
                user=config.user,
                password=config.password,
                database=config.db,
        ) as connection:
            select_query = "call CalculateFullTransactionSum()"
            with connection.cursor() as cursor:
                cursor.execute(select_query)
                connection.commit()
                self.showdb()

    def add(self):
        idCustomer = self.lineEdit.text()
        today = date.today()
        with connect(
                host="localhost",
                user=config.user,
                password=config.password,
                database=config.db,
            ) as connection:
                insert_query = "INSERT INTO full_transaction (idCustomer, date) VALUES (%s, %s)"
                insert_tuple = [(idCustomer, today)]
                with connection.cursor() as cursor:
                    cursor.execute(insert_query, insert_tuple[0])
                    connection.commit()
        
                    self.lineEdit.setText("")
                    self.showdb()

    def delete(self):
        id = self.lineEdit_2.text()
        with connect(
                host="localhost",
                user=config.user,
                password=config.password,
                database=config.db,
        ) as connection:
            delete_query = "DELETE from full_transaction where idFull_transaction = %s"
            delete_tuple = [(id,)]
            with connection.cursor() as cursor:
                cursor.execute(delete_query, delete_tuple[0])
                connection.commit()
        
                self.lineEdit_2.setText("")
                self.showdb()

    def init(self):
        #назначаем действия по кнопкам
        self.pushButton_4.clicked.connect(self.back)
        self.pushButton_2.clicked.connect(self.delete)
        self.pushButton.clicked.connect(self.add)
        self.pushButton_5.clicked.connect(self.full_transaction_sum)

    def back(self):
        self.driver = WCreateTransaction()
        self.driver.show()
        self.hide()


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.show()
    app.exec_()

if __name__ == '__main__':
    main()
