// document.getElementById("button-name").addEventListener("click", () => { eel.get_random_name() }, false);
// document.getElementById("button-number").addEventListener("click", () => { eel.get_random_number() }, false);
// document.getElementById("button-date").addEventListener("click", () => { eel.get_date() }, false);
// document.getElementById("button-ip").addEventListener("click", () => { eel.get_ip() }, false);

// Declarando variáveis
let txtDefinition = document.getElementById("txtDefinition");
let spanDefinitionStatus = document.getElementById("spanDefinitionStatus");

// Adicionando eventos
txtDefinition.addEventListener("input", () => { checkTxtDescription() }, false);

eel.expose(prompt_alerts);

// Funcionalidades
function prompt_alerts(description) {
    alert(description);
}

function checkTxtDescription() {

    if (isJsonValid(txtDefinition.value)) {
        txtDefinition.classList.remove('ms-borderColor-redDark');

        spanDefinitionStatus.innerHTML = "";
        spanDefinitionStatus.classList.remove('ms-fontColor-red');

    } else {
        txtDefinition.classList.add('ms-borderColor-redDark');

        spanDefinitionStatus.innerHTML = "❌ JSON inválido";
        spanDefinitionStatus.classList.add('ms-fontColor-red');
    }
}

function isJsonValid(str) {
    try {
        JSON.parse(str)
    } catch (e) {
        return false;
    }
    return true;
}

function saveFlow() {

    let zipSave = {
        'filePath': document.getElementById('spanFileLocation').innerHTML,
        'flowName': {
            'new': document.getElementById('txtFlowName').value,
            'old': document.getElementById('spanOriginalFlowName').innerHTML
        },
        'flowSite': {
            'new': document.getElementById('txtFlowActionsSite').value,
            'old': JSON.parse(document.getElementById('txtDefinition').value)['properties']['definition']['actions']['Parâmetros']['inputs']['Site']
        },
        'flowDefinition': JSON.parse(document.getElementById('txtDefinition').value),
        'flowManifest': JSON.parse(document.getElementById('txtManifest').value)
    }

    console.log(zipSave);

    eel.saveFlow(zipSave);

}


async function getExportedFlow() {
    var zipFile = await eel.btn_ResimyoluClick()();
    if (zipFile) {

        document.getElementById('spanFileLocation').innerHTML = zipFile.fullPath;

        if (!(zipFile.error)) {
            document.getElementById('divFlowEditor').classList.remove('d-none');
            document.getElementById('divFlowActions').classList.remove('d-none');
            document.getElementById('divWrongZip').classList.add('d-none');
            document.getElementById('spanResumeError').innerHTML = '';

            document.getElementById('spanOriginalFlowName').innerHTML = zipFile.flowName;
            document.getElementById('txtFlowName').value = zipFile.flowName;
            document.getElementById('txtDefinition').value = JSON.stringify(zipFile.flowDefinition);
            document.getElementById('txtManifest').value = JSON.stringify(zipFile.flowManifest);

            document.getElementById('txtFlowActionsSite').value = zipFile.parameters.site;

        } else {
            document.getElementById('divFlowEditor').classList.add('d-none');
            document.getElementById('divFlowActions').classList.add('d-none');
            document.getElementById('divWrongZip').classList.remove('d-none');

            zipFile.messageError ? document.getElementById('spanResumeError').innerHTML = zipFile.messageError : document.getElementById('spanResumeError').innerHTML = '';

        }
    }
}