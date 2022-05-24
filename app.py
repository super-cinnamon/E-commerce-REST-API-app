from glob import glob
from PyQt5 import QtWidgets, uic, QtGui,QtCore
import sys
import requests

from test import BASE

class Ui(QtWidgets.QMainWindow):
    BASE = "http://127.0.0.1:5000/"
    global listOfProducts
    global selectedProduct
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('mainWindow.ui', self)

        #the list of products
        self.product_list = self.findChild(QtWidgets.QListView,"product_list")
        self.product_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.listModel = QtGui.QStandardItemModel()
        self.product_list.setModel(self.listModel)
        self.product_list.clicked[QtCore.QModelIndex].connect(self.openSelectedClickListener)
        self.getAllProduct()
        
        #product image
        self.product_image=self.findChild(QtWidgets.QLabel,"product_image")
        self.product_image.setPixmap(QtGui.QPixmap("./images/10.png"))

        #description of the product
        self.product_desc=self.findChild(QtWidgets.QTextEdit,"product_desc")
        self.product_desc.setReadOnly(True)

        #the name of the product
        self.product_name = self.findChild(QtWidgets.QLabel,"product_name")
        
        #id of the bidder
        self.bidder_id = self.findChild(QtWidgets.QTextEdit,"bidder_id")
        
        #name of the bidder
        self.bidder_name = self.findChild(QtWidgets.QTextEdit,"bidder_name")
        
        #the suggested price 
        self.bidder_price = self.findChild(QtWidgets.QSpinBox,"bidder_price")
        
        #button to validate the bid
        self.bid_validation = self.findChild(QtWidgets.QPushButton,"bid_validation")

        #liste of bidders
        self.bidders_list = self.findChild(QtWidgets.QTableView,"bidders_list")

        self.show()

    def openSelectedClickListener(self, index):
        global listOfProducts
        global selectedProduct
        item = self.listModel.itemFromIndex(index)
        self.product_name.setText(item.text())
        keys = [k for k, v in listOfProducts.items() if v == item.text()]
        response = requests.get(BASE + f"auction/{keys[0]}", {})
        selectedProduct=response.json()
        self.product_desc.setText(selectedProduct[f'{keys[0]}']["Description"])
        self.product_image.setPixmap(QtGui.QPixmap(f"./images/{keys[0]}.png"))
        

    def getAllProduct(self):
        global listOfProducts
        response = requests.get(BASE + "auction/0", {})
        listOfProducts=response.json()
        i=1
        while i <=len(listOfProducts):
            item = QtGui.QStandardItem(listOfProducts[f'{i}'])
            self.listModel.appendRow(item)
            i+=1


    



app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()