document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('parameterForm');
    const inputs = form.querySelectorAll('input');
    const formResult = document.getElementById('formResult');

    const validateInput = (input) => {
        const value = parseFloat(input.value);
        const min = parseFloat(input.min);
        const max = parseFloat(input.max);
        const formGroup = input.closest('.form-group');
        
        if (input.value === '' || isNaN(value) || value < min || value > max) {
            formGroup.classList.remove('valid');
            formGroup.classList.add('invalid');
            return false;
        } else {
            formGroup.classList.remove('invalid');
            formGroup.classList.add('valid');
            return true;
        }
    };

    const checkFormValidity = () => {
        let isValid = true;
        inputs.forEach(input => {
            if (!validateInput(input)) {
                isValid = false;
            }
        });
        return isValid;
    };

    inputs.forEach(input => {
        ['input', 'blur'].forEach(eventType => {
            input.addEventListener(eventType, () => {
                validateInput(input);
            });
        });
    });

    form.addEventListener('submit', async (e) => {
        if (!checkFormValidity()) {
            e.preventDefault();
            return;
        }
    });
});