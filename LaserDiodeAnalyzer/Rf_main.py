#from dataclasses import replace
from Mothership_class import Mother
from ordnerstruktur_class import OrdnerStruktur
from Rf_CleanRawData_Class import RawDataProcessing
from Rf_Spektren_Class import RfSpektren
import os
import pandas as pd
from csv import DictReader


#Wenn es mehrere einstellschleifen durchläufe gibt, z.B. messungen für verschiedene
#Temperaturen, wäre es gut die Rohdaten in seperaten ordnern abzulegen 




def Rf(path_to_RawData):
        
    path = os.path.join(path_to_RawData + r'/')
    
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
                
                # RohDaten in anständige Form bringen und in csv Datei Speichern
                Instanz_RawDataProcessing = RawDataProcessing(path_to_raw_data)
                clean_raw_Data_df = Instanz_RawDataProcessing.RfSpektrum_DataFrame()
                clean_raw_Data_df.to_csv(path_to_AuswertungsSubOrdner + 'Rf_cleanRawData.csv')
                
                ####Übersichtsspektrum in bereinigter form Speichern (im zusammenfassungs ordner)
                # Spektren die einen kleineren Span haben werden gefittet                
                aktuelle_spannung = Mothership_instanz.Spannung(current_dataname)      
                Instanz_Rf = RfSpektren(value, path_to_AuswertungsSubOrdner)
             
                if '3.000e+10Hz' in current_dataname:
                    #Speichern der Bereinigten Daten (Nur Frequenz und Intensität) 
                    #in einer CSV Datei
                    path_zusammenfassung = path + '/Auswertung/'
                    Rf_PlotDaten_dBm_Path_csv = path_zusammenfassung + 'Rf_PlotDaten_'+ aktuelle_spannung +'V_3.000e+10Hz_dBm.csv'
                    Rf_PlotDaten_mW_Path_csv = path_zusammenfassung + 'Rf_PlotDaten_'+ aktuelle_spannung +'V_3.000e+10Hz_mW.csv' 
                    Rf_PlotDaten_normiert_dBm_Path_csv = path_zusammenfassung + 'Rf_PlotDaten_normiert_'+ aktuelle_spannung +'V_3.000e+10Hz_dBm.csv'
                    
                    Instanz_Rf.PlotDataDataFrame_dBm_full_spann().to_csv(Rf_PlotDaten_dBm_Path_csv, sep=';', decimal=',')
                    Instanz_Rf.PlotData_dBm_full_spann_normalized_df().to_csv(Rf_PlotDaten_normiert_dBm_Path_csv, sep=';', decimal=',')
                    Instanz_Rf.PlotDataDataFrame_mW_full_spann().to_csv(Rf_PlotDaten_mW_Path_csv, sep=';', decimal=',')
                    

                else:
                    ####Fitten##############################
                    Rf_PlotDaten_dBm_Path_csv = path_to_AuswertungsSubOrdner + 'Rf_PlotDaten_'+ aktuelle_spannung +'V_dBm.csv'
                    Rf_PlotDaten_mW_Path_csv = path_to_AuswertungsSubOrdner + 'Rf_PlotDaten_'+ aktuelle_spannung +'V_mW.csv'
                    Instanz_Rf.PlotDataDataFrame_dBm_zoomed_spann().to_csv(Rf_PlotDaten_dBm_Path_csv, sep=';', decimal=',')
                    Instanz_Rf.PlotDataDataFrame_mW_zoomed_spann().to_csv(Rf_PlotDaten_mW_Path_csv, sep=';', decimal=',')                    
                    #Instanz_Rf.PlotSpektren_mW()
                    
                    #####Daten Fitten und Fit Parameter in csv schreiben##########################
                    
                    #### dBm ####
                    # Geht irgendwie nicht mit einem Lorentz zu fitten. wahrscheinlich wegen der Logarithmierten y Achse (dBm)        
                    # Startwerte der Fit Parameter:
                    #A_dBm = -10
                    #xc_dBm = 12.38
                    #w_dBm = 0.05
                    #fit_startValues_dBm_list = [A_dBm, xc_dBm, w_dBm]
                    #df_dBm = pd.read_csv(Rf_PlotDaten_dBm_Path_csv)
                    #print(Rf.DatenFitten(df_dBm, fit_startValues_dBm_list))
                    
                    #### mW ####
                    # wenn die csv mit den plotdaten wieder eingelesen wird, werden die column names(indexe) nicht richtig
                    # gelesen, weil sie doppelt sind. deswegen dieser workarount
                    df_mW = pd.read_csv(Rf_PlotDaten_mW_Path_csv, sep=';', decimal=',')
                    col_names = DictReader(open(Rf_PlotDaten_mW_Path_csv, 'r')).fieldnames #https://stackoverflow.com/questions/50083583/allow-duplicate-columns-in-pandas
                    col_names = col_names[0]
                    col_names = list(col_names.split(';'))
                    df_mW.columns=col_names
                    
                    fit_parameters_mW_df = Instanz_Rf.DatenFitten(df_mW)
                    Fit_parameter_alles_df = fit_parameters_mW_df[0]
                    #Fit_parameter_zusammenfassung_df = fit_parameters_mW_df[1]
                    Fit_parameter_alles_df.to_csv(path_to_AuswertungsSubOrdner + 'LorentzFitParameters.csv', sep=';', decimal=',')
                    
                    ######## Aus den Fit Parametern die y Werte Für einen Fit erstellen.##################
                    ######## Diese Werte mit den zugehörigen x Werten in einer CSV Datei speichern ######
                    ######## Da Fitten nur für die in mW umgerechneten Intensitätswerte funktoniert
                    ######## werden auch nur mW fits erstellt und keine dBm
                    #fit_parameters_mW_df =pd.read_csv(path_to_AuswertungsSubOrdner + 'LorentzFitParameters.csv', 
                                                      #index_col = 0, sep=';', decimal=',')
                    #fit_mW_df = Instanz_Rf.FitDfErstellen(Fit_parameter_alles_df)
                    #fit_mW_df.to_csv(path_to_AuswertungsSubOrdner + 'Lorentz_FitDataFrame.csv', sep=';', decimal=',')        
                    #Daten Plotten
                    #Instanz_Rf.PlotDataWithFit(Fit_parameter_alles_df)
        
        ###############################################################
        ###########Zusammenfassung der Fitwerte Erstellen##############
        ###############################################################
        path_data= path + '/Auswertung/Rf/'
        path_zusammenfassung = path + '/Auswertung'
        Rf_folder_paths=[x[0] for x in os.walk(path_data)]
        dir_list =[]
        for folder_path in Rf_folder_paths:
            if os.path.basename(folder_path) == 'Rf':
                pass
            else:
                if '3.000e+10Hz' in os.path.basename(folder_path):
                    pass
                else:
                    dir_list.append(os.path.basename(folder_path))
        
        dir_list.pop(0) #Erstes Element ist der Rf ordner. Dieser wird gelöscht. IST NICHT SCHÖN
        voltage_span_list = [element[9:] for element in dir_list]
        #voltage_list = [voltage[:4] for voltage in voltage_span_list]
        #unique_voltage_list = list(set(voltage_list))
        span_list =[span.split('RF')[1] for span in voltage_span_list]
        unique_span_list = list(set(span_list))
        list_of_dictionarys = [] #hier werden dann dictionarys reingeschrieben, in diese die dataframes mit den verschiedenen FItwerten reingeschrieben werden, jede unterliste gehört zu einem Span
        
        for i in unique_span_list: #https://thispointer.com/how-to-create-and-initialize-a-list-of-lists-in-python/
            list_of_dictionarys.append({i:[]})
        for dir in dir_list:
            #für full span gibt es keine fits, daher fullspan überspringen
            if '3.000e+10Hz' in dir:
                pass
            else: 
                current_dirPath = path_data + '/' + dir
                FitData_path = current_dirPath + '/' + 'LorentzFitParameters.csv'
                aktuelle_voltage = dir[9:][:4]
                aktueller_span = dir.split('RF')[1] 
                for dictionary in list_of_dictionarys:
                    for key in dictionary:
                        if key == aktueller_span:
                            fitdata_df = pd.read_csv(FitData_path, sep=';', decimal=',', index_col=0)
                            
                            # erstellen einens dataframes mit der aktuellen spannung
                            # diesen dann in den dataenframe, der die Fitwerte enthält enfühgen
                            aktuelle_voltage_list = [aktuelle_voltage for i in fitdata_df.columns] #Absorberspannung für Multiindex
                            #print(fitdata_df.columns)
                            #print(aktuelle_voltage_list)
                            spannungs_hilfs_df = pd.DataFrame([aktuelle_voltage_list], columns=fitdata_df.columns)
                            spannungs_hilfs_df.index=['Uabs']
                            #print(spannungs_hilfs_df)
                            fitvalues_main_df = pd.concat([spannungs_hilfs_df, fitdata_df])
                            #print(fitvalues_main_df)
                            dictionary.setdefault(key, []).append(fitvalues_main_df)
        #print(list_of_dictionarys)
        
        for dictionary in list_of_dictionarys:
           #print(dictionary)
            dict_key = list(dictionary.keys())[0]
            fitvalues_df = pd.concat(dictionary.get(dict_key),axis=1)
            y_0_zusammenfassung_df = fitvalues_df.filter(like='y_0')
            y_0_zusammenfassung_df.to_csv(path_zusammenfassung +'/'+ 'Rf_y0_span_'+ dict_key +'_mW_summary.csv', sep=';', decimal=',')
            xc_zusammenfassung_df = fitvalues_df.filter(like='Frequency (GHz)')
            xc_zusammenfassung_df.to_csv(path_zusammenfassung +'/'+ 'Rf_xc_span_'+ dict_key +'_mW_summary.csv', sep=';', decimal=',')
            FWHM_zusammenfassung_df = fitvalues_df.filter(like='FWHM (GHz)')
            FWHM_zusammenfassung_df.to_csv(path_zusammenfassung +'/'+ 'Rf_FWHM_span_'+ dict_key +'_mW_summary.csv', sep=';', decimal=',')
            Amplitude_zusammenfassung_df = fitvalues_df.filter(like='Amplitude')
            Amplitude_zusammenfassung_df.to_csv(path_zusammenfassung +'/'+ 'Rf_Amplitude_span_'+ dict_key +'_mW_summary.csv', sep=';', decimal=',')