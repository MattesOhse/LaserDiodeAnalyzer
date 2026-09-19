import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Mothership_class import Mother

class OptischeSpektren(Mother):
    def __init__(self, path_to_rawData, path_to_AuswertungsSubOrdner):
        super().__init__(path_to_rawData)
        self.path = path_to_AuswertungsSubOrdner
    

    # Erstellen eines DataFrames mit den zu plottenden Daten(wellenlänge und intensität)
    def DataFrame_ReadyToPlot(self):
        x_values = self.Load_CleanRawData_from_CSV('opt',self.path)['Wavelength (nm)'] #DataFrame 
        x_axis = x_values.iloc[:, 0]  #Erstes Spalte des DataFrames (X-Achse)
        x_axis.name='Wavelength (nm)'
        y_values = self.Load_CleanRawData_from_CSV('opt',self.path)['Intensity (dBm)']
        plot_df = pd.concat([x_axis, y_values], axis=1)#.reindex(x_axis.index)
        plot_df = plot_df.set_index('Wavelength (nm)')
        return plot_df

    def DataFrame_normiert_ReadyToPlot(self, path_to_AuswertungsSubOrdner):
        df = self.Load_CleanRawData_from_CSV('opt', path_to_AuswertungsSubOrdner)
        x = df['Wavelength (nm)']
        y = df['Intensity (dBm)']
        wellenlaenge = x.iloc[:, 0]
        wellenlaenge.name = 'Wavelength (nm)'
        y_max=y.max()
        y_normiert = y.subtract(y_max, axis=1)
        y_normiert.index = wellenlaenge
        return y_normiert

    def Bandbreite_3dB_linfit(self, plot_df, plot_df_voltage):
        bandbreite_3dB_list = []
        peak_wellenlänge_nm_list = []
        peak_intensität_dB_list = []
        strom_liste = plot_df.columns
        for column_name in plot_df:
            try:
                y_max_dB = plot_df[column_name].max() #dB
                peak_intensität_dB_list.append(y_max_dB)
                y_max_index = plot_df[column_name].idxmax() #nm
                peak_wellenlänge_nm_list.append(y_max_index)
                
                #slice pandas series in zwei teile, an der stelle des maximums
                vorPeak = plot_df[column_name].loc[:y_max_index]
                hinterPeak = plot_df[column_name].loc[y_max_index:]

                y_3dB = y_max_dB - 3
                index_3dB_vorPeak_nm = vorPeak.sub(y_3dB).abs().idxmin()
                value_3dB_vorPeak_dBm = vorPeak.loc[[index_3dB_vorPeak_nm][0]]
                index_3dB_hinterPeak_nm = hinterPeak.sub(y_3dB).abs().idxmin()
                value_3dB_hinterPeak_dBm = hinterPeak.loc[[index_3dB_hinterPeak_nm][0]]
                ##### bestimmung der beiden Messwerte, die vor und hinter dem 3dB wert liegen
                #Für die Flanke des Spektrums, die vor dem maximal Wert (peak) liegen:

                #wenn der berechnete y_3dB wert größer ist als als der gefundene, der am
                #nächsten zu diesem wert liegt, dann den gefundenen wert nehmen und den nächsten wert nehmen, 
                #der größer ist als der gefundene (der berechnete 3dB wert liegt zwischen diesen)
                #fordere flanke
                if value_3dB_vorPeak_dBm < y_3dB:
                    x1_index_vorPeak_nm = index_3dB_vorPeak_nm
                    y1_value_vorPeak_dBm = value_3dB_vorPeak_dBm 
                    x2_index_vorPeak_nm = index_3dB_vorPeak_nm + 0.05
                    x2_index_vorPeak_nm = round(x2_index_vorPeak_nm, 2)
                    y2_value_vorPeak_dBm = vorPeak[x2_index_vorPeak_nm]


                #wenn der berechnete y_3dB wert kleiner ist als als der gefundene, der am
                #nächsten zu diesem wert liegt, dann den gefundenen wert nehmen und den nächsten wert nehmen,
                #der kleiner ist als der gefundene (der berechnete 3dB wert liegt zwischen diesen)
                if value_3dB_vorPeak_dBm > y_3dB:
                    x1_index_vorPeak_nm = index_3dB_vorPeak_nm
                    y1_value_vorPeak_dBm = value_3dB_vorPeak_dBm 
                    x2_index_vorPeak_nm = index_3dB_vorPeak_nm - 0.05
                    x2_index_vorPeak_nm = round(x2_index_vorPeak_nm,2)
                    y2_value_vorPeak_dBm = vorPeak[x2_index_vorPeak_nm]
                    
                x_vorPeak_fit_array = np.array([x1_index_vorPeak_nm, x2_index_vorPeak_nm])
                y_vorPeak_fit_array = np.array([y1_value_vorPeak_dBm,  y2_value_vorPeak_dBm])
                
                m_vorPeak, b_vorPeak = np.polyfit(x_vorPeak_fit_array, y_vorPeak_fit_array,1) #https://www.kite.com/python/answers/how-to-plot-a-line-of-best-fit-in-python#:~:text=pyplot.,the%20line%20of%20best%20fit.
                x_3dB_vorPeak_nm = (y_3dB-b_vorPeak)/m_vorPeak
 
                #Jetzt das gleiche für die hintere Flanke
                if value_3dB_hinterPeak_dBm < y_3dB:
                    x1_index_hinterPeak_nm = index_3dB_hinterPeak_nm
                    y1_value_hinterPeak_dBm = value_3dB_hinterPeak_dBm 
                    x2_index_hinterPeak_nm = index_3dB_hinterPeak_nm + 0.05
                    #print(x2_index_nm)
                    x2_index_hinterPeak_nm = round(x2_index_hinterPeak_nm, 2)
                    #print(x2_index_hinterPeak_nm)
                    y2_value_hinterPeak_dBm = hinterPeak[x2_index_hinterPeak_nm]

                    


                #wenn der berechnete y_3dB wert kleiner ist als als der gefundene, der am
                #nächsten zu diesem wert liegt, dann den gefundenen wert nehmen und den nächsten wert nehmen,
                #der kleiner ist als der gefundene (der berechnete 3dB wert liegt zwischen diesen)
                if value_3dB_hinterPeak_dBm > y_3dB:
                    
                    x1_index_hinterPeak_nm = index_3dB_hinterPeak_nm
                    y1_value_hinterPeak_dBm = value_3dB_hinterPeak_dBm 
                    x2_index_hinterPeak_nm = index_3dB_hinterPeak_nm - 0.05
                    x2_index_hinterPeak_nm = round(x2_index_hinterPeak_nm,2)
                    y2_value_hinterPeak_dBm = hinterPeak[x2_index_hinterPeak_nm]
                    
                x_hinterPeak_fit_array = np.array([x1_index_hinterPeak_nm, x2_index_hinterPeak_nm])
                y_hinterPeak_fit_array = np.array([y1_value_hinterPeak_dBm,  y2_value_hinterPeak_dBm])
                

                m_hinterPeak, b_hinterPeak = np.polyfit(x_hinterPeak_fit_array, y_hinterPeak_fit_array,1) #https://www.kite.com/python/answers/how-to-plot-a-line-of-best-fit-in-python#:~:text=pyplot.,the%20line%20of%20best%20fit.
                x_3dB_hinterPeak_nm = (y_3dB-b_hinterPeak)/m_hinterPeak
                          
                bandbreite_3dB = x_3dB_hinterPeak_nm-x_3dB_vorPeak_nm
                bandbreite_3dB_list.append(bandbreite_3dB)
            except Exception as e:
                print('Fehlermeldung:', e) 
                bandbreite_3dB_list.append(np.NaN)
                peak_intensität_dB_list.append(np.NaN)
                peak_wellenlänge_nm_list.append(np.NaN)
      
        bandbreite_3dB_df = pd.Series(data=bandbreite_3dB_list, index=strom_liste, name ='Uabs = -'+ str(plot_df_voltage) +' V')
        
        return bandbreite_3dB_df

    
    def peak_wellenlaenge_nm(self, plot_df, plot_df_voltage):
        peak_wellenlänge_nm_list = []
        strom_liste = plot_df.columns
        for column_name in plot_df:
            try:
                y_max_index = plot_df[column_name].idxmax() #nm
                peak_wellenlänge_nm_list.append(y_max_index)
            except Exception as e:
                print('Fehlermeldung:', e)
                peak_wellenlänge_nm_list.append(np.NaN)
        peak_nm_df = pd.Series(data=peak_wellenlänge_nm_list, index= strom_liste, name ='Uabs = -'+ str(plot_df_voltage) +'V') #Dataframe mit eingestelltem strom und wellenlänge des Peaks 
        
        return peak_nm_df





    #Plot erstellen 
    def PlotData(self):
        print(self.DataFrame_ReadyToPlot())
        self.DataFrame_ReadyToPlot().set_index('Wavelength (nm)').plot()
        plt.show()


