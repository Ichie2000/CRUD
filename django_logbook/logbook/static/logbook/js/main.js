// Main JavaScript file for Logbook application

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Handle form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.add('fade');
            setTimeout(() => alert.remove(), 150);
        }, 5000);
    });

    // Dynamic search functionality
    const searchInput = document.querySelector('#search-input');
    if (searchInput) {
        let timeout = null;
        searchInput.addEventListener('input', (e) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                const query = e.target.value;
                if (query.length >= 2) {
                    fetch(`/search/?q=${encodeURIComponent(query)}&format=json`)
                        .then(response => response.json())
                        .then(data => {
                            updateSearchResults(data);
                        })
                        .catch(error => console.error('Error:', error));
                }
            }, 300);
        });
    }

    // Function to update search results
    function updateSearchResults(data) {
        const resultsContainer = document.querySelector('#search-results');
        if (!resultsContainer) return;

        resultsContainer.innerHTML = '';
        if (data.results && data.results.length > 0) {
            data.results.forEach(result => {
                const item = document.createElement('div');
                item.className = 'list-group-item search-result';
                item.innerHTML = `
                    <div class="d-flex w-100 justify-content-between">
                        <h5 class="mb-1">${escapeHtml(result.title)}</h5>
                        <small>${result.created_at}</small>
                    </div>
                    <p class="mb-1">${escapeHtml(result.description)}</p>
                `;
                resultsContainer.appendChild(item);
            });
        } else {
            resultsContainer.innerHTML = '<p class="text-muted">No results found</p>';
        }
    }

    // Utility function to escape HTML
    function escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    // Handle file inputs
    const fileInputs = document.querySelectorAll('.custom-file-input');
    fileInputs.forEach(input => {
        input.addEventListener('change', (e) => {
            const fileName = e.target.files[0]?.name || 'Choose file';
            const label = e.target.nextElementSibling;
            if (label) {
                label.textContent = fileName;
            }
        });
    });

    // Handle dynamic form fields
    const addFieldButton = document.querySelector('#add-field');
    if (addFieldButton) {
        addFieldButton.addEventListener('click', () => {
            const container = document.querySelector('#dynamic-fields');
            const fieldCount = container.children.length;
            const newField = document.createElement('div');
            newField.className = 'form-group row mb-3';
            newField.innerHTML = `
                <div class="col-md-5">
                    <input type="text" class="form-control" name="field_name_${fieldCount}" placeholder="Field Name">
                </div>
                <div class="col-md-5">
                    <input type="text" class="form-control" name="field_value_${fieldCount}" placeholder="Field Value">
                </div>
                <div class="col-md-2">
                    <button type="button" class="btn btn-danger remove-field">Remove</button>
                </div>
            `;
            container.appendChild(newField);
        });

        // Handle remove field button
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('remove-field')) {
                e.target.closest('.form-group').remove();
            }
        });
    }
}); 