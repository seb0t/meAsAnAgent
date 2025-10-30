import { useState } from 'react'

const ChatUI: React.FC = () => {
  const [messages, setMessages] = useState<string[]>([])
  const [input, setInput] = useState('')

  const sendMessage = () => {
    // TODO: send to backend
    setMessages([...messages, input])
    setInput('')
  }

  return (
    <div style={{ padding: '20px' }}>
      <h1>AI Career Agent Chat</h1>
      <div>
        {messages.map((msg, idx) => <p key={idx}>{msg}</p>)}
      </div>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  )
}

export default ChatUI