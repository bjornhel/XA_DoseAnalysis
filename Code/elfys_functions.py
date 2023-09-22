






"""
# Remove unwanted categories:
procedures_to_drop = [  'RGV Hjerte Høyre Kat.',
                        'RGA Hjertebiopsi - TX',
                        'RGV Cor Hø kat, måling av trykk og flow i lille kretsløp ved hje',
                        'RGV Cor Biopsi høyre ventrikkel (int.)',
                        'RGA Hjertebiopsi - Diagn.',
                        'RGV Cor Høyresidig hjertekateterisering (int.)',
                        'RGA Uspes. lok. interv.',
                        'RGA Revisjon av ledning',
                        'MIG_Ukjent US fremtidig',
                        'RGA Overex. Annen intervensjon (int.)',
                        'RGA Generatorbytte (PM)',
                        'RGA Generatorbytte (ICD)',
                        'RGA Cor Revisjon av elektroder (int.)',
                        'RGA Uspes. lok.',
                        'RGA Cor Koronarangiografi (int.)',
                        'RG Thorax',
                        'RGA Cor Biopsi venstre ventrikkel (int.)',
                        'RGA Biopsi m/høyre kat.',
                        'RGV Cor Temporær PM (int.)',
                        'RGA Abd. interv.',
                        'RGV Hode / Hals interv.']

data = data[~data['Protocol Description'].isin(procedures_to_drop)]

# Remove all categories that have zero entries from the categorical variable:
procedure_count = data['Protocol Description'].value_counts()
categories_to_remove = procedure_count[procedure_count == 0].index.tolist()
data['Protocol Description'] = data['Protocol Description'].cat.remove_categories(categories_to_remove)

# Clean up:
del procedures_to_drop, procedure_count, categories_to_remove

# This section will map similar procedures into the same category:
# Create a dictionary with the procedures to be mapped:
mapping = { 'RGA Ablasjon SVT'                  : 'RGA Cor Ablasjon SVT (int.) m og u 3D',
            'RGA Cor Ablasjon SVT (int.)'       : 'RGA Cor Ablasjon SVT (int.) m og u 3D',
            'RGA Cor Ablasjon SVT m 3D (int.)'  : 'RGA Cor Ablasjon SVT (int.) m og u 3D',
            
            'RGA Ablasjon Atrieflimmer'                 : 'RGA Cor Ablasjon Atrieflimmer (int.) m og u 3D',
            'RGA Cor Ablasjon Atrieflimmer (int.)'      : 'RGA Cor Ablasjon Atrieflimmer (int.) m og u 3D',
            'RGA Cor Ablasjon Atrieflimmer med 3D (int.)' : 'RGA Cor Ablasjon Atrieflimmer (int.) m og u 3D',

            'RGA Ablasjon Atrieflutter'         : 'RGA Cor Ablasjon Atrieflutter (int.)',

            'RGA Ablasjon VT'                   : 'RGA Cor Ablasjon VT m 3D (int.)',

            'RGA CRYO Ablasjon Atrieflimmer'    : 'RGA Cor Cryo Ablasjon Atrieflimmer (int.)',

            'RGA Elfys SVT'                     : 'RGA Cor Elfys VT el. SVT (int.)',
            'RGA Cor Elfys SVT (int.)'          : 'RGA Cor Elfys VT el. SVT (int.)',
            'RGA Elfys VT'                      : 'RGA Cor Elfys VT el. SVT (int.)',
            'RGA Cor Elfys VT (int.)'           : 'RGA Cor Elfys VT el. SVT (int.)',

            'RGA CRT-D'                         : 'RGA Cor CRT-D (int.)',

            'RGA CRT-P'                         : 'RGA Cor CRT-P (int.)',

            'RGA ICD1'                              : 'RGA Cor Implantasjon PM/ICD (int.) ink. 2k og 1k PM',

            'RGA ICD2'                              : 'RGA Cor Implantasjon PM/ICD (int.) ink. 2k og 1k PM',
            'RGA PM1'                               : 'RGA Cor Implantasjon PM/ICD (int.) ink. 2k og 1k PM',
            'RGA PM2'                               : 'RGA Cor Implantasjon PM/ICD (int.) ink. 2k og 1k PM',
            'RGA TPM'                               : 'RGA Cor Implantasjon PM/ICD (int.) ink. 2k og 1k PM',
            'RGA Cor 2-k PM (int.)'                 : 'RGA Cor Implantasjon PM/ICD (int.) ink. 2k og 1k PM',
            'RGA Cor 1-k PM (int.)'                 : 'RGA Cor Implantasjon PM/ICD (int.) ink. 2k og 1k PM',
            'RGA Cor Implantasjon PM/ICD (int.)'    : 'RGA Cor Implantasjon PM/ICD (int.) ink. 2k og 1k PM'}

data['Protocol Description'] = data['Protocol Description'].replace(mapping)

# Clean up:
del mapping

"""