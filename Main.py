import sqlite3
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from UrunEkle import *

uygulama = QApplication(sys.argv)
pencere = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(pencere)
pencere.show()


# Veritabanı işlemleri
baglanti = sqlite3.connect("Urunler.db")
islem = baglanti.cursor()
baglanti.commit()

table = islem.execute(
    "create table if not exists urun (urunKodu int , urunAdi varchar(30), birimFiyati int , stokMiktari int,urunAciklamasi text , marka varchar(30) , kategori varchar(30))")


def KayitEkle():
    UrunKodu = int(ui.txtUrunKodu.text())
    UrunAdi = ui.txtUrunAdi.text()
    BirimFiyati = int(ui.txtBirimFiyati.text())
    StokMiktari = int(ui.txtStokMiktari.text())
    UrunAciklamasi = ui.txtUrunAciklamasi.text()
    Marka = ui.cmbMarka.currentText()
    Kategori = ui.cmbKategori.currentText()

    try:
        islem.execute("insert into urun (urunKodu,urunAdi,birimFiyati,stokMiktari,urunAciklamasi,marka,kategori)        values (?,?,?,?,?,?,?)",
                      (UrunKodu, UrunAdi, BirimFiyati, StokMiktari, UrunAciklamasi, Marka, Kategori))
        baglanti.commit()
        ui.statusbar.showMessage("Kayit Ekleme işlemi Başarili.", 2000)
    except Exception as ex:
        ui.statusbar.showMessage(
            "Kayit Ekleme işlemi Başarisiz. {0}".format(ex), 20000)

def KayitListele():
    ui.tblUrun.clear()
    ui.tblUrun.setHorizontalHeaderLabels(("Ürün Kodu","Ürün Adi","Ürün Fiyati","Ürün Stok Miktari","Ürün Aciklama","Ürün Marka","Ürün Kategori"))
    ui.tblUrun.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    values = islem.execute("Select * from urun")
    for index,value in enumerate(values):
        for rowValue , rowRecord in enumerate(value):
            ui.tblUrun.setItem(index,rowValue,QTableWidgetItem(str(rowRecord)))

def KategoriyeGoreListele():
    ui.tblUrun.clear()
    ui.tblUrun.setHorizontalHeaderLabels(("Ürün Kodu","Ürün Adi","Ürün Fiyati","Ürün Stok Miktari","Ürün Aciklama","Ürün Marka","Ürün Kategori"))
    ui.tblUrun.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    listelenilicekKategori = ui.cmbKategoriListele_3.currentText()
    sorgu = f"select * from urun where kategori = '{listelenilicekKategori}'"
    values = islem.execute(sorgu)
    for index,value in enumerate(values):
        for rowValue , rowRecord in enumerate(value):
            ui.tblUrun.setItem(index,rowValue,QTableWidgetItem(str(rowRecord)))

def KayitSil():
    silmesaj = QMessageBox.question(pencere,"Silme Onayi","Mevcut Kaydi Silmek istediğnize eminmisiniz??",QMessageBox.Yes| QMessageBox.No)
    if silmesaj == QMessageBox.Yes:
        secilenKayit = ui.tblUrun.selectedItems()
        silinicekKayit = secilenKayit[0].text()
        sorgu = f"DELETE FROM urun WHERE urunKodu = {silinicekKayit}"

        try:
            islem.execute(sorgu)
            baglanti.commit()
            ui.statusbar.showMessage("Silme işlemi başarili",2000)
        except Exception as ex:
            ui.statusbar.showMessage(f"Silme işlemi Başarisiz. Hata :{ex}",2000)
    else:
        ui.statusbar.showMessage("Silme işlemi iptal edildi.",2000)

def KayitGuncelle():
    guncelleme = QMessageBox.question(pencere,"Silme Onayi","Mevcut Kaydi Silmek istediğnize eminmisiniz??",QMessageBox.Yes| QMessageBox.No)
    if guncelleme == QMessageBox.Yes:
            pass

#Buttonlar

ui.btnEkle.clicked.connect(KayitEkle)
ui.btnListele.clicked.connect(KayitListele)
ui.btnKategoriyeGoreListele.clicked.connect(KategoriyeGoreListele)
ui.btnSil.clicked.connect(KayitSil)


sys.exit(uygulama.exec_())
