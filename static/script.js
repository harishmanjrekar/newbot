const chatWindow = document.getElementById('chat-window');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

sendBtn.addEventListener('click', () => {
    const question = userInput.value;
    if (question.trim() === '') return;

    // Send user question to OpenAI API and handle the response
    // Replace this with actual OpenAI API integration

    const answer = "This is the answer from OpenAI API"; // Replace with actual answer

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
