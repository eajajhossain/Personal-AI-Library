
async function sendMessage() {
    const inputField = document.getElementById('user-input');
    const chatWindow = document.getElementById('chat-window');
    const message = inputField.value.trim();

    if (!message) return;

    // Add User Message to UI
    appendMessage('user', message);
    inputField.value = '';

    // Prepare Bot Bubble with a loading state
    const botBubble = appendMessage('bot', 'Thinking...');

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();
        
        // Display the answer from your core.py ai_handler
        botBubble.innerText = data.reply || "No response from AI.";
        chatWindow.scrollTop = chatWindow.scrollHeight;

    } catch (error) {
        botBubble.innerText = "Error: Model unreachable. Ensure Ollama is running.";
        console.error("Chat Error:", error);
    }
}


async function uploadBook() {
    const fileInput = document.getElementById('pdf-upload');
    const file = fileInput.files[0];
    
    if (!file) {
        alert("Please select a PDF file first.");
        return;
    }

    // Visual feedback that upload started
    const uploadBtn = document.querySelector('.btn-upload');
    const originalText = uploadBtn.innerText;
    uploadBtn.innerText = "Indexing... Please wait";
    uploadBtn.disabled = true;

    const formData = new FormData();
    // Key 'file' must match: file = request.files.get('file') in app.py
    formData.append('file', file);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.status === "success") {
            alert(result.message);
            addBookToList(file.name); // Optional: update UI list
        } else {
            alert("Upload Error: " + result.message);
        }
    } catch (error) {
        console.error("Upload Error:", error);
        alert("Server connection failed during upload.");
    } finally {
        uploadBtn.innerText = originalText;
        uploadBtn.disabled = false;
        fileInput.value = ""; // Reset input
    }
}


function appendMessage(role, text) {
    const chatWindow = document.getElementById('chat-window');
    const div = document.createElement('div');
    div.className = `message ${role}`;
    div.innerText = text;
    chatWindow.appendChild(div);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    return div;
}

function addBookToList(filename) {
    const bookList = document.getElementById('book-list');
    const item = document.createElement('div');
    item.className = 'book-item';
    item.innerHTML = `<i class="fas fa-book"></i> ${filename}`;
    bookList.appendChild(item);
}

function handleKey(e) { 
    if (e.key === 'Enter') sendMessage(); 
}

// Ensure the file input triggers uploadBook when a file is chosen
document.getElementById('pdf-upload').addEventListener('change', uploadBook);