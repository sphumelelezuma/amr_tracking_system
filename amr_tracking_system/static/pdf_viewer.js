document.addEventListener('DOMContentLoaded', function () {
    
    // Set the workerSrc for PDF.js
    pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.10.377/pdf.worker.min.js';

    // Iterate over all posts and render PDFs for those that have them
    document.querySelectorAll('[id^=pdf-url]').forEach(function (pdfInput) {
        const postId = pdfInput.id.split('-')[2]; // Extract the post ID
        const url = document.getElementById(`pdf-url-${postId}`).value; // Get the PDF URL
        
        if (url) {
            pdfjsLib.getDocument(url).promise.then(pdf => {
                pdf.getPage(1).then(page => {
                    const scale = 1.5;
                    const viewport = page.getViewport({ scale });
                    const canvas = document.createElement('canvas');
                    const context = canvas.getContext('2d');
                    canvas.height = viewport.height;
                    canvas.width = viewport.width;
                    document.getElementById(`pdf-viewer-${postId}`).appendChild(canvas); // Append canvas to dynamic viewer
                    const renderContext = {
                        canvasContext: context,
                        viewport: viewport,
                    };
                    page.render(renderContext);
                });
            }).catch(error => {
                console.error(`Error loading PDF for post ${postId}:`, error);
            });
        } else {
            console.error(`No URL found for post ${postId}`);
        }
    });
});

