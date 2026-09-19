import PySimpleGUI as sg
from ordnerstruktur_class import OrdnerStruktur


class GUI_ELEMENTS():
    def __init__(self):
        pass

    def Rf_span_list(self, path_to_RawData):
        span_list = []
        if path_to_RawData != None:
            try:
                ordnerStruktur=OrdnerStruktur(path_to_RawData)
                Rf_dir = ordnerStruktur.Rf_dir()
                if Rf_dir == []:
                    pass
                else:
                    for element in  Rf_dir:
                        for key, value in element.items():
                            span = value[-11:]
                            span_list.append(span)
            except Exception as e:
                print('Rf option gui fail:')
                print(e)     
            return list(set(span_list))



    def open_folder(self):
        return [
                [sg.Text("Messwerte")],
                [
                 sg.In(size=(25,1), enable_events=True, key="-Ordner-"),
                 sg.FolderBrowse()
                ],
                [sg.Text("Todo")],
                [sg.Listbox(
                            values=[], enable_events=True, size=(32,4),
                            key="-Ordner Liste-"
                           )
                ]
              ]
    

    def pui_option_element(self):
        return  [
                sg.Frame('PUI',
                         [
                             [sg.CBox('Auswerten', default=False, key ='PUI')]       
                         ])
                ]
               
    
    def opt_option_element(self):
        return [
                sg.Frame('Optische Spektren',
                         [
                             [sg.CBox('Auswerten', default=False, key='OPT')],            
                             [sg.CBox("Normieren", default=False, key='OPT_normieren')]
                          ])
               ]
    
    def Rf_option_element(self):
        return [
                sg.Frame('Rf Spektren',
                          [
                             
                                [sg.CBox('Auswerten', default=True, key='-Rf-')],
                                [sg.Listbox(
                                    values=([]), 
                                    size=(20, 6),
                                    enable_events=True,
                                    key = '-Rf span-')],
                                [sg.Button("Aktualisieren")]
                           ])
                ]
    '''
    def Rf_option_element(self, path_to_RawData):
        span_list = self.Rf_span_list(path_to_RawData)
        print('span_list: ',span_list)
        sg_element_list =  []
        if span_list != None:
            for span in span_list:
                element = [sg.CBox(span, default=True, key=span)]
                sg_element_list.append(element)
        else:
            pass
        return [sg_element_list]
        #return [
        #        [sg.CBox(span, default=True, key=span)] 
        #        for span in span_list 
        #       ]
       ''' 




    def option_element(self):
        return [
                sg.Frame('PUI',
                         [
                             [sg.CBox('Auswerten', default=True, key ='PUI')]       
                         ]),
               sg.Frame('Optische Spektren',
                         [
                             [sg.CBox('Auswerten', default=True, key='OPT')],            
                             [sg.CBox("Normieren", default=True, key='OPT_normieren')]
                         ]),
                sg.Frame('Rf-Spektren',
                         [
                             [sg.CBox('Auswerten', default=True, key='Rf')],            
                             [sg.CBox("Fullspan", default=True, key='Rf_fullspan')]
                         ])
              ]

'''
def option_element(self):
        return [
                sg.Frame('PUI',
                         [
                             [sg.CBox('Auswerten', default=True, key ='PUI')]       
                         ]),
               sg.Frame('Optischespektren',
                         [
                             [sg.CBox('Auswerten', default=True, key='OPT')],            
                             [sg.CBox("Normieren", default=True, key='OPT_normieren')]
                         ])
              ]
'''