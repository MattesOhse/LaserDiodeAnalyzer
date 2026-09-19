# Die x-achse ist durch das neue Messgerät nicht mehr für jede messung die gleiche
# Dies Muss berücksichtigt werden 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
from Mothership_class import Mother


class RfSpektren(Mother):
    def __init__(self, path_to_rawData, path_to_AuswertungsSubOrdner):
        super().__init__(path_to_rawData)
        self.path = path_to_AuswertungsSubOrdner
    

#############################################################################################
########## Datenframes zum Plotten Erstellen in dBm und mW, und PlotFunktionen ##############
#############################################################################################     
 # Für das Übersichtsspektrum  ist die x-Achse immer gleich
    # bei eingezoomten Spektren Variiert die x-Achse, da sich der Peak immer bei unterschiedlichen frequenzen befindet
    # Aus dem Übersichtsspektrum lässt sich eine HeatMap erstellen, aus den anderen (eingezoomten) Spektren nicht.
    # Aus den Aufgenommenen Übersichtsspektren wird aus dem ersten aufgenommenen Spektrum die x-Achse (frequenz) genommen 
    # und die Intensitästswerte der aufgenommenen Spektren einfach als folgene Spalten angehängt      
    def PlotDataDataFrame_dBm_full_spann(self):
        ## Erstellen eines DataFrames mit den zu plottenden Daten######
        x_values_df = self.Load_CleanRawData_from_CSV('Rf', self.path)['Frequency (GHz)']  #DataFrame 
        #print(x_values_df)
        x_axis = x_values_df.iloc[:, 0]  #Erstes Spalte des DataFrames (X-Achse)                    
        x_axis.name='Frequency (GHz)'
        y_values_df = self.Load_CleanRawData_from_CSV('Rf',self.path)['Intensity (dBm)']
        plot_df_dBm = pd.concat([x_axis, y_values_df], axis=1)
        plot_df_dBm = plot_df_dBm.set_index('Frequency (GHz)')
        return plot_df_dBm
    
    def PlotData_dBm_full_spann_normalized_df(self):    #normieren der dBm-übersichtsspektren 
        df = self.Load_CleanRawData_from_CSV('Rf', self.path)
        x = df['Frequency (GHz)']
        y = df['Intensity (dBm)']
        frequenz = x.iloc[:, 0]
        frequenz.name = 'Frequenz (GHz)'
        y_max=y.max()
        y_normiert = y.subtract(y_max, axis=1)
        y_normiert.index = frequenz
        return y_normiert

    def PlotDataDataFrame_mW_full_spann(self):
        x_values_df = self.Load_CleanRawData_from_CSV('Rf',self.path)['Frequency (GHz)'] #DataFrame 
        x_axis = x_values_df.iloc[:, 0]                     #Erstes Spalte des DataFrames (X-Achse)
        x_axis.name='Frequency (GHz)'
        y_values_df = self.Load_CleanRawData_from_CSV('Rf',self.path)['Intensity (dBm)']          
        ## Intensität von dBm in mW umrechnen#####
        y_df_mW = 10**(y_values_df/10)        
        ## Erstellen eines Datenframes mit Intensität in mW zum plotten und Plotten
        plot_df_mW = pd.concat([x_axis, y_df_mW], axis=1)
        plot_df_mW = plot_df_mW.set_index('Frequency (GHz)')
        #plot_df_mW.to_csv(self.path + 'Rf_plot_df_mW.csv')#Speichert die sen Datenframe in einer csv Datei im temp ordner, zur weiterverarbeitung (fitten)
        return plot_df_mW        
 
 # Für die eingezoomten Spektren  ist die x-Achse nicht immer gleich 
    def PlotDataDataFrame_dBm_zoomed_spann(self):
        ## Erstellen eines DataFrames mit den zu plottenden Daten######
        x_values_df = self.Load_CleanRawData_from_CSV('Rf',self.path)['Frequency (GHz)'] 
        #print(x_values_df)
        y_values_df = self.Load_CleanRawData_from_CSV('Rf',self.path)['Intensity (dBm)']
        #print(y_values_df)
        
        #Frequenz (x) und Intensität(y) für die verschiedenen messungen zusammenfühgen
        spektren_liste = []
        for (x,y) in zip(x_values_df, y_values_df):
            #neue zeile mit den Namen in die einzelnen Sieriesses einfühgen
            new_x_row = pd.Series('Frequency (GHz)')
            frequency = x_values_df[x]
            stromWert = frequency.name
            frequency = pd.concat([new_x_row, frequency]).reset_index(drop = True)
            new_y_row = pd.Series('Intensity (dBm)')   
            intensity = y_values_df[y] 
            intensity = pd.concat([new_y_row, intensity]).reset_index(drop = True) 
            
            spektrum = pd.concat([frequency,intensity],axis=1)
            spektrum.columns = [stromWert ,stromWert] #den einzelnen Spalten den eingestellten STrom als namen geben
            spektren_liste.append(spektrum)
        
        spektren_df = pd.concat(spektren_liste,axis=1)
        #print(spektren_df)
        return spektren_df

    def PlotDataDataFrame_mW_zoomed_spann(self):
        ## Erstellen eines DataFrames mit den zu plottenden Daten######
        x_values_df = self.Load_CleanRawData_from_CSV('Rf',self.path)['Frequency (GHz)'] 
        #print(x_values_df)
        y_values_df = self.Load_CleanRawData_from_CSV('Rf',self.path)['Intensity (dBm)']
        #print(y_values_df)
        y_values_df = 10**(y_values_df/10)

        #Frequenz (x) und Intensität(y) für die verschiedenen messungen zusammenfühgen
        spektren_liste = []
        for (x,y) in zip(x_values_df, y_values_df):
            #neue zeile mit den Namen in die einzelnen Sieriesses einfühgen
            new_x_row = pd.Series('Frequency (GHz)')
            frequency = x_values_df[x]
            stromWert = frequency.name
            frequency = pd.concat([new_x_row, frequency]).reset_index(drop = True)
            new_y_row = pd.Series('Intensity (dBm)')   
            intensity = y_values_df[y] 
            intensity = pd.concat([new_y_row, intensity]).reset_index(drop = True) 
            
            spektrum = pd.concat([frequency,intensity],axis=1)
            spektrum.columns = [stromWert ,stromWert] #den einzelnen Spalten den eingestellten STrom als namen geben
            spektren_liste.append(spektrum)
        
        spektren_df = pd.concat(spektren_liste,axis=1)
        #print(spektren_df)
        return spektren_df








