from glob import glob
from PyQt5 import QtWidgets, uic, QtGui,QtCore
import sys
import requests
from sqlalchemy import false

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

        #prix estimé
        self.prix_estime=self.findChild(QtWidgets.QLabel,"prix_estime")
        self.prix_estime.setFont(QtGui.QFont('Arial', 9))

        #description of the product
        self.product_desc=self.findChild(QtWidgets.QTextEdit,"product_desc")
        self.product_desc.setReadOnly(True)
        self.product_desc.setFont(QtGui.QFont('Arial', 10))

        #the name of the product
        self.product_name = self.findChild(QtWidgets.QLabel,"product_name")
        self.product_name.setFont(QtGui.QFont('Arial', 10))
        self.product_name.setStyleSheet("font-weight: bold")
        
        #id of the bidder
        self.bidder_id = self.findChild(QtWidgets.QTextEdit,"bidder_id")
        self.bidder_id.setFont(QtGui.QFont('Arial', 10))
        
        #name of the bidder
        self.bidder_name = self.findChild(QtWidgets.QTextEdit,"bidder_name")
        self.bidder_name.setFont(QtGui.QFont('Arial', 10))
        
        #the suggested price 
        self.bidder_price = self.findChild(QtWidgets.QSpinBox,"bidder_price")
        self.bidder_price.setFont(QtGui.QFont('Arial', 10))
        self.prix = self.findChild(QtWidgets.QLabel,"prix")
        self.prix.setFont(QtGui.QFont('Arial', 8))
        
        #button to validate the bid
        self.bid_validation = self.findChild(QtWidgets.QPushButton,"bid_validation")
        self.bid_validation.setFont(QtGui.QFont('Arial', 10))

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
        self.prix_estime.setText("Prix estimé : "+selectedProduct[f'{keys[0]}']["Estimation"])
        self.product_image.setPixmap(QtGui.QPixmap(f"./images/{keys[0]}.png"))
        

    def getAllProduct(self):
        global listOfProducts
        response = requests.get(BASE + "auction/0", {})
        listOfProducts=response.json()
        i=1
        while i <=len(listOfProducts):
            item = QtGui.QStandardItem(listOfProducts[f'{i}'])
            item.setEditable(False)
            item.setFont(QtGui.QFont('Arial', 10))
            self.listModel.appendRow(item)
            i+=1


    



app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()