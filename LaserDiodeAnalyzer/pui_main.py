from Mothership_class import Mother
from ordnerstruktur_class import OrdnerStruktur
from pui_clean_rawdata_class import pui_RawDataProcessing
import os
import pandas as pd
import math

def pui(path_to_RawData):
    
    path = os.path.join(path_to_RawData + r'/')
    Mothership_instanz = Mother(path)
    Mothership_instanz.Auswertungsordner_erstellen()
    
    pui_Ordnerstruktur_instanz = OrdnerStruktur(path)
    pui_dir = pui_Ordnerstruktur_instanz.pui_dir()
    
    counter = 0 
    pui_power_zusammenfassung_list = []
    pui_voltage_zusammenfassung_list = []
    
    if pui_dir == []:
        pass
    else:
        for element in pui_dir:
            for key, value in element.items(): #key=Pfad zu Rohdaten, Value=Pfad zu subOrdner mit Auswertung
                print('PUI-Messung Nummer ', counter)
                counter += 1

                path_to_raw_data = key
                current_dataname = os.path.basename(key)
                path_to_AuswertungsSubOrdner = value +'/'
                spannung = Mothership_instanz.Spannung(current_dataname)
                
                # RohDaten in anständige Form bringen und in csv Datei Speichern
                Instanz_RawDataProcessing = pui_RawDataProcessing(path_to_raw_data)
                clean_RawData_df = Instanz_RawDataProcessing.pui_Dataframe()                              
                clean_RawData_df.to_csv(path_to_AuswertungsSubOrdner + 'PUI_cleanRawData.csv', sep=';', decimal=',')
                
                power_series = clean_RawData_df['Power (mW)']
                power_series = power_series.rename('Uabs = -' + spannung + ' V')
                pui_power_zusammenfassung_list.append(power_series)
                
                voltage_series = clean_RawData_df['Voltage (V)']
                voltage_series = voltage_series.rename('Uabs = -' + spannung + ' V')
                pui_voltage_zusammenfassung_list.append(voltage_series)
                
        ######Zusammenfassung der kennlinien und in CSV Datei speichern 
        # Strom index liste aus allen dataframes erstellen 
        # (mit jedem eingestellten strom einmal) für Zusammenfassung.
        # Sodass auch messungen mit unterschiedlichen Stromwerten zusammen anständig gespeichert werden        
        stromIndex_list = []
        
        for element in pui_power_zusammenfassung_list:
            liste = element.index.values.astype(float)
            liste = liste.tolist()
            stromIndex_list.append(liste)        

        stromIndex_list = [item for sublist in stromIndex_list for item in sublist] #https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-a-list-of-lists
        stromIndex_list = sorted(list(set(stromIndex_list)))
        stromIndex_list = [x for x in stromIndex_list if math.isnan(x) == False]
        hilfs_df = pd.DataFrame(index=stromIndex_list)#leerer Dataframe, sein index enthält alle ströme die in den Messungen eingestellt wurden

        ######PowerZusammenfassung########################
        # In den einzelnen DataFrames der pui_power_zusammenfassung_list
        # die indexe (strom) von strings zu floats convertieren
        pui_power_zusammenfassung_list2 = []
        for element in pui_power_zusammenfassung_list:
            element.index = element.index.astype(float)
            pui_power_zusammenfassung_list2.append(element)

        # Erstellen des Datenframes mit der Zusammenfassung der kennlinien
        path_zusammenfassungen = path + '/Auswertung/'
        
        pui_power_zusammenfassung_list2 = [hilfs_df] + pui_power_zusammenfassung_list2
        pui_power_zusammenfassung_df = pd.concat(pui_power_zusammenfassung_list2, axis=1)
        pui_power_zusammenfassung_df = pui_power_zusammenfassung_df.apply(pd.to_numeric) # convertiert Dataframe inhalt zu floats
        pui_power_zusammenfassung_df.to_csv(path_zusammenfassungen + 'PUI_power_summary.csv', sep=';', decimal=',')
        
        ######VoltageZusammenfassung##########################
        # Im endeffekt habe ich das gleiche gemacht wie bei der power zusammenfassung

        # In den einzelnen DataFrames der pui_power_zusammenfassung_list
        # die indexe (strom) von strings zu floats convertieren
        pui_voltage_zusammenfassung_list2 = []
        for element in pui_voltage_zusammenfassung_list:
            element.index = element.index.astype(float)
            pui_voltage_zusammenfassung_list2.append(element)

        # Erstellen des Datenframes mit der Zusammenfassung der kennlinien
        pui_voltage_zusammenfassung_list2 = [hilfs_df] + pui_voltage_zusammenfassung_list2
        pui_voltage_zusammenfassung_df = pd.concat(pui_voltage_zusammenfassung_list2, axis=1)
        pui_voltage_zusammenfassung_df = pui_voltage_zusammenfassung_df.apply(pd.to_numeric) # convertiert Dataframe inhalt zu floats
        pui_voltage_zusammenfassung_df.to_csv(path_zusammenfassungen + 'PUI_voltage_summary.csv', sep=';', decimal=',')


