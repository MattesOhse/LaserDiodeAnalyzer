#Prinzipiell sind alle Methoden gleich, bis auf die Dateinamen
import os
from os import listdir
from os.path import isfile, join

class OrdnerStruktur():
    def __init__(self, folder_path):
        self.folder_path = folder_path

    #SubSub directorys mit messlaufnummer und Absorberspannung in opt erstellen
    #Rückgabewert ist eine liste bestehend aus dictionarys, deren Schlüssel 
    #der Dateiname der rohdaten deren schloss der Pfad zum entsprechenden unterordner ist
    #in die die Auswertung gespeichert wird
    def opt_dir(self):
        opt_dir = self.folder_path + '/Auswertung/' + 'Opt/'
        rückgabe_wert_list = [] #[{pfad zu rohdatenDatei : pfad zu sub ordner},...]
        temp_dict = {} #dictionariy, dass in die rückgabe_wert_list geschrieben wird
        opt_file_list = []
        onlyfiles = [f for f in listdir(self.folder_path) if isfile(join(self.folder_path, f))]

        for file in onlyfiles:
            if 'S.dat' in file:
                opt_file_list.append(file)

        for file in opt_file_list:
            sub_ordner_name = file.replace('S.dat', '')
            sub_ordner_name = sub_ordner_name[-16:]

            if not os.path.exists(opt_dir+sub_ordner_name):
                os.makedirs(opt_dir+sub_ordner_name)
            temp_dict = {self.folder_path+file : opt_dir+sub_ordner_name}
            rückgabe_wert_list.append(temp_dict)
        
        return rückgabe_wert_list


    #SubSub directorys mit messlaufnummer und Absorberspannung in pui erstellen
    #Rückgabewert ist eine liste bestehend aus dictionarys, deren Schlüssel 
    #der Dateiname der rohdaten deren schloss der Pfad zum entsprechenden unterordner ist
    #in die die Auswertung gespeichert wird
    def pui_dir(self):
        pui_dir = self.folder_path + '/Auswertung/' + 'PUI/'
        rückgabe_wert_list = [] #[{pfad zu rohdatenDatei : pfad zu sub ordner},...]
        temp_dict = {} #dictionariy, dass in die rückgabe_wert_list geschrieben wird
        pui_file_list = []
        onlyfiles = [f for f in listdir(self.folder_path) if isfile(join(self.folder_path, f))]

        for file in onlyfiles:
            if 'G.dat' in file:
                pui_file_list.append(file)

        for file in pui_file_list:
            sub_ordner_name = file.replace('G.dat', '')
            sub_ordner_name = sub_ordner_name[-16:]

            if not os.path.exists(pui_dir+sub_ordner_name):
                os.makedirs(pui_dir+sub_ordner_name)
            temp_dict = {self.folder_path+file : pui_dir+sub_ordner_name}
            rückgabe_wert_list.append(temp_dict)
        
        return rückgabe_wert_list


    #SubSub directorys mit messlaufnummer und Absorberspannung in ACF erstellen
    #Rückgabewert ist eine liste bestehend aus dictionarys, deren Schlüssel 
    #der Dateiname der rohdaten deren schloss der Pfad zum entsprechenden unterordner ist
    #in die die Auswertung gespeichert wird
    def acf_dir(self):
        acf_dir = self.folder_path + '/Auswertung/' + 'ACF/'
        rückgabe_wert_list = [] #[{pfad zu rohdatenDatei : pfad zu sub ordner},...]
        temp_dict = {} #dictionariy, dass in die rückgabe_wert_list geschrieben wird
        acf_file_list = []
        onlyfiles = [f for f in listdir(self.folder_path) if isfile(join(self.folder_path, f))]

        for file in onlyfiles:
            if 'ACF.dat' in file:
                acf_file_list.append(file)
 
        for file in acf_file_list:
            sub_ordner_name = file.replace('ACF.dat', '')
            sub_ordner_name = sub_ordner_name[-16:]      

            if not os.path.exists(acf_dir+sub_ordner_name):
                os.makedirs(acf_dir+sub_ordner_name)
            temp_dict = {self.folder_path+file : acf_dir+sub_ordner_name}
            rückgabe_wert_list.append(temp_dict)
        
        return rückgabe_wert_list


    #SubSub directorys mit messlaufnummer und Absorberspannung in Rf erstellen
    #Rückgabewert ist eine liste bestehend aus dictionarys, deren Schlüssel 
    #der Dateiname der rohdaten deren schloss der Pfad zum entsprechenden unterordner ist
    #in die die Auswertung gespeichert wird
    def Rf_dir(self):
        Rf_SmallSpan_dir = self.folder_path + '/Auswertung/' + 'Rf/'
        
        rückgabe_wert_list = [] #[{pfad zu rohdatenDatei : pfad zu sub ordner},...]
        temp_dict = {} #dictionariy, dass in die rückgabe_wert_list geschrieben wird
        Rf_file_list = []
        onlyfiles = [
                        f for f in listdir(self.folder_path) 
                        if isfile(join(self.folder_path, f))
                    ]


        #die Datei namen  in eine liste schreiben (also die auszuwertenden Dateien)
        for file in onlyfiles:
            if 'RF' in file:
                Rf_file_list.append(file)
        
        for file in Rf_file_list:
            sub_ordner_name = file.replace('.dat', '')
            sub_ordner_name = sub_ordner_name[-29:]  


            if not os.path.exists(Rf_SmallSpan_dir+sub_ordner_name):
                os.makedirs(Rf_SmallSpan_dir+sub_ordner_name)
            temp_dict = {self.folder_path+file : Rf_SmallSpan_dir+sub_ordner_name}
            rückgabe_wert_list.append(temp_dict)
        
        return rückgabe_wert_list
