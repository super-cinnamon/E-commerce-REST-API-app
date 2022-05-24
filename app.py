from glob import glob
from PyQt5 import QtWidgets, uic, QtGui,QtCore
import sys
import requests
from time import sleep
import threading

from test import BASE

def countdown():
    global time_left
    time_left = 30
    while time_left != 0:
        time_left = time_left - 1
        #update the label
        timer_label.setText(str(time_left))
        sleep(1)
    print("time is over, bidding for item has been closed")
    bid_validation.setEnabled(False)


    ####### here we update the item

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
        global bid_validation
        bid_validation = self.findChild(QtWidgets.QPushButton,"bid_validation")
        bid_validation.setFont(QtGui.QFont('Arial', 10))
        bid_validation.clicked.connect(self.validateClickListener)

        #liste of bidders
        self.bidders_list = self.findChild(QtWidgets.QTableView,"bidders_list")

        #timer label 
        global timer_label
        timer_label = self.findChild(QtWidgets.QLabel,"timer_label")

        self.show()

    def openSelectedClickListener(self, index):
        ###### here we have to check if the item has been bought or not while updating the info
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
        ####### if the item already has an owner then make the buttons unusable 
        

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
    
    def validateClickListener(slef):
        global time_left
        time_left = 30
        timer_label.setText(str(time_left))
        #here we will first add to the bidder list
        pass


    



app = QtWidgets.QApplication(sys.argv)
window = Ui()
countdown_thread = threading.Thread(target = countdown)
countdown_thread.start()
app.exec_()

### start the timer thread
