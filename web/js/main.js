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
    console.log('entrei')

    if (isJsonValid(txtDefinition.value)) {
        txtDefinition.classList.remove('ms-borderColor-redDark');

        spanDefinitionStatus.innerHTML = "";
        spanDefinitionStatus.classList.remove('ms-fontColor-red');
        console.log('JSON válido');

    } else {
        txtDefinition.classList.add('ms-borderColor-redDark');

        spanDefinitionStatus.innerHTML = "❌ JSON inválido";
        spanDefinitionStatus.classList.add('ms-fontColor-red');
        console.log('❌ JSON inválido');
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