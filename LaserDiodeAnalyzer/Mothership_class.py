import os
import pandas as pd

class Mother():
    def __init__(self, path_to_rawData):
        self.path = path_to_rawData
        self.path_to_Auswertung = self.path + '/Auswertung/'

    # Extrahiert die Absorberspannung (string) aus dem Dateinamen
    def Spannung(self, MesurmentDataName):
        if 'S.dat' in MesurmentDataName:
            spannung = MesurmentDataName.replace('S.dat', '')
            spannung = spannung[-7:-3]
        if 'RF' in MesurmentDataName:
            spannung = MesurmentDataName.split('RF',1)[0]
            spannung = spannung[-7:]
            spannung = spannung[:4]
        if 'ACF.dat' in MesurmentDataName:
            spannung = MesurmentDataName.replace('ACF.dat', '')
            spannung = spannung[-7:-3]
        if 'G.dat' in MesurmentDataName: 
            spannung = MesurmentDataName.replace('G.dat', '')
            spannung = spannung[-7:-3]

        return spannung


    # Diese Methode Bringt die Rohdaten in eine anständige Form
    def loadRawData(self):  
        with open(self.path, 'rb') as file:
            data = file.read()
        data = data.decode("cp1252") 
        data = data.split("\n")
        data = [i.strip() for i in data]
        del data[0:83]
        #print(data)
        cleanData = [i.split() for i in data] #Das sind die Sauberen Daten
        return cleanData
    
    # Diese Methode erstellt einen Ordner mit dem namen Auswertung, 
    # falls er nicht im gegebenen Pfad der init-funktion schon existiert 
    def Auswertungsordner_erstellen(self): 
        auswertung_dir = self.path_to_Auswertung
        if not os.path.exists(auswertung_dir):
            os.makedirs(auswertung_dir)
            #print("Directory " , auswertung_dir ,  " Created ")
        else:
            pass
            #print("Directory " , auswertung_dir ,  " already exists")
    

    # Erstellen eines Anständigen DataFrames mit den Intreressanten messwerten aus den 
    # sauberen Roh Daten, die in einer CSV Datei gespeichert wurden 
    def Load_CleanRawData_from_CSV(self, DataType, path_to_AuswertungsSubOrdner): 
        if DataType == 'Rf':
            path_to_cleanRawData = path_to_AuswertungsSubOrdner + '/Rf_cleanRawData.csv'           
        if DataType == 'opt':
            path_to_cleanRawData = path_to_AuswertungsSubOrdner + '/opt_cleanRawData.csv'
        if DataType == 'acf':
            path_to_cleanRawData = path_to_AuswertungsSubOrdner + 'ACF_cleanRawData.csv'
        
        df = pd.read_csv(path_to_cleanRawData, 
                         header=[0, 1], 
                         skipinitialspace=True)

        multiindex=pd.MultiIndex.from_tuples(df.columns, 
                            names=["Messwerte", "Stromwert"])
        
        multiindex=list(multiindex)
        multiindex.pop(0)
        
        multiindex=pd.MultiIndex.from_tuples(multiindex, 
                            names=["Messwerte", "Stromwert"])
        
        df.drop('Messwerte',inplace=True, axis=1)
        df.columns = multiindex
        
        return df