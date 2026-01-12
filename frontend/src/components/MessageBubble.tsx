import type { Message } from '@/types'

interface MessageBubbleProps {
  message: Message
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.type === 'user'

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} animate-fade-in`}>
      <div className="flex items-start space-x-2 max-w-3xl">
        {!isUser && (
          <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center">
            <span className="text-lg">🤖</span>
          </div>
        )}
        <div className={`message-bubble ${isUser ? 'message-user' : 'message-bot'}`}>
          <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
          <span className={`text-xs mt-1 block ${isUser ? 'text-primary-100' : 'text-gray-500'}`}>
            {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </span>
        </div>
        {isUser && (
          <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary-600 flex items-center justify-center">
            <span className="text-lg">👤</span>
          </div>
        )}
      </div>
    </div>
  )
}
