document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(event) {
            const action = event.submitter.value;
            const justification = document.querySelector('#justification').value.trim();

            if (action === 'disapprove' && !justification) {
                event.preventDefault();
                alert('Justification is required when disapproving a comment.');
            }
        });
    }
});