from Mothership_class import Mother 
import pandas as pd
import os 

class pui_RawDataProcessing(Mother):
    def __init__(self, path_to_rawData):
        super().__init__(path_to_rawData)

    def pui_Dataframe(self):
        cleanData = self.loadRawData()  #Funktion aus der Mutterklasse
        cleanData.pop(0)
        column_names = ['Current (mA)', 
                        'Power (mW)', 
                        'Voltage (V)', 
                        'C_absorber (A)',
                        'Temperature (deg.C)']

        df = pd.DataFrame(cleanData, columns=column_names)
        df = df.set_index('Current (mA)')
        df = df[df.index.notnull()] #entfernt zeilen deren index nan ist

        return df





if __name__=='__main__':
    path = r'C:\Users\Ohse\Desktop\ACF\ACF_PUI\30C\PUI_070603_25-30C_02_0.00_1.00_0_G.dat'
    instanz = pui_RawDataProcessing(path)
    print(instanz.pui_Dataframe())