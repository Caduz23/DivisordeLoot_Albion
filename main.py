from PySide6 import QtCore
from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtWidgets import (QApplication, QMainWindow, QTableWidgetItem, QTableWidget, QCheckBox)
from ui_main import Ui_MainWindow
from database import Data_base
import sys
import sqlite3

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Divisor de Loot - Albion Online")
        self.pushButton.clicked.connect(self.gerarArquivo)
        self.pushButton_2.clicked.connect(self.cadastrarMembro)
        self.buscar_membros()
        
    def cadastrarMembro(self):
        db = Data_base()
        db.connect()
        
        fullDataSet = (
            self.lineEdit_5.text(),0
        )
        
        if fullDataSet[0] != "":
            resp = db.registrar_membro(fullDataSet)
        self.buscar_membros()
        db.close_connection()
        
    def buscar_membros(self):
        db = Data_base()
        db.connect()
        result = db.selecionar_membros()
        
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(2)
        
        for row, text in enumerate(result):
            for column, data in enumerate(text):
                item = QTableWidgetItem(str(data))
                if column == 0:
                    item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                    item.setCheckState(Qt.CheckState.Unchecked)
                self.tableWidget.setItem(row, column, item)
                    
        db.close_connection()
        
        for col in range(self.tableWidget.columnCount()):
            self.tableWidget.resizeColumnToContents(col)
            
    def checarCheckBox(self):
        membros_participantes = []
        for row in range(self.tableWidget.rowCount()):
            if(self.tableWidget.item(row,0).checkState() == Qt.CheckState.Checked):
                membros_participantes.append(self.tableWidget.item(row,0).text())
        return membros_participantes
        
    def gerarArquivo(self):    
        
        players = self.checarCheckBox()
        arquivo = open("divisao.txt", "w")
        nome = window.lineEdit.text()
        data = window.lineEdit_2.text()
        valorTotal = int(window.lineEdit_3.text())
        valorReparo = int(window.lineEdit_4.text())
        valorFinal = int(valorTotal)-int(valorReparo)
        valorDivido = valorFinal/int(len(players))        
        valorTotal = valorTotal/1000000
        valorReparo = valorReparo/1000000
        valorFinal = valorFinal/1000000
        valorDivido = valorDivido/1000000
        valorTotalFormatado = "{:.4f}".format(valorTotal)
        valorReparoFormatado = "{:.4f}".format(valorReparo)
        valorFinalFormatado = "{:.4f}".format(valorFinal)
        valorDividoFormatado = "{:.4f}".format(valorDivido)

        db = Data_base()
        db.connect()
        db.loot_total(valorDividoFormatado,players)
        db.close_connection()
        
        arquivo.write(f"Nome: {nome}")
        arquivo.write(f"   Data do Loot: {data}\n")
        arquivo.write(f"Valor Total do Loot: {valorTotalFormatado}M")
        arquivo.write(f"   Custo de reparo: {valorReparoFormatado}M\n")
        arquivo.write(f"Loot Divido: {valorFinalFormatado}M\n")
        arquivo.write("Players:\n")
        arquivo.writelines(f"%s {valorDividoFormatado}M\n" %t for t in players)
        
            
if __name__ == "__main__":
    
    db = Data_base()
    db.connect()
    db.create_table_membros()
    db.close_connection()
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
        
