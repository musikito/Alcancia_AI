import React from 'react';
import Message from './Assistant'; // Assuming Message interface is defined in Assistant.tsx

interface ChatBoxProps {
  messages: Array<typeof Message>;
}

const ChatBox: React.FC<ChatBoxProps> = ({ messages }) => {
  return (
    <div id="chat-box" className="chat-box">
      {messages.map((message, index) => (
        <div key={index} className={`message ${message.role}`}>
          {message.content}
        </div>
      ))}
    </div>
  );
};

export default ChatBox;
