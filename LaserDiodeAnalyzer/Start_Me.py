from acf_main import ACF
from pui_main import pui
from opt_main import opt
from Rf_main import Rf
from PeakPower_PulsBreite import PeakPower_Pulsbreite

# Achtung, wenn der Spannungswert im Dateinamen der Messwerte 
# mehr oder weniger als 7 zeichen besitzt gibt es Probleme
# bei den Rf Messungen im Messprogram nicht im Dateinamen RF eingeben


path_list = [
                r'C:\Users\matte\Desktop\Programmieren\MA_Auswertungstool\small_testdataset'
                
            ]

for path in path_list:
    opt(path)
    Rf(path)
    pui(path)
    ACF(path)
    PeakPower_Pulsbreite(path)







