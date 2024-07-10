import React, { useState, useEffect } from 'react';
import Assistant from '@/components/Assistant';
import ChatBox from '@/components/ChatBox';
import axios from 'axios';



const Chat: React.FC = () => {

    const [messages, setMessages] = useState<any[]>([]);
    const handleAsk = async (question: string) => {
        try {
            const response = await axios.post('http://localhost:5000/ask', { question });
            setMessages([...messages, { sender: 'user', content: question }]);
            setMessages([...messages, { sender: 'assistant', content: response.data.response }]);
        } catch (error) {
            console.error(error);
            setMessages([...messages, { sender: 'assistant', content: 'Something went wrong. Try again later.' }]);
        }
    };

    return (
        <div className="chat-container">
            <ChatBox messages={messages} />
            <Assistant onAsk={handleAsk} />
        </div>
    );
};

export default Chat