from ordnerstruktur_class import OrdnerStruktur
from opt_CleanRawdata_Class import opt_RawDataProcessing
from opt_spektren_class import OptischeSpektren
from Mothership_class import Mother
import os
import pandas as pd



# Nur Wellenlänge und Intensität in einer csv Datei speichern 
def normalize_opt_data_and_save_as_csv(MesurmentFolder_Path):  
    Mothership_instanz = Mother(MesurmentFolder_Path)
    opt_ordnerstruktur_instanz = OrdnerStruktur(MesurmentFolder_Path)
    opt_dir = opt_ordnerstruktur_instanz.opt_dir()
    if opt_dir == []:
        pass
    else:
        for element in opt_dir:
            for key, value in element.items(): #key=Pfad zu Rohdaten, value=Pfad zu subOrdner mit Auswertung
                RawData_name = os.path.basename(key)
                spannung = Mothership_instanz.Spannung(RawData_name)       
                instanz_opt = OptischeSpektren(key, value)
                opt_PlotDaten_normiert_csv_path = value + '/opt_normiert_'+spannung+'V_PlotDaten.csv'
                normierter_df=instanz_opt.DataFrame_normiert_ReadyToPlot(value)
                normierter_df.to_csv(opt_PlotDaten_normiert_csv_path, sep=';', decimal=',')

def opt(path_to_RawData):    
    
    path = os.path.join(path_to_RawData+r'/' )
    
    Mothership_instanz = Mother(path_to_RawData)
    Mothership_instanz.Auswertungsordner_erstellen()
    
    opt_ordnerstruktur_instanz = OrdnerStruktur(path)
    opt_dir = opt_ordnerstruktur_instanz.opt_dir()

    counter = 0
    Bandbreite_3dB_zusammenfassung_list = []
    peak_wellenlaenge_zusammenfassung_list = []
    
    if opt_dir == []:
        pass
    else:
        for element in opt_dir:
            for key, value in element.items(): #key=Pfad zu Rohdaten, value=Pfad zu subOrdner mit Auswertung

                print('opt-Messung Nummer ', counter)
                counter += 1
                path_to_raw_data = key
                current_dataname = os.path.basename(key)
                path_to_AuswertungsSubOrdner = value + '/'
                print(current_dataname)
                
                # RohDaten in anständige Form bringen und in csv Datei Speichern
                Instanz_RawDataProcessing = opt_RawDataProcessing(path_to_raw_data)
                clean_raw_Data_df = Instanz_RawDataProcessing.OptSpektrum_DataFrame()
                clean_raw_Data_df.to_csv(path_to_AuswertungsSubOrdner + 'opt_cleanRawData.csv')
                
                # Speichern der Bereinigten Daten (Nur Wellenlänge und Intensität) 
                # in einer CSV Datei 
                instanz_opt = OptischeSpektren(value, path_to_AuswertungsSubOrdner)
                # spannung des aktuellen Dataframes
                spannung = Mothership_instanz.Spannung(current_dataname)                
                opt_PlotDaten_Path_csv = path_to_AuswertungsSubOrdner + 'opt_'+spannung+'V_PlotDaten.csv'
                instanz_opt.DataFrame_ReadyToPlot().to_csv(opt_PlotDaten_Path_csv, sep=';', decimal=',')
                

                # 3dB bandbreite Berechnen und in einer csv Datei im subauswertungsordner speichern                 
                opt_spektren_df = pd.read_csv(opt_PlotDaten_Path_csv, sep=';', decimal=',', index_col='Wavelength (nm)')                
                bandbreite_3dB = instanz_opt.Bandbreite_3dB_linfit(opt_spektren_df, spannung)
                #bandbreite_3dB = bandbreite_3dB_bandbreite_wellenlaenge
                peak_wellenlaenge = instanz_opt.peak_wellenlaenge_nm(opt_spektren_df, spannung)
                Bandbreite_3dB_zusammenfassung_list.append(bandbreite_3dB)
                peak_wellenlaenge_zusammenfassung_list.append(peak_wellenlaenge)
            
            Bandbreite_3dB_zusammenfassung_df=pd.concat(Bandbreite_3dB_zusammenfassung_list, axis=1)
            Bandbreite_3dB_zusammenfassung_df.index.name = 'Current (mA)'
            Bandbreite_3dB_zusammenfassung_df.columns.name = 'Voltage'
            Bandbreite_3dB_zusammenfassung_df.to_csv(path + '/Auswertung/' + 'opt_3dB_Bandbreite.csv', sep=';', decimal='.')
            
            Peak_wellenlaenge_zusammenfassung_df = pd.concat(peak_wellenlaenge_zusammenfassung_list, axis=1)
            Peak_wellenlaenge_zusammenfassung_df.index.name = 'Current (mA)'
            Peak_wellenlaenge_zusammenfassung_df.columns.name = 'Voltage'
            Peak_wellenlaenge_zusammenfassung_df.to_csv(path + '/Auswertung/' + 'opt_peak_Wellenlaenge.csv', sep=';', decimal='.')





