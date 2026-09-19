import pandas as pd
import os

def PeakPower_Pulsbreite(path_to_RawData):   
    
    path_to_Auswertung = path_to_RawData + r'\Auswertung/'
    path_to_FWHMsummary = path_to_Auswertung + 'ACF_FWHM_summary.csv'
    path_Pulsbreite_summary = path_to_Auswertung+'ACF_Pulsbreite_summary.csv'
    path_PUI_Power_summary = path_to_Auswertung + 'PUI_power_summary.csv'
    path_PulsPeakPower_summary = path_to_Auswertung + 'ACF_PulsePeakPower_summary.csv'
    
    ####Berechnung der Pulsbreite######
    df_FWHM = pd.read_csv(path_to_FWHMsummary, sep=';', decimal=',')
    
    df_FWHM.index = df_FWHM.index.astype(float)
    df_FWHM = df_FWHM.set_index('Current (mA)')
    new_column_names = ['Uabs = -'+ name + ' V'  for name in df_FWHM.columns]
    df_FWHM.columns = new_column_names
    Pulsbreite_zusammenfassung_df = df_FWHM * 0.648
    Pulsbreite_zusammenfassung_df.to_csv(path_Pulsbreite_summary, sep=';', decimal=',')
        
    ####Berechnung der Pulsspitzenleistung#####
    pui_power_df = pd.read_csv(path_PUI_Power_summary,index_col=0, sep=';', decimal=',')
    pui_power_df.index = pui_power_df.index.astype(float)
    pui_power_df.index.name = 'Current (mA)'
    
    
    
    # erstellen von zwei Dataframes für pui power und Pulsbreite, die
    # nur werte enthalten, die die gleiche spannung besitzen.
    # sonst wird in der letzten schleife die PulsePeakPower aus 
    # werten berechnet, die nicht zusammen gehören 
    pui_power_zusammenfassung_neu = []
    Pulsbreite_zusammenfassung_neu = []
    for column_name_pulsbreite in Pulsbreite_zusammenfassung_df:
        for column_name_pui in pui_power_df:
            if column_name_pulsbreite == column_name_pui:
                # ich glaube ich mache aus den daten frames listen, 
                # weil bei den PUI messungen andere stromwerte eingestellt werden können
                # als bei den acf messungen (woraus die Pulsbreite berechnet wird)
                pui_power_zusammenfassung_neu.append(pui_power_df[column_name_pui])
                Pulsbreite_zusammenfassung_neu.append(Pulsbreite_zusammenfassung_df[column_name_pulsbreite])                   
            else:
                pass
    
    pui_power_zusammenfassung_neu_df = pd.concat(pui_power_zusammenfassung_neu, axis=1)
    Pulsbreite_zusammenfassung_neu_df = pd.concat(Pulsbreite_zusammenfassung_neu, axis=1)
    PulsePeakPower_summary_list = []
    
    for column_pui, column_pulsbreite in zip(pui_power_zusammenfassung_neu_df, Pulsbreite_zusammenfassung_neu_df):
        zaeler = 0.881*pui_power_df[column_pui].astype(float)
        nenner = 6.3*Pulsbreite_zusammenfassung_df[column_pulsbreite].astype(float)
        nenner.index = nenner.index.astype(float)               

        PulsePeakPower_df = zaeler.divide(nenner)
        PulsePeakPower_df=pd.DataFrame(PulsePeakPower_df,columns=[column_pui])#column_name)
        PulsePeakPower_df.index = PulsePeakPower_df.index.astype(float)
        PulsePeakPower_summary_list.append(PulsePeakPower_df)
    PulsePeakPower_summary_df = pd.concat(PulsePeakPower_summary_list, axis=1)
    PulsePeakPower_summary_df.to_csv(path_PulsPeakPower_summary, sep=';', decimal=',')