#############################################################################################
########## Daten mit Lorentz Fitten #########################################################
#############################################################################################
## Define Lorentz Fitfunction####
#Names: xc, w, A
#Meanings: y0= offset, xc = center, w = FWHM, A = Amplitude
#Lower Bounds: w > 0.0
#Upper Bounds: none

    def Lorentz(self, x, y0, xc, w, A): 
        return y0+((w*A)/(4*(x-xc)**2+w**2))



    #Gibt einen Dataframe mit den Fitparametern zurück#########
    #Geht nur, wenn die Intensität in mW umgerechnet ist
    def DatenFitten(self, plot_df):
        current_list=list(plot_df.columns)
        del current_list[::2]
        #print(current_list)
        
        fit_parameters = []
        fit_parameters_zusammenfassung = []

        for current in current_list:
            aktuelles_spektrum = plot_df[current]
            #print(aktuelles_spektrum)
            aktuelles_spektrum = aktuelles_spektrum.iloc[1: , :] #Erste zeile des Dataframes löschen, weil da der Name der Spalten drin steht  
            aktuelles_spektrum.index = aktuelles_spektrum.iloc[:, 0] #frequenz als index setzen
            aktuelles_spektrum = aktuelles_spektrum.iloc[: , 1:] #erste spalte löschen, weil da noch die frequenz drin steht
            aktuelles_spektrum = aktuelles_spektrum.squeeze() #Den Dataframe zu einer Series machen
            aktuelles_spektrum = pd.to_numeric(aktuelles_spektrum) #Werte der Series in ein nummerisches Format bringen 
            aktuelles_spektrum.index = pd.to_numeric(aktuelles_spektrum.index, errors='coerce') #den index in ein nummerisches Format bringen
            
            x_values = aktuelles_spektrum.index

            try:
                #####Fit_startvalues guess###
                #https://stackoverflow.com/questions/31553265/python-curve-fit-does-not-give-reasonable-fitting-result
                y0_guess= aktuelles_spektrum.min() 
                A_guess = aktuelles_spektrum.max()
                xc_guess = aktuelles_spektrum.idxmax()

                pos_half = aktuelles_spektrum-A_guess/2
                pos_half = pos_half.abs().argmin()
                w_guess = np.abs(xc_guess - x_values[pos_half])
                #print(current, 'mA ', 'y0_guess: ', str(y0_guess) , 'A_guess: ', str(A_guess), 'xc_guess: ', str(xc_guess), 'FWHM: ', str(w_guess))
                
                param_guess =[y0_guess,xc_guess,w_guess,A_guess]
                param_guess =[y0_guess,xc_guess,w_guess,A_guess]
                popt, pcov = scipy.optimize.curve_fit(
                                                        self.Lorentz, 
                                                        x_values,
                                                        aktuelles_spektrum,
                                                        p0=param_guess,
                                                        maxfev=1000 #Maximale anzahl der Iterationen. Standard wert ist 800
                                                      )
                y0, xc, w, A = popt
                standard_errors = np.sqrt(pcov.diagonal()) #https://stackoverflow.com/questions/25234996/getting-standard-error-associated-with-parameter-estimates-from-scipy-optimize-c
                y0_err, xc_err, w_err, A_err = standard_errors

           
                parameter_list = [y0, y0_err, xc, xc_err, w, w_err, A, A_err]
                parameter_zusammenfassung_list = [y0, xc, w, A]

                #print(current, 'mA ', 'y0_real: ', str(y0) , 'A_real: ', str(A), 'xc_real: ', str(xc), 'FWHM_real', str(w))

                fit_parameters.append(parameter_list)
                fit_parameters_zusammenfassung.append(parameter_zusammenfassung_list)

            except Exception as e: #Wenn Fitten nicht funktioniert
                print(e)
                y0, xc, w, A = np.NaN, np.NaN, np.NaN, np.NaN
                y0_err, xc_err, w_err, A_err = np.NaN, np.NaN, np.NaN, np.NaN

                parameter_list = [y0, y0_err, xc, xc_err, w, w_err, A, A_err]
                parameter_zusammenfassung_list = [y0, xc, w, A]

                fit_parameters.append(parameter_list)
                fit_parameters_zusammenfassung.append(parameter_zusammenfassung_list)


        fitparameter_alles_df = pd.DataFrame(fit_parameters, 
                        columns=['y_0','+-y0_err', 'Center Frequency (GHz)','+-xc_err', 'FWHM (GHz)','+-w_err', 'Amplitude','+-A_err'],
                        index = current_list) 

        fitparameter_zusammenfassung_df = pd.DataFrame(fit_parameters_zusammenfassung, 
                            columns=['y_0', 'Center Frequency (GHz)', 'FWHM (GHz)','Amplitude'],
                            index = current_list)
        
        #print(fitparameter_zusammenfassung_df)
        return [fitparameter_alles_df, fitparameter_zusammenfassung_df]

            
                

'''
    #Erstellt die y werte des Fits aus den Fitparametern und packt sie 
    #mit der Frequenz (x-Achse) in einen Datenframe
    def FitDfErstellen(self,fit_parameters_df):
        #fitparameter_df =self.DatenFitten()
        x_y_values_fit_list = []
        for current in fit_parameters_df.index:          
            y0 = fit_parameters_df.loc[current]['y_0']
            A = fit_parameters_df.loc[current]['Amplitude']
            xc = fit_parameters_df.loc[current]['Center Frequency (GHz)']
            w = fit_parameters_df.loc[current]['FWHM (GHz)']
            
            #print(str(xc))
            #print(type(xc))
            if np.isnan(xc)==True:
                pass
            else:
                x_axis_list = np.arange(xc-0.005, xc+0.005, 0.00001)
                y_fit_list = self.Lorentz(x_axis_list, y0, xc, w, A)
                x_y_dict = {
                            'Frequency (GHz)': x_axis_list, 
                            'Intensity' : y_fit_list
                            }

                multiindex = pd.MultiIndex.from_tuples(
                                                        [
                                                            (current,'Frequency (GHz)'), 
                                                            (current,'Intensity')
                                                        ], 
                                                        names=['Strom', 'Fit'])
                x_y_values_df= pd.DataFrame(x_y_dict)
                x_y_values_df.columns=multiindex
                x_y_values_fit_list.append(x_y_values_df)


        x_y_values_fit_df = pd.concat(x_y_values_fit_list, axis=1)
        return x_y_values_fit_df

            
    #Plotten der Messwerte zusammen mit ihrem Fit. 
    #Übereinander andordnen der spektren (inkrement +0.2 mw)
    def PlotDataWithFit(self, fit_parameters_df):      
        
        rawData_df = self.PlotDataDataFrame_mW()#.set_index('Frequency (GHz)')
        fitData_df = self.FitDfErstellen(fit_parameters_df)

        ##Rawdata Spektren übereinanderlegen (Auf y-Achse versetzen)#######
        columnName_list = rawData_df.columns
        x0_rawData = 0  #um spektren übereinander zu legen 
        
        for column in columnName_list:
           newIntensity = x0_rawData + rawData_df[column]
           rawData_df[column]=newIntensity        
           x0_rawData += 0.001     

        plt.plot(rawData_df)
    
        # Fitdaten übereinanderlegen (Auf y-Achse veretzen)########
        stromValuesIndex_FitDf_list = list(fitData_df.columns.get_level_values('Strom'))
        x0_fitData = 0 
        del stromValuesIndex_FitDf_list[::2] #löscht jedes zweite element der liste, weil in der liste jeder stromwert doppelt ist. liegt am multiindex.  das löschen ist nicht schön, besser machen. aber erstmal getting shit done
        for columnIndex in stromValuesIndex_FitDf_list:
            fit_series = fitData_df[columnIndex].set_index('Frequency (GHz)')
            newFitIntensity = x0_fitData +fit_series
            x0_fitData += 0.1
            plt.plot(newFitIntensity)

        plt.show()                
           
'''            

