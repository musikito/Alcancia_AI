import React, { useState, useEffect } from 'react';
import ChatBox from './ChatBox';

interface AssistantProps {
  onAsk: (question: string) => void;
  messages: Message[];
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>;
}

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

const Assistant: React.FC<AssistantProps> = ({ onAsk, messages, setMessages }) => {
  const [userInput, setUserInput] = useState('');

  const handleAsk = () => {
    if (userInput) {
      onAsk(userInput);
      setUserInput('');
    }
  };

  useEffect(() => {
    // Scroll to the bottom of the chat box on message updates
    const chatBox = document.getElementById('chat-box');
    if (chatBox) {
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="assistant-container">
      <ChatBox messages={messages} />
      <input
        type="text"
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
        placeholder="Ask your question..."
      />
      <button onClick={handleAsk}>Ask Assistant</button>
    </div>
  );
};

export default Assistant;
