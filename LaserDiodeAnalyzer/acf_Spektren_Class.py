import pandas as pd
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
from Mothership_class import Mother


class acf_Spektren(Mother):
    def __init__(self, path_to_rawData, path_to_AuswertungsSubOrdner):
        super().__init__(path_to_rawData)
        self.path = path_to_AuswertungsSubOrdner

 
#############################################################################################
########## Datenframes zum Plotten Erstellen  ###############################################
#############################################################################################
    def PlotDataDataFrame(self):
        x_values_df = self.Load_CleanRawData_from_CSV('acf', self.path)['Zeit (ps)']

        x_axis = x_values_df.iloc[:, 0]  #Erstes Spalte des DataFrames (X-Achse)
        x_axis.name='Zeit (ps)'

        y_values_df = self.Load_CleanRawData_from_CSV('acf', self.path)['Intensity']
        plot_df = pd.concat([x_axis, y_values_df], axis=1)
        plot_df = plot_df.set_index('Zeit (ps)')
        return plot_df       

#############################################################################################
########## Intensitäten auf 1 Normieren Fitten #########################################################
#############################################################################################
    def Normalize(self):
        df = self.PlotDataDataFrame()
        normalized_df=(df-df.min())/(df.max()-df.min())
        return normalized_df

#############################################################################################
########## Daten mit sech^2 Fitten #########################################################
#############################################################################################
#Names: y0, xc, A, w
#Meanings: y0 = y_Minimum, xc = center, A = Amplitude, w = FWHM
    def Sech_2(self, x, y0, xc, A, w):
        return y0 + A / (np.cosh(1.7627*(x-xc)/w))**2

    #Gibt einen DataFrame mit den Fitparametern zurück#########
    def DatenFitten(self, plot_df_normalized):#, fit_startValues_list):
        x = plot_df_normalized.index
        y = plot_df_normalized
        
        fit_parameters =[]
        fit_parameters_zusammenfassung = []
        current_list = plot_df_normalized.columns #liste der eingestellten Gainstrom-stärken

        for column in current_list:
            try:
                #####Fit_startvalues guess###
                #https://stackoverflow.com/questions/31553265/python-curve-fit-does-not-give-reasonable-fitting-result
                y0_guess = y[column].min()
                xc_guess = y[column].idxmax()
                A_guess = y[column].max()
                w_guess = 5 #das irgendwie noch smart abschätzen

                param_guess =[y0_guess,xc_guess,A_guess,w_guess] 
                popt, pcov = optimize.curve_fit(
                                                self.Sech_2,
                                                x,
                                                y[column],
                                                p0=param_guess,
                                                maxfev=5000 #Maximale anzahl der Iterationen. Standard wert ist 800
                                                )

                
   
                y0, xc, A, w = popt
                standard_errors = np.sqrt(pcov.diagonal()) #https://stackoverflow.com/questions/25234996/getting-standard-error-associated-with-parameter-estimates-from-scipy-optimize-c
                y0_err, xc_err, A_err, w_err = standard_errors
            
                parameter_list = [y0, y0_err, xc, xc_err, A, A_err, w, w_err]
                parameter_zusammenfassung_list = [y0, xc, A, w] 

                fit_parameters.append(parameter_list)
                fit_parameters_zusammenfassung.append(parameter_zusammenfassung_list)

            except Exception as e:  #Wenn fitten nicht funktioniert
                print('Fehler: ', e)
                y0, xc, A, w = np.NaN, np.NaN, np.NaN, np.NaN 
                y0_err, xc_err, A_err, w_err = np.NaN, np.NaN, np.NaN, np.NaN
                
                parameter_list = [y0, y0_err, xc, xc_err, A, A_err, w, w_err]
                parameter_zusammenfassung_list = [y0, xc, A, w]
                
                fit_parameters.append(parameter_list)
                fit_parameters_zusammenfassung.append(parameter_zusammenfassung_list)
        
        fitparameter_alles_df = pd.DataFrame(fit_parameters, 
                        columns=['y_Minimum','+-y0_err', 'Center Zeit (ps)','+-xc_err', 'Amplitude','+-A_err', 'FWHM (ps)','+-w_err'],
                        index = current_list) 
        
        fitparameter_zusammenfassung_df = pd.DataFrame(fit_parameters_zusammenfassung, 
                        columns=['y_Minimum', 'Center Zeit (ps)', 'Amplitude', 'FWHM (ps)'],
                        index = current_list)             
        
        return [fitparameter_alles_df, fitparameter_zusammenfassung_df]



































    #Erstellt die y werte des Fits aus den Fitparametern und packt sie 
    #mit der Zeit (x-Achse) in einen Datenframe
    def FitDfErstellen(self, fit_parameters_df):
        x_y_values_fit_list = []
        for current in fit_parameters_df.index:
            y0 = fit_parameters_df.loc[current]['y_Minimum']
            xc = fit_parameters_df.loc[current]['Center Zeit (ps)']
            A = fit_parameters_df.loc[current]['Amplitude']
            w = fit_parameters_df.loc[current]['FWHM (ps)']

            if np.isnan(y0):
                #print('alles soll nan sein ', 'y0 = ', y0, 'xc = ', xc, 'A = ', A, 'w = ', w)
                x_y_dict = {
                            'Zeit (ps)': [np.nan], 
                            'Intensity' : [np.nan]
                            }
            else:
                #print(type(y0))
                #print('alles soll != nan sein ', 'y0 = ', y0, 'xc = ', xc, 'A = ', A, 'w = ', w)
                x_axis_list = np.arange(xc-15, xc+15, 0.1)
                y_fit_list = self.Sech_2(x_axis_list, y0, xc, A, w)
                x_y_dict = {
                            'Zeit (ps)': x_axis_list, 
                            'Intensity' : y_fit_list
                            }
            
            multiindex = pd.MultiIndex.from_tuples(
                                                    [
                                                        (current,'Zeit (ps)'), 
                                                        (current,'Intensity')
                                                    ], 
                                                    names=['Strom', 'Fit'])
            x_y_values_df= pd.DataFrame(x_y_dict)
            x_y_values_df.columns=multiindex
            x_y_values_fit_list.append(x_y_values_df)

        x_y_values_fit_df = pd.concat(x_y_values_fit_list, axis=1)
        return x_y_values_fit_df
    
    #Plotten der Messwerte zusammen mit ihrem Fit. 
    #Übereinander andordnen der spektren (inkrement +1)
    def PlotDataWithFit(self, fit_parameters_df):
        rawData_df = self.Normalize()#.set_index('Zeit (ps)')
        fitData_df = self.FitDfErstellen(fit_parameters_df)

        ##Rawdata Spektren übereinanderlegen (Auf y-Achse versetzen)#######
        columnName_list = rawData_df.columns
        y0_rawData = 0  #um spektren übereinander zu legen 
        for column in columnName_list:
           newIntensity = y0_rawData + rawData_df[column]
           rawData_df[column]=newIntensity        
           y0_rawData += 1     

        plt.plot(rawData_df)

        #######Hier muss das gleiche noch mit den Fits gemacht werden
        stromValuesIndex_FitDf_list = list(fitData_df.columns.get_level_values('Strom'))
        y0_fitData = 0 
        del stromValuesIndex_FitDf_list[::2] #löscht jedes zweite element der liste, weil in der liste jeder stromwert doppelt ist. liegt am multiindex.  das löschen ist nicht schön, besser machen. aber erstmal getting shit done
        for columnIndex in stromValuesIndex_FitDf_list:
            fit_series = fitData_df[columnIndex].set_index('Zeit (ps)')
            newFitIntensity = y0_fitData +fit_series
            y0_fitData += 1
            plt.plot(newFitIntensity)



        plt.show()

    ###### Bestimmtheitsmaß Kor. R-Quadrat######




