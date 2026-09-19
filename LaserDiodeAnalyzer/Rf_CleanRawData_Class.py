#https://pandas.pydata.org/pandas-docs/stable/user_guide/cookbook.html#cookbook-multi-index
from Mothership_class import Mother
import pandas as pd
import itertools
import numpy as np

class RawDataProcessing(Mother):
    def __init__(self, path_to_rawData):
        super().__init__(path_to_rawData)


    def RfSpektrum_DataFrame(self):
        ###Rohdaten in Dataframe###
        cleanData=self.loadRawData()    #Funktion aus Mutterklasse 
        #Liste der Spaltennamen erstellen:
        i=0
        column_names =[]
        while i < len(cleanData[0]):    
            first = cleanData[0][i]
            i+=1
            second = cleanData[0][i]
            i+=1
            column_names.append(first+ ' ' +second)

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
        #print(strom_index_list)

        #######Erstellen einer liste mit den Mullticolumn indexen######
        Multicolumnindex = []
        for x in strom_index_list:  #erstellen einer liste der Spalten namen mit den jeweiligen Stromwerten
            column_index = pd.MultiIndex.from_product([list(df.columns),[x]], 
                                                       names=["Messwerte", "Stromwert"])
            Multicolumnindex.append(column_index)
        #print(Multicolumnindex)

        #######Erstellen des finalen Dataframes für Rf Spektren
        nach_strom_gruppiert = df.groupby(df.columns[0]) #hier wird nach dem strom der dataframe entstapelt 

        finalMesurementDataFrame_list = []
        for strom, multiindex in zip(strom_index_list,Multicolumnindex): #eine liste mit allen Messdaten Dataframes erstellen, die im folgenden dann nur noch zu einem Datenframe zusammengefühgt werden müssen
            df = nach_strom_gruppiert.get_group(strom)
            #print(df)
            Current = np.array(df['Current (mA)'])
            Frequency = np.array(df['Frequency (GHz)'])
            Intensity = np.array(df['Intensity (dBm)'])
            C_absorber = np.array(df['C_absorber (A)'])
            Temperature = np.array(df['Temperature (deg.C)'])

            df = pd.DataFrame(data=[Current, Frequency, Intensity, C_absorber, Temperature]).T
            df.columns = multiindex
            finalMesurementDataFrame_list.append(df)

        #print(finalMesurementDataFrame_list)
        final_Rf_DataFrame = pd.concat(finalMesurementDataFrame_list, axis=1)

        return final_Rf_DataFrame

    






if __name__ == "__main__":
    path = r'C:\Users\Ohse\Desktop\Rf_smallSpan\KleinerDatensatz/SP_020205_30C_01_0.00_0.00_0_RF1.000e+08Hz.dat'
    #name = 'SP_020205_30C_01_0.00_0.00_0_RF1.000e+08Hz.dat'
    x=RawDataProcessing(path)
    print(x.RfSpektrum_DataFrame())
