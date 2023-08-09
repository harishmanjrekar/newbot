const chatWindow = document.getElementById('chat-window');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

sendBtn.addEventListener('click', async () => {
    const question = userInput.value;
    if (question.trim() === '') return;

    const response = await fetch('/get_answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_input: question })
    });

    const data = await response.json();
    const answer = data.answer;

    saveAnswerToAzure(question, answer);

    displayMessage(question, 'user');
    displayMessage(answer, 'bot');

    userInput.value = '';
});

function displayMessage(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    messageDiv.textContent = message;
    chatWindow.appendChild(messageDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function saveAnswerToAzure(question, answer) {
    // Implement Azure storage logic here
    // Replace with actual Azure storage integration
}
