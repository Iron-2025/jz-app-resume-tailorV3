/**
 * Resume Tailor - Main JavaScript
 * Handles client-side functionality for the Resume Tailor application
 */

document.addEventListener('DOMContentLoaded', function() {
    // File upload preview functionality
    setupFilePreview('resume_file', 'resume_preview');
    setupFilePreview('job_description_file', 'job_description_preview');
    
    // PDF export functionality (for future implementation)
    const pdfExportButton = document.getElementById('export-pdf');
    if (pdfExportButton) {
        pdfExportButton.addEventListener('click', function() {
            alert('PDF export functionality coming soon!');
        });
    }
    
    // Markdown preview toggle
    const togglePreviewButton = document.getElementById('toggle-preview');
    if (togglePreviewButton) {
        togglePreviewButton.addEventListener('click', function() {
            const markdownContent = document.querySelector('.markdown-content');
            const markdownSource = document.getElementById('markdown-source');
            
            if (markdownContent.style.display === 'none') {
                markdownContent.style.display = 'block';
                markdownSource.parentElement.style.display = 'none';
                togglePreviewButton.textContent = 'Show Markdown';
            } else {
                markdownContent.style.display = 'none';
                markdownSource.parentElement.style.display = 'block';
                togglePreviewButton.textContent = 'Show Preview';
            }
        });
    }
});

/**
 * Sets up file preview functionality for file inputs
 * @param {string} inputId - The ID of the file input element
 * @param {string} previewId - The ID of the preview element
 */
function setupFilePreview(inputId, previewId) {
    const fileInput = document.getElementById(inputId);
    const previewElement = document.getElementById(previewId);
    
    if (!fileInput || !previewElement) return;
    
    fileInput.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            const file = this.files[0];
            
            // Show file name and size
            const fileSize = (file.size / 1024).toFixed(2) + ' KB';
            previewElement.innerHTML = `
                <div class="mt-2 text-sm">
                    <strong>File:</strong> ${file.name}<br>
                    <strong>Size:</strong> ${fileSize}
                </div>
            `;
            
            // If it's a text file, show a preview
            if (file.type === 'text/plain') {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const content = e.target.result;
                    const previewContent = content.substring(0, 200) + (content.length > 200 ? '...' : '');
                    
                    previewElement.innerHTML += `
                        <div class="mt-2 p-2 bg-gray-100 rounded text-sm font-mono overflow-hidden">
                            <strong>Preview:</strong><br>
                            ${previewContent.replace(/\n/g, '<br>')}
                        </div>
                    `;
                };
                reader.readAsText(file);
            }
        } else {
            previewElement.innerHTML = '';
        }
    });
}

/**
 * Handles the copy to clipboard functionality
 * @param {string} text - The text to copy to clipboard
 * @param {HTMLElement} button - The button element that was clicked
 */
function copyToClipboard(text, button) {
    navigator.clipboard.writeText(text).then(function() {
        const originalText = button.textContent;
        button.textContent = 'Copied!';
        setTimeout(function() {
            button.textContent = originalText;
        }, 2000);
    }).catch(function(err) {
        console.error('Could not copy text: ', err);
        alert('Failed to copy to clipboard');
    });
}
