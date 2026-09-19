#from dataclasses import replace
from Mothership_class import Mother
from ordnerstruktur_class import OrdnerStruktur
from Rf_CleanRawData_Class import RawDataProcessing
from Rf_Spektren_Class import RfSpektren
import os
import pandas as pd
from csv import DictReader


def Rf_Fullspan(path_to_MesswertOrdner):
    path = os.path.join(path_to_MesswertOrdner + r'/')
    
    Mothership_instanz = Mother(path)
    Mothership_instanz.Auswertungsordner_erstellen()
    
    Rf_ordnerstruktur_instanz = OrdnerStruktur(path)
    Rf_dir = Rf_ordnerstruktur_instanz.Rf_dir()
    counter = 0 
    
    if Rf_dir == []:
        pass
    else:
        for element in Rf_dir:
            for key, value in element.items(): #key=Pfad zu Rohdaten, value=Pfad zu subOrdner mit Auswertung
                print('Rf-Messung Nummer ', counter)
                counter += 1
                path_to_raw_data = key
                current_dataname = os.path.basename(key)
                path_to_AuswertungsSubOrdner = value + '/'
                print('Aktuelle Datei: ', current_dataname)

                if '3.000e+10Hz' in current_dataname:
                    # RohDaten in anständige Form bringen und in csv Datei Speichern
                    Instanz_RawDataProcessing = RawDataProcessing(path_to_raw_data)
                    clean_raw_Data_df = Instanz_RawDataProcessing.RfSpektrum_DataFrame()
                    clean_raw_Data_df.to_csv(path_to_AuswertungsSubOrdner + 'Rf_cleanRawData.csv')

                    ####Übersichtsspektrum in bereinigter form Speichern (im zusammenfassungs ordner)
                    # Spektren die einen kleineren Span haben werden gefittet                
                    aktuelle_spannung = Mothership_instanz.Spannung(current_dataname)      
                    Instanz_Rf = RfSpektren(value, path_to_AuswertungsSubOrdner)
                    #Speichern der Bereinigten Daten (Nur Frequenz und Intensität) 
                    #in einer CSV Datei
                    path_zusammenfassung = path + '/Auswertung/'
                    Rf_PlotDaten_dBm_Path_csv = path_zusammenfassung + 'Rf_PlotDaten_'+ aktuelle_spannung +'V_3.000e+10Hz_dBm.csv'
                    Rf_PlotDaten_mW_Path_csv = path_to_AuswertungsSubOrdner + 'Rf_PlotDaten_'+ aktuelle_spannung +'V_3.000e+10Hz_mW.csv' 
                    Rf_PlotDaten_normiert_dBm_Path_csv = path_zusammenfassung + 'Rf_PlotDaten_normiert_'+ aktuelle_spannung +'V_3.000e+10Hz_dBm.csv'
                    
                    Instanz_Rf.PlotDataDataFrame_dBm_full_spann().to_csv(Rf_PlotDaten_dBm_Path_csv, sep=';', decimal=',')
                    Instanz_Rf.PlotData_dBm_full_spann_normalized_df().to_csv(Rf_PlotDaten_normiert_dBm_Path_csv, sep=';', decimal=',')
                    Instanz_Rf.PlotDataDataFrame_mW_full_spann().to_csv(Rf_PlotDaten_mW_Path_csv, sep=';', decimal=',')
                else: 
                    pass

def Rf_small_span(path_to_MesswertOrdner):
    pass


if __name__ == '__main__':
    path = r'C:\Users\matte\Desktop\TestData\test_daten_struktur\155523'
    Rf_Fullspan(path)