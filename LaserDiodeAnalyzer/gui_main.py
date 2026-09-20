#https://www.youtube.com/watch?v=-_z2RPAH0Qk&t=574s
import PySimpleGUI as sg
from gui_class import GUI_ELEMENTS
from pui_main import pui
from opt_main import opt 
from opt_main import normalize_opt_data_and_save_as_csv

# ---- Elements ----

start_auswertung = sg.Button("Auswertung Starten")
    
close = sg.Button("Schließen")

# ---- full layout ---- 
gui_elements = GUI_ELEMENTS()
full_layout = [   
               [
                sg.Column(gui_elements.open_folder()), 
                #sg.Frame('optionen',[gui_elements.option_element()]),
                sg.Frame('optionen',
                                    [[
                                       gui_elements.pui_option_element()[0],
                                       gui_elements.opt_option_element()[0],
                                       gui_elements.Rf_option_element()[0]
                                    ]])
               ],
               
                [close, start_auswertung]
               ]


window = sg.Window(title="Jiminy", layout=full_layout,grab_anywhere=False)#, margins=(100,50)

# ---- Main Loop ----
ordner_list = []
Rf_span_list = []
while True:
    event, values = window.read()

    print('event: ', event)
    print('values: ', values)

    
    if event == "Schließen" or event == sg.WIN_CLOSED:
        break
    # Auswertungsordner Pfad in eine Liste schreiben
    if event == "-Ordner-":
        print('Rf_spanlist ordner event anfang', Rf_span_list)
        # Ordner Mit Messwerten einlesen
        path_to_RawData = values["-Ordner-"]
        ordner_list.append(values["-Ordner-"])
        window["-Ordner Liste-"].update(ordner_list)
        
        # ListBox für Rf Spans die ausgewertet werden sollen 
        aktuelle_span_list = gui_elements.Rf_span_list(values["-Ordner-"]) 
        #print('aktuelle spanliste', aktuelle_span_list)
        Rf_span_list= Rf_span_list+aktuelle_span_list
        Rf_span_list = list(set(Rf_span_list))
        Rf_span_list_Listbox = Rf_span_list
        window['-Rf span-'].update(Rf_span_list_Listbox)

    if event == '-Rf span-': # wenn man auf ein element der listbox klickt wird es gelöscht
        help_list = Rf_span_list
      
        help_list.remove(values['-Rf span-'][0])
        Rf_span_list = help_list
        window['-Rf span-'].update(Rf_span_list)

    
    if event == 'Aktualisieren': #Aktualisieren der Rf span Listbox mit allen Rf spans, die in der ordnerliste gefunden werden
        alle_spans = []
        for element in ordner_list:
           alle_spans = alle_spans+gui_elements.Rf_span_list(element)
        Rf_span_list = list(set(alle_spans))
        window['-Rf span-'].update(Rf_span_list)
    
    if event == "Auswertung Starten":
        for path in ordner_list:
            if values['PUI']:
                pui(path)
            if values['OPT']:
                opt(path)         
            if values['OPT_normieren']:
                normalize_opt_data_and_save_as_csv(path)
            if values['-Rf-']:
                print(Rf_span_list)
              
        ordner_list = []
        window["-Ordner Liste-"].update(ordner_list)
        window['-Rf span-'].update([])
        print('Fertig')
                
        
    
window.close()
