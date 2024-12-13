document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('uploadForm');
    const csvFile = document.getElementById('csvFile');
    const uploadMessage = document.getElementById('uploadMessage');
    const ideateBtn = document.getElementById('ideateBtn');
    const refreshEntriesBtn = document.getElementById('refreshEntriesBtn');
    const logsSection = document.getElementById('logsSection');
    const logsContainer = document.getElementById('logsContainer');
    const entriesTable = document.getElementById('entriesTable').querySelector('tbody');

    // Upload CSV
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        uploadMessage.textContent = "";
        const file = csvFile.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        if (response.ok) {
            uploadMessage.textContent = result.message;
            refreshEntries();
        } else {
            uploadMessage.textContent = result.error;
            uploadMessage.classList.add('text-danger');
        }
    });

    // Ideation
    ideateBtn.addEventListener('click', async () => {
        const response = await fetch('/ideate', {
            method: 'POST'
        });
        const result = await response.json();
        logsContainer.innerHTML = "";
        if (result.logs && result.logs.length > 0) {
            logsSection.style.display = 'block';
            result.logs.forEach(log => {
                const p = document.createElement('p');
                p.textContent = log;
                logsContainer.appendChild(p);
            });
        }
    });

    // Refresh Entries
    refreshEntriesBtn.addEventListener('click', () => {
        refreshEntries();
    });

    async function refreshEntries() {
        const response = await fetch('/entries');
        const data = await response.json();
        entriesTable.innerHTML = "";
        data.forEach(entry => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${entry.name || ''}</td>
                <td>${entry.description || ''}</td>
                <td>${entry.category || ''}</td>
                <td>${entry.base_url || ''}</td>
                <td>${entry.endpoint || ''}</td>
            `;
            entriesTable.appendChild(tr);
        });
    }

    // Load entries on page load
    refreshEntries();
});
