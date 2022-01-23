from tkinter import filedialog as fd
from datetime import datetime
import tkinter as tk
import subprocess
import tempfile
import zipfile
import random
import json
import eel
import os

eel.browsers.set_path('chrome', 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')

eel.init('web')

definitionJsonPath = ''


@eel.expose
def saveFlow(newFlow):
    
    # Making Manifest.json & Definition in string
    manifest = json.dumps(newFlow['flowManifest'], ensure_ascii=False)
    definition = json.dumps(newFlow['flowDefinition'], ensure_ascii=False)

    # Replace
    manifest = manifest.replace(newFlow['flowName']['old'], newFlow['flowName']['new'])
    definition = definition.replace(newFlow['flowName']['old'], newFlow['flowName']['new'])
    definition = definition.replace(newFlow['flowSite']['old'], newFlow['flowSite']['new'])

    # Return to Dict
    manifest = json.loads(manifest)
    definition = json.loads(definition)

    # Update ZIP File
    updateZip(newFlow['filePath'], 'manifest.json', manifest)
    updateZip(newFlow['filePath'], definitionJsonPath, definition)
    
    # Abrir pasta do arquivo com o próprio selecionado
    subprocess.Popen(r'explorer /select,"' + newFlow['filePath'].replace('/', '\\') + '"')

def updateZip(zipname, filename, data):
    # generate a temp file
    tmpfd, tmpname = tempfile.mkstemp(dir=os.path.dirname(zipname))
    os.close(tmpfd)

    # create a temp copy of the archive without filename            
    with zipfile.ZipFile(zipname, 'r') as zin:
        with zipfile.ZipFile(tmpname, 'w') as zout:
            zout.comment = zin.comment # preserve the comment
            for item in zin.infolist():
                if item.filename != filename:
                    zout.writestr(item, zin.read(item.filename))

    # replace with the temp archive
    os.remove(zipname)
    os.rename(tmpname, zipname)

    # now add filename with its new data
    with zipfile.ZipFile(zipname, mode='a', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(filename, json.dumps(data).encode('utf-8'))
        # zf.writestr(filename, data)


@eel.expose
def btn_ResimyoluClick():
    global definitionJsonPath

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
        },
        'definitionJsonPath': ''
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
                    definitionJsonPath = 'Microsoft.Flow/flows/' + zipInformation['flowId'] + '/definition.json'

            else:
                zipInformation['error'] = True
                zipInformation['messageError'] = 'Unidentified Flow exported file.'

    except zipfile.BadZipFile:
        zipInformation['error'] = True
        zipInformation['messageError'] = 'BadZipFile'

    return zipInformation

eel.start('index.html')