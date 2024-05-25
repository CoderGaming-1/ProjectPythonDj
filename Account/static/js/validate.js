function validateNonNullFields() {
    var fields = ['name', 'birth', 'gender', 'graduation', 'nation'];
    var valid = true;

    fields.forEach(function(field) {
        var input = document.getElementById(field);
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            valid = false;
        } else {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
        }
    });

    return valid;
}

function validateEmail() {
    var emailInput = document.getElementById('email');
    var emailValue = emailInput.value;
    
    var emailPattern = /^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$/i;

    if (emailPattern.test(emailValue)) {
        emailInput.classList.remove('is-invalid');
        emailInput.classList.add('is-valid');
        return true;
    } else {
        emailInput.classList.remove('is-valid');
        emailInput.classList.add('is-invalid');
        return false;
    }
}

function validatePhoneNumber() {
    var phoneInput = document.getElementById('phonenumber');
    var phoneValue = phoneInput.value;
    
    var phonePattern = /^0[0-9]+$/;

    if (phonePattern.test(phoneValue)) {
        phoneInput.classList.remove('is-invalid');
        phoneInput.classList.add('is-valid');
        return true;
    } else {
        phoneInput.classList.remove('is-valid');
        phoneInput.classList.add('is-invalid');
        return false;
    }
}

function submitAndRedirect() {
    var nonNullFieldsValid = validateNonNullFields();
    var emailValid = validateEmail();
    var phoneValid = validatePhoneNumber();
    
    if (nonNullFieldsValid && emailValid && phoneValid) {
        document.getElementById('myForm').submit();

        setTimeout(function() {
            var saveButton = document.querySelector('.btn-success');
            var url = saveButton.getAttribute('data-url');
            window.location.href = url;
        }, 500);
    }
}

document.getElementById('myForm').addEventListener('submit', function(event) {
    var nonNullFieldsValid = validateNonNullFields();
    var emailValid = validateEmail();
    var phoneValid = validatePhoneNumber();
    
    if (!nonNullFieldsValid || !emailValid || !phoneValid) {
        event.preventDefault();
    }
});
