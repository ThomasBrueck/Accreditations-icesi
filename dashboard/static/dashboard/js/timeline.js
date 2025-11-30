document.addEventListener('DOMContentLoaded', function() {
    console.log('Timeline.js loaded successfully');

    function updateTimeline(status, progressPercentage) {
        console.log('Updating timeline with status:', status);
        console.log('Progress percentage:', progressPercentage + '%');
        
        const timelineDots = document.querySelectorAll('.timeline-dot');
        console.log('Found timeline dots:', timelineDots.length);

        // Update progress line
        const progressLine = document.querySelector('.timeline-progress');
        if (progressLine) {
            console.log('Setting progress line width to:', progressPercentage + '%');
            progressLine.style.width = progressPercentage + '%';
        }

        // Update dots and status labels
        timelineDots.forEach((dot, index) => {
            const dotElement = document.getElementById(`dot${index + 1}`);
            const statusElement = dotElement.parentElement.querySelector('.status');
            
            console.log(`Updating dot ${index + 1}`);
            
            if (status === 'planning' && index <= 0) {
                console.log(`Dot ${index + 1}: In Progress`);
                updateDotStatus(dotElement, statusElement, 'in-progress');
            } else if (status === 'analysis' && index <= 1) {
                console.log(`Dot ${index + 1}: Completed/In Progress`);
                updateDotStatus(dotElement, statusElement, index < 1 ? 'completed' : 'in-progress');
            } else if (status === 'evidence' && index <= 2) {
                console.log(`Dot ${index + 1}: Completed/In Progress`);
                updateDotStatus(dotElement, statusElement, index < 2 ? 'completed' : 'in-progress');
            } else if (status === 'report' && index <= 3) {
                console.log(`Dot ${index + 1}: Completed/In Progress`);
                updateDotStatus(dotElement, statusElement, index < 3 ? 'completed' : 'in-progress');
            } else if (status === 'consolidation' && index <= 4) {
                console.log(`Dot ${index + 1}: Completed/In Progress`);
                updateDotStatus(dotElement, statusElement, index < 4 ? 'completed' : 'in-progress');
            } else if (status === 'submission' && index <= 5) {
                console.log(`Dot ${index + 1}: Completed/In Progress`);
                updateDotStatus(dotElement, statusElement, index < 5 ? 'completed' : 'in-progress');
            } else if (status === 'completed') {
                console.log(`Dot ${index + 1}: Completed`);
                updateDotStatus(dotElement, statusElement, 'completed');
            } else {
                console.log(`Dot ${index + 1}: Pending`);
                updateDotStatus(dotElement, statusElement, 'pending');
            }
        });
    }

    function updateDotStatus(dot, statusElement, status) {
        dot.classList.remove('completed', 'in-progress', 'pending');
        dot.classList.add(status);
        statusElement.textContent = status.charAt(0).toUpperCase() + status.slice(1);
        statusElement.className = 'status ' + status;
    }

    // Initial timeline update
    fetch(accreditationStatusUrl, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrfToken
        },
        credentials: 'same-origin'
    })
    .then(response => {
        console.log('Response status:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('Received data:', data);
        updateTimeline(data.status, data.progress_percentage);
    })
    .catch(error => {
        console.error('Error fetching timeline status:', error);
    });
});