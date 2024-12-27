document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            const closeButton = alert.querySelector('.btn-close');
            if (closeButton) {
                closeButton.click();
            }
        }, 5000);
    });

    // Dynamic option fields in poll creation
    const addOptionBtn = document.getElementById('add-option');
    if (addOptionBtn) {
        addOptionBtn.addEventListener('click', function() {
            const optionForms = document.querySelectorAll('.option-form');
            const lastForm = optionForms[optionForms.length - 1];
            const newForm = lastForm.cloneNode(true);
            
            // Clear the input value
            const input = newForm.querySelector('input[type="text"]');
            input.value = '';
            
            lastForm.parentNode.insertBefore(newForm, addOptionBtn);
        });
    }
}); 