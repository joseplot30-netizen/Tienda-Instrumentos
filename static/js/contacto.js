document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contact-form');
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const messageInput = document.getElementById('message');
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        let isValid = true;
        let errors = [];
        if (nameInput.value.trim().length < 2) {
            isValid = false;
            errors.push('El nombre debe tener al menos 2 caracteres.');
        }
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(emailInput.value.trim())) {
            isValid = false;
            errors.push('Por favor, ingresa un email válido.');
        }
        if (messageInput.value.trim().length < 10 || messageInput.value.trim().length > 200) {
            isValid = false;
            errors.push('El mensaje debe tener entre 10 y 200 caracteres.');
        }
        if (!isValid) {
            alert('Errores en el formulario:\n' + errors.join('\n'));
            return;
        }
        const formData = new FormData(form);
        fetch('/contacto', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                alert('¡Mensaje enviado exitosamente!');
                form.reset();
            } else {
                response.text().then(text => alert('Error: ' + response.status + ' ' + response.statusText + '\n' + text));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al enviar el mensaje. Inténtalo de nuevo.');
        });
    });
    const inputs = [nameInput, emailInput, messageInput];
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.style.borderColor = '#dc0808';
        });
        input.addEventListener('blur', function() {
            this.style.borderColor = '#ccc';
        });
    });
});