// question_form.js
document.addEventListener("DOMContentLoaded", function() {
    const txtInput = document.getElementById('id_txt_file');
    const descriptionField = document.getElementById('id_description');

    if (txtInput && descriptionField) {
        txtInput.addEventListener('change', function() {
            const file = txtInput.files[0];
            if (file && file.name.toLowerCase().endsWith('.txt')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    descriptionField.value = e.target.result;
                };
                reader.onerror = function() {
                    alert('Error al leer el archivo. Por favor, asegúrate de que sea un archivo de texto válido.');
                };
                reader.readAsText(file);
            } else {
                alert('Por favor, selecciona un archivo .txt válido.');
            }
        });
    }
});