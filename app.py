from tkinter import filedialog as fd
from datetime import datetime
import tkinter as tk
import zipfile
import random
import json
import eel

eel.browsers.set_path('chrome', 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')

eel.init('web')



@eel.expose
def get_random_name():
    eel.prompt_alerts('Random name')

@eel.expose
def get_random_number():
    eel.prompt_alerts(random.randint(1, 100))

@eel.expose
def get_date():
    eel.prompt_alerts(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

@eel.expose
def get_ip():
    eel.prompt_alerts('127.0.0.1')

@eel.expose
def saveFlow(newFlow):

    print(type(newFlow))

    # Subtituir nome e site
    manifest = json.loads(json.dumps(newFlow['flowManifest']).replace(newFlow['flowName']['old'], newFlow['flowName']['new']))
    definition = json.loads(json.dumps(newFlow['flowDefinition']).replace(newFlow['flowSite']['old'], newFlow['flowSite']['new']))

    newFileName = manifest['details']['displayName'].replace(' ', '_') + '.zip'
    print(newFileName)

    # print('Nome: ')
    # print(manifest['details']['displayName'])
    # print('Site: ')
    # print(definition['properties']['definition']['actions']['Parâmetros']['inputs']['Site'])

    # Salvar arquivo (tenha apenas manifest e definition)
    with zipfile.ZipFile(newFlow.filePath) as inzip, zipfile.ZipFile(newFileName, "w") as outzip:
        pass

@eel.expose
def btn_ResimyoluClick():
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    filetypes = (
        ('zip files', '*.zip'),
        ('All files', '*.*')
    )

    zipInformation = {
        'error': False,
        'messageError': '',
        'fullPath': '',
        'fileName': '',
        'flowName': '',
        'flowId': '',
        'flowManifest': {},
        'flowDefinition': {},
        'parameters': {
            'site': ''
        }
    }

    zipInformation['fullPath'] = fd.askopenfilename(filetypes=filetypes)

    try:
        with zipfile.ZipFile(zipInformation['fullPath']) as z:
            if 'manifest.json' in z.namelist():
                zipInformation['error'] = False
                zipInformation['messageError'] = ''

                with z.open('manifest.json') as manifest:
                    data = manifest.read()
                    zipInformation['flowName'] = json.loads(data)['details']['displayName']
                    zipInformation['flowManifest'] = json.loads(data)

                with z.open('Microsoft.Flow/flows/manifest.json') as manifestFlowId:
                    data = manifestFlowId.read()
                    zipInformation['flowId'] = json.loads(data)['flowAssets']['assetPaths'][0]

                with z.open('Microsoft.Flow/flows/' + zipInformation['flowId'] + '/definition.json') as definitionFlow:
                    data = definitionFlow.read()
                    zipInformation['flowDefinition'] = json.loads(data)
                    zipInformation['parameters']['site'] = json.loads(data)['properties']['definition']['actions']['Parâmetros']['inputs']['Site']

            else:
                zipInformation['error'] = True
                zipInformation['messageError'] = 'Unidentified Flow exported file.'

    except zipfile.BadZipFile:
        zipInformation['error'] = True
        zipInformation['messageError'] = 'BadZipFile'

    return zipInformation

eel.start('index.html')