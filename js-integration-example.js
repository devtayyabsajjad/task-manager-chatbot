/**
 * JavaScript Integration Example for Railway-deployed Groq FastAPI Chatbot
 *
 * Replace 'https://your-project.up.railway.app' with your actual Railway URL
 * after deployment.
 */

const API_BASE_URL = 'https://your-project.up.railway.app';

/**
 * Simple chatbot client class
 */
class ChatbotClient {
    constructor(baseUrl = API_BASE_URL) {
        this.baseUrl = baseUrl;
    }

    /**
     * Send a message to the chatbot
     * @param {string} message - User message
     * @param {Object} options - Optional parameters
     * @returns {Promise<Object>} Chat response
     */
    async sendMessage(message, options = {}) {
        const payload = {
            message: message,
            model: options.model || 'llama-3.1-8b-instant',
            max_tokens: options.maxTokens || 1024,
            temperature: options.temperature || 0.7
        };

        const response = await fetch(`${this.baseUrl}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const error = await response.text();
            throw new Error(`HTTP ${response.status}: ${error}`);
        }

        return await response.json();
    }

    /**
     * Get available models
     * @returns {Promise<Object>} Models list
     */
    async getModels() {
        const response = await fetch(`${this.baseUrl}/models`);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        return await response.json();
    }

    /**
     * Health check
     * @returns {Promise<Object>} Health status
     */
    async healthCheck() {
        const response = await fetch(`${this.baseUrl}/health`);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        return await response.json();
    }
}

// Create global client instance
const chatbot = new ChatbotClient();

// Example usage functions
window.ChatbotExamples = {
    /**
     * Basic chat example
     */
    async basicChat() {
        try {
            console.log('Sending message...');
            const response = await chatbot.sendMessage('Hello! Tell me a joke.');
            console.log('Response:', response);
            return response;
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    },

    /**
     * Advanced chat with custom parameters
     */
    async advancedChat() {
        try {
            console.log('Sending advanced message...');
            const response = await chatbot.sendMessage(
                'Explain machine learning in simple terms',
                {
                    model: 'mixtral-8x7b-32768',
                    maxTokens: 500,
                    temperature: 0.8
                }
            );
            console.log('Response:', response);
            return response;
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    },

    /**
     * Get available models
     */
    async getAvailableModels() {
        try {
            console.log('Fetching models...');
            const models = await chatbot.getModels();
            console.log('Available models:', models);
            return models;
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    },

    /**
     * Health check
     */
    async checkHealth() {
        try {
            console.log('Checking health...');
            const health = await chatbot.healthCheck();
            console.log('Health status:', health);
            return health;
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    },

    /**
     * Interactive chat in console
     */
    async startInteractiveChat() {
        console.log('🤖 Interactive Chat Started!');
        console.log('Type your messages and press Enter. Type "quit" to exit.');

        while (true) {
            const message = prompt('You: ');

            if (!message || message.toLowerCase() === 'quit') {
                console.log('👋 Chat ended!');
                break;
            }

            try {
                console.log('Bot is thinking...');
                const response = await chatbot.sendMessage(message);
                console.log('Bot:', response.reply);
                console.log(`(Model: ${response.model_used}, Tokens: ${response.tokens_used})`);
            } catch (error) {
                console.error('Error:', error.message);
            }
        }
    }
};

// HTML UI Example (can be added to your HTML file)
const createChatUI = () => {
    const ui = document.createElement('div');
    ui.innerHTML = `
        <div id="chat-container" style="
            max-width: 600px;
            margin: 20px auto;
            font-family: Arial, sans-serif;
            border: 1px solid #ccc;
            border-radius: 8px;
            overflow: hidden;
        ">
            <div id="chat-messages" style="
                height: 300px;
                overflow-y: auto;
                padding: 10px;
                background: #f9f9f9;
            "></div>
            <div id="chat-input-area" style="
                display: flex;
                padding: 10px;
                border-top: 1px solid #ccc;
                background: white;
            ">
                <input
                    id="chat-input"
                    type="text"
                    placeholder="Type your message..."
                    style="
                        flex: 1;
                        padding: 8px;
                        border: 1px solid #ccc;
                        border-radius: 4px;
                        margin-right: 10px;
                    "
                />
                <button
                    id="send-button"
                    style="
                        padding: 8px 16px;
                        background: #007bff;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        cursor: pointer;
                    "
                >Send</button>
            </div>
        </div>
        <div style="text-align: center; margin: 10px;">
            <button id="clear-chat" style="
                padding: 5px 10px;
                background: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            ">Clear Chat</button>
        </div>
    `;

    // Add event listeners
    const input = ui.querySelector('#chat-input');
    const sendButton = ui.querySelector('#send-button');
    const messages = ui.querySelector('#chat-messages');
    const clearButton = ui.querySelector('#clear-chat');

    const addMessage = (text, isUser = false) => {
        const messageDiv = document.createElement('div');
        messageDiv.style.cssText = `
            margin: 5px 0;
            padding: 8px;
            border-radius: 8px;
            max-width: 70%;
            ${isUser
                ? 'margin-left: auto; background: #007bff; color: white; text-align: right;'
                : 'margin-right: auto; background: white; border: 1px solid #ccc;'
            }
        `;
        messageDiv.textContent = text;
        messages.appendChild(messageDiv);
        messages.scrollTop = messages.scrollHeight;
    };

    const sendMessage = async () => {
        const text = input.value.trim();
        if (!text) return;

        addMessage(text, true);
        input.value = '';

        try {
            addMessage('Bot is thinking...', false);
            const response = await chatbot.sendMessage(text);
            // Remove "thinking" message
            messages.removeChild(messages.lastElementChild);
            addMessage(response.reply, false);
        } catch (error) {
            messages.removeChild(messages.lastElementChild);
            addMessage(`Error: ${error.message}`, false);
        }
    };

    sendButton.addEventListener('click', sendMessage);
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    clearButton.addEventListener('click', () => {
        messages.innerHTML = '';
    });

    return ui;
};

// Make functions available globally for easy testing
window.ChatbotClient = ChatbotClient;
window.chatbot = chatbot;
window.createChatUI = createChatUI;

console.log('🚀 Groq Chatbot JavaScript Integration Loaded!');
console.log('Try: ChatbotExamples.basicChat()');
console.log('Or: ChatbotExamples.startInteractiveChat()');
console.log('Or add UI: document.body.appendChild(createChatUI())');
