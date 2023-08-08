document.addEventListener("DOMContentLoaded", function () {
    const chatContainer = document.getElementById("chat");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");

    sendBtn.addEventListener("click", function () {
        const message = userInput.value.trim();
        if (message !== "") {
            addMessage("user", message);
            userInput.value = "";

            // TODO: Send the user's question to the server and handle response
            // You can use fetch() to send the user's question to the server and update the chat with the response
        }
    });

    function addMessage(sender, text) {
        const messageDiv = document.createElement("div");
        messageDiv.className = "message " + sender;
        messageDiv.textContent = text;

        chatContainer.appendChild(messageDiv);

        // Scroll to the bottom of the chat
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
});
