import os
from Mothership_class import Mother
from acf_Spektren_Class import acf_Spektren
from acf_CleanRawData_Class import acf_RawDataProcessing 
from ordnerstruktur_class import OrdnerStruktur
import pandas as pd
import numpy as np

def ACF(path_to_RawData):    
    
    path = os.path.join(path_to_RawData + r'/')
    
    Mothership_instanz = Mother(path)
    Mothership_instanz.Auswertungsordner_erstellen()
    acf_Ordnerstruktur_instanz = OrdnerStruktur(path)   
    
    counter = 0 
    acf_dir = acf_Ordnerstruktur_instanz.acf_dir()
    y0_zusammenfassung_list =[]
    xc_zusammenfassung_list= []
    A_zusammenfassung_list = []
    FWHM_zusammenfassung_list = []
    intensity_zusammenfassung_list = []
    
    if acf_dir == []:
        pass
    else:
        for element in acf_dir:    
            for key, value in element.items(): #key=Pfad zu Rohdaten, Value=Pfad zu subOrdner mit Auswertung
                print('ACF-Spektrum Nummer ', counter)
                
                counter += 1
                path_to_raw_data = key
                current_dataname = os.path.basename(key)
                path_to_AuswertungsSubOrdner = value +'/'
                
                # Aktueller Spannungswert (string)
                spannung = Mothership_instanz.Spannung(current_dataname)
                
                # RohDaten in anständige Form bringen und in csv Datei Speichern
                Instanz_RawDataProcessing = acf_RawDataProcessing(path_to_raw_data)
                clean_raw_Data_df = Instanz_RawDataProcessing.ACFSpektrum_DataFrame()
                clean_raw_Data_df.to_csv(path_to_AuswertungsSubOrdner + 'ACF_cleanRawData.csv')
                
                # Instanz der ACF Klasse erstellen
                Instanz_acf = acf_Spektren(value, path_to_AuswertungsSubOrdner)
                
                # Speichern der Bereinigten Daten (Nur Zeit und Intensität) 
                # in einer CSV Datei 
                # Intensität nicht auf 1 normiert (Originalwerte)        
                acf_PlotDaten_Path_csv = path_to_AuswertungsSubOrdner + 'ACF_'+spannung+'V_PlotDaten.csv'
                Instanz_acf.PlotDataDataFrame().to_csv(acf_PlotDaten_Path_csv, sep=';', decimal=',')
                
                intensity_series = Instanz_acf.PlotDataDataFrame().max() #intensität die vom autokorrelator gemessen wird (in Counts)
                intensity_series.name = 'Uabs = -'+spannung+' V'
                intensity_zusammenfassung_list.append(intensity_series)
                #print(type(intensity_series))
                # Intensität auf 1 Normiert
                acf_PlotDaten_normalized_Path_csv = path_to_AuswertungsSubOrdner + 'ACF_PlotDaten_normalized.csv'
                Instanz_acf.Normalize().to_csv(acf_PlotDaten_normalized_Path_csv, sep=';', decimal=',')
            
            # Fit Paramater in einer CSV Datei speichern
            normalized_df = Instanz_acf.Normalize().replace(np.nan, 0) #NaN werte in df werden durch 0 Ersetzt, da sonst das fitten nicht funktioniert
            Fit_parameter_df = Instanz_acf.DatenFitten(normalized_df)#, fit_startValues_list)
            Fit_parameter_alles_df = Fit_parameter_df[0]
            Fit_parameter_zusammenfassung_df = Fit_parameter_df[1]
            Fit_parameter_alles_df.to_csv(path_to_AuswertungsSubOrdner + 'Sech_2_FitParameters.csv', sep=';', decimal=',')
           
            #####Zusammenfassung der Fitparameter erstellen und alle in seperate CSV datein schreiben
            
            y0 = Fit_parameter_zusammenfassung_df['y_Minimum'].rename(spannung)
            y0.index = y0.index.astype(float)
            y0_zusammenfassung_list.append(y0)
            
            xc = Fit_parameter_zusammenfassung_df['Center Zeit (ps)'].rename(spannung)
            xc.index = xc.index.astype(float)
            xc_zusammenfassung_list.append(xc)
            
            A = Fit_parameter_zusammenfassung_df['Amplitude'].rename(spannung)
            A.index = A.index.astype(float)
            A_zusammenfassung_list.append(A)
            
            FWHM = Fit_parameter_zusammenfassung_df['FWHM (ps)'].rename(spannung)
            FWHM.index = FWHM.index.astype(float)
            FWHM_zusammenfassung_list.append(FWHM)
        
        ######Zusammenfassung der Fitparamewter erstellen und in CSV Datei speichern 
        # Strom index liste aus allen dataframes erstellen 
        # (mit jedem eingestellten strom einmal) für Zusammenfassung.
        # Sodass auch messungen mit unterschiedlichen Stromwerten zusammen anständig gespeichert werd
        
        stromIndex_list = []
        for element in FWHM_zusammenfassung_list: 
            liste = element.index.values.astype(float)
            liste = liste.tolist()
            stromIndex_list.append(liste)
        stromIndex_list = [item for sublist in stromIndex_list for item in sublist] #https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-a-list-of-lists
        stromIndex_list = sorted(list(set(stromIndex_list)))
        hilfs_df = pd.DataFrame(index=stromIndex_list)#leerer Dataframe, sein index enthält alle ströme die in den Messungen eingestellt wurden
        
        # Hier werden nun die Dataframes mit den Zusammenfassungen der Fitparameter 
        # erstellt und in eine csv Datei geschrieben
        path_zusammenfassungen = path + '/Auswertung/'
        
        FWHM_zusammenfassung_list = [hilfs_df] + FWHM_zusammenfassung_list
        FWHM_zusammenfassung_df = pd.concat(FWHM_zusammenfassung_list, axis=1)               
        FWHM_zusammenfassung_df.index.name = 'Current (mA)'
        FWHM_zusammenfassung_df.columns.name = 'Voltage'
        FWHM_zusammenfassung_df.to_csv(path_zusammenfassungen + 'ACF_FWHM_summary.csv', sep=';', decimal=',')
        
        y0_zusammenfassung_list = [hilfs_df] + y0_zusammenfassung_list 
        y0_zusammenfassung_df = pd.concat(y0_zusammenfassung_list, axis=1)
        y0_zusammenfassung_df.index.name = 'Current (mA)'
        y0_zusammenfassung_df.columns.name = 'Voltage'
        y0_zusammenfassung_df.to_csv(path_zusammenfassungen + 'ACF_y0_summary.csv', sep=';', decimal=',')
        
        xc_zusammenfassung_list = [hilfs_df] + xc_zusammenfassung_list
        xc_zusammenfassung_df = pd.concat(xc_zusammenfassung_list, axis=1)
        xc_zusammenfassung_df.index.name = 'Current (mA)'
        xc_zusammenfassung_df.columns.name = 'Voltage'
        xc_zusammenfassung_df.to_csv(path_zusammenfassungen + 'ACF_xc_summary.csv', sep=';', decimal=',')
        
        A_zusammenfassung_list = [hilfs_df] + A_zusammenfassung_list
        A_zusammenfassung_df = pd.concat(A_zusammenfassung_list, axis=1)
        A_zusammenfassung_df.index.name = 'Current (mA)'
        A_zusammenfassung_df.columns.name = 'Voltage'
        A_zusammenfassung_df.to_csv(path_zusammenfassungen + 'ACF_Amplitude_summary.csv', sep=';', decimal=',')

        intensity_zusammenfassung_df = pd.concat(intensity_zusammenfassung_list, axis=1)
        intensity_zusammenfassung_df.to_csv(path_zusammenfassungen + 'ACF_Intensity_counts_summary.csv', sep=';', decimal=',')