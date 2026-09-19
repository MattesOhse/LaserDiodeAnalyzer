from Mothership_class import Mother
from ordnerstruktur_class import OrdnerStruktur
#import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import pandas as pd
import os


def Rf_modenkopplung_df(spannung, intensitaet): #gibt dataframe zurück wo drinsteht on modenkopplung vorliegt oder nicht
    modenkopplungsliste = []
    strom_liste = []
    for strom in intensitaet:
        strom_liste.append(strom)
        spektrums_maximum = intensitaet[strom].max()
        snr_fuer_modenkopplung = spektrums_maximum - 30
        peaks, _ = find_peaks(intensitaet[strom], height=snr_fuer_modenkopplung, distance=100)
        if len(peaks) != 1:
            modenkopplungsliste.append(0) #Keine Modenkopplung vorhanden
        else:
            modenkopplungsliste.append(1) # Es herrscht modenkopplung
    df = pd.Series(modenkopplungsliste, index=strom_liste, name=spannung + 'V')
    return df


def Opt_modenkopplung_df(spannung, intensitaet): #gibt dataframe zurück wo drinsteht on modenkopplung vorliegt oder nicht
    modenkopplungsliste = []
    strom_liste = []
    for strom in intensitaet:
        strom_liste.append(strom)
        spektrums_maximum = intensitaet[strom].max()
        snr_fuer_modenkopplung = spektrums_maximum - 20
        peaks, _ = find_peaks(intensitaet[strom],height=snr_fuer_modenkopplung,prominence=1)
        if len(peaks) != 1:
            modenkopplungsliste.append(0) #Keine Modenkopplung vorhanden
        else:
            modenkopplungsliste.append(1) # Es herrscht modenkopplung        
    df = pd.Series(modenkopplungsliste, index=strom_liste, name=spannung + 'V')
    return df







if __name__=='__main__':

    rawData_path_list = [
                         r'\\fbh-berlin.de\fbhdfs\OE_Mess\Messdaten\820-1000nm\TPL\R1268-4_830nm_ASOPS\030202_DQW_RW_SCPM_Labs400µm']
    
    for path_to_rawData in rawData_path_list:
    
        
        Motherclass = Mother(path_to_rawData)
        ordnerStruktur=OrdnerStruktur(path_to_rawData)
    
    
    ###### Schleife für opt Daten ##########
        spannung_liste = [] #behelf um später die daten von Rf und opt spektren zu vergleichen 
        opt_modenkopplung_liste = []
        for element in ordnerStruktur.opt_dir():
                        
            path_to_clean_rawData = list(element.values())[0]
            spannung = os.path.basename(os.path.normpath(path_to_clean_rawData))
            spannung = spannung[9:13]
            spannung_liste.append(spannung+'V')
    
            df = Motherclass.Load_CleanRawData_from_CSV('opt', path_to_clean_rawData)
            x = df['Wavelength (nm)'] #nm
            y = df['Intensity (dBm)'] #Intensität
                
            opt_modenkopplung_df=Opt_modenkopplung_df(spannung, y)
            opt_modenkopplung_liste.append(opt_modenkopplung_df)
           
    
          
        if len(opt_modenkopplung_liste) != 0:        
            opt_modenkopplung_final_df = pd.concat(opt_modenkopplung_liste, axis=1) 
            #print(opt_modenkopplung_final_df)
            opt_modenkopplung_final_df.to_csv(path_to_rawData + '/Auswertung'+'/opt_modenkopplung.csv', 
                                              sep=';', decimal=',')
        else: 
            pass

       
        ###### Schleife für Rf Daten ##########
        rf_modenkopplung_liste = []
        for element in ordnerStruktur.Rf_dir():
            #print(list(element.values())[0])
            if '6.300e+09Hz' in list(element.values())[0]:
                path_to_clean_rawData = list(element.values())[0]
                #print(path_to_clean_rawData)
                spannung = os.path.basename(os.path.normpath(path_to_clean_rawData))
                spannung = spannung[9:13]
        
                df = Motherclass.Load_CleanRawData_from_CSV('Rf', path_to_clean_rawData)
                x = df['Frequency (GHz)'] #GHz
                y = df['Intensity (dBm)'] #Intensität

                rf_modenkopplung_df=Rf_modenkopplung_df(spannung, y)
                rf_modenkopplung_liste.append(rf_modenkopplung_df)
            else:
                pass
        
        if len(rf_modenkopplung_liste) != 0:
            #print('hallo')
            rf_modenkopplung_final_df = pd.concat(rf_modenkopplung_liste, axis=1) 
            rf_modenkopplung_final_df.to_csv(path_to_rawData + '/Auswertung'+'/Rf_modenkopplung.csv', 
                                            sep=';', decimal=',')
        else:
            pass
        
    
        
        ###### Vergleich von optischen- und Rf- Modenkopplungs Dataframes um final zu bestimmen, ob modenkopplung vorliuegt oder nicht
        finale_modenkopplung_liste = []
        for spannung in spannung_liste:
            
            opt_df = opt_modenkopplung_final_df[spannung]
            rf_df=rf_modenkopplung_final_df[spannung]
            modenkopplung_liste = []
            #modenkopplung_df.name = spannung + 'V'
            strom_liste = []
            for strom in opt_df.index:
                strom_liste.append(float(strom))
                if opt_df[strom] == rf_df[strom]:
                    modenkopplung_liste.append(opt_df[strom])
                else:
                    modenkopplung_liste.append(0) #keine Modenkopplung
            #print(strom_liste)
            modenkopplung_insgesammt_df = pd.Series(modenkopplung_liste, 
                                                    index=strom_liste, 
                                                    name=spannung)
            #print(modenkopplung_insgesammt_df)
            finale_modenkopplung_liste.append(modenkopplung_insgesammt_df)
        #print(finale_modenkopplung_liste)
        if len(finale_modenkopplung_liste) != 0 :
            finaler_modenkopplungs_df = pd.concat(finale_modenkopplung_liste, axis=1)
            #print(finaler_modenkopplungs_df)
            finaler_modenkopplungs_df.to_csv(path_to_rawData + '/Auswertung'+'/Modenkopplung.csv', 
                                             sep=';', decimal=',')
        else:
            pass
    
    
    