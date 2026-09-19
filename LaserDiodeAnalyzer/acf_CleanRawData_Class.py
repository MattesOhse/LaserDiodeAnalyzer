#https://pandas.pydata.org/pandas-docs/stable/user_guide/cookbook.html#cookbook-multi-index
from Mothership_class import Mother
import pandas as pd
import itertools
import numpy as np

class acf_RawDataProcessing(Mother):

    def __init__(self, path_to_rawData):
        super().__init__(path_to_rawData)
    

    def ACFSpektrum_DataFrame(self):
        ###Rohdaten in Dataframe###
        cleanData=self.loadRawData()    #funktion ist aus der Mutterklasse

            #Liste der Spaltennamen erstellen:

        column_names =['Current (mA)', 'Zeit (ps)', 'Intensity', 
                       'Tau', 'C_absorber (A)', 'Temperature (deg.C)']


        cleanData.pop(0)
        df = pd.DataFrame(cleanData, columns=column_names)
        #print(df)  

        #####Liste der eingestellten stromwerte Erstellen####
        strom_index_list = []
        aktuellerstromwert = 0
        for x in df[df.columns[0]].items():     #erstellen der liste mit den verschiedenen, eingestellten stromwerten
            strom = x[1]
            if strom != aktuellerstromwert and strom != None:
                aktuellerstromwert = strom
                strom_index_list.append(aktuellerstromwert)
            else:
                pass           


        #######Erstellen einer liste mit den Mullticolumn indexen######
        Multicolumnindex = []
        for x in strom_index_list:  #erstellen einer liste der Spalten namen mit den jeweiligen Stromwerten
            column_index = pd.MultiIndex.from_product([list(df.columns),[x]], 
                                                       names=["Messwerte", "Stromwert"])
            Multicolumnindex.append(column_index)
        #print(Multicolumnindex) 

        #######Erstellen des finalen Dataframes für ACF Spektren
        nach_strom_gruppiert = df.groupby(df.columns[0]) #hier wird nach dem strom der dataframe entstapelt 
        finalMesurementDataFrame_list = []
        for strom, multiindex in zip(strom_index_list,Multicolumnindex): #eine liste mit allen Messdaten Dataframes erstellen, die im folgenden dann nur noch zu einem Datenframe zusammengefühgt werden müssen
            df = nach_strom_gruppiert.get_group(strom)        

            Current = np.array(df['Current (mA)'])
            Zeit = np.array(df['Zeit (ps)'])
            Intensity = np.array(df['Intensity'])
            Tau = np.array(df['Tau'])
            C_absorber = np.array(df['C_absorber (A)'])
            Temperature = np.array(df['Temperature (deg.C)'])      

            df = pd.DataFrame(data=[Current, Zeit, Intensity, Tau, C_absorber,Temperature]).T
            df.columns = multiindex
            finalMesurementDataFrame_list.append(df)
        #print(finalMesurementDataFrame_list)
        finalACF_DataFrame = pd.concat(finalMesurementDataFrame_list, axis=1)
        finalACF_DataFrame = finalACF_DataFrame.iloc[:-2] #letzte beiden zeilen des dataFrames wegen den intensitätssprüngen löschen
        return finalACF_DataFrame




'''

if __name__ == "__main__":
    path = 'MesurmentData/C3628-6-1_835nm/Las020504_ACPM_150µm/'
    name = 'RFOpt_25°C_Uab0-1V_Ig01-03A_01_0.00_0.50_0_S.dat'
    x=RawDataProcessing(path, name)
    print(x.OptSpektrum_DataFrame())
'''