from Mothership_class import Mother 
import pandas as pd
import itertools
import numpy as np

class opt_RawDataProcessing(Mother):
    def __init__(self, path_to_rawData):
        super().__init__(path_to_rawData)
    

    def OptSpektrum_DataFrame(self):
         ###Rohdaten in Dataframe###
        cleanData=self.loadRawData()    #Funktion aus der Mutter Klasse 

        #Liste der Spaltennamen erstellen:
        current_name = 'Current (mA)'
        wl_name = 'Wavelength (nm)'
        intensity = 'Intensity (dBm)'
        c_absorber = 'C_absorber (A)'
        temperature = 'Temperature (deg.C)'
        column_names =[current_name, wl_name, intensity, c_absorber, temperature]

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

        #######Erstellen des finalen Dataframes für optische Spektren
        nach_strom_gruppiert = df.groupby(df.columns[0]) #hier wird nach dem strom der dataframe entstapelt 
        finalMesurementDataFrame_list = []
        for strom, multiindex in zip(strom_index_list,Multicolumnindex): #eine liste mit allen Messdaten Dataframes erstellen, die im folgenden dann nur noch zu einem Datenframe zusammengefühgt werden müssen
            df = nach_strom_gruppiert.get_group(strom)

            Current = np.array(df['Current (mA)'])
            Wavelength = np.array(df['Wavelength (nm)'])
            Intensity = np.array(df['Intensity (dBm)'])
            Absorber = np.array(df['C_absorber (A)'])
            Temperatur = np.array(df['Temperature (deg.C)'])

            df = pd.DataFrame(data=[Current, Wavelength, Intensity, Absorber, Temperatur]).T
            df.columns = multiindex
            finalMesurementDataFrame_list.append(df)
        #print(finalMesurementDataFrame_list)
        finalOpt_DataFrame = pd.concat(finalMesurementDataFrame_list, axis=1)
        return finalOpt_DataFrame

if __name__ == '__main__':
    path = r'C:\Users\Ohse\Desktop\AuswertungsTool\Gute messwerte\070603_SQW_RW_Labs200µm\SP\SP_070603_25C_01_0.00_0.00_0_S.dat'
    instanz = opt_RawDataProcessing(path)

    print(instanz.OptSpektrum_DataFrame())








