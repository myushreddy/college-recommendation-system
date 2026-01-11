'use client'

import { useState, useRef, useEffect } from 'react'
import { nlpService, collegeService } from '@/services/api'
import type { Message, College } from '@/types'
import MessageBubble from './MessageBubble'
import QuickActions from './QuickActions'
import CollegeCard from './CollegeCard'

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'bot',
      content: 'Hi! 👋 I\'m your college recommendation assistant. I can help you find engineering colleges based on your preferences. Try asking me something like "Find CS colleges in Karnataka under 2 lakhs"',
      timestamp: new Date(),
    },
  ])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleQuickAction = (query: string) => {
    setInputValue(query)
    handleSendMessage(query)
  }

  const handleSendMessage = async (messageText?: string) => {
    const text = messageText || inputValue.trim()
    if (!text || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: text,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInputValue('')
    setIsLoading(true)

    try {
      // Process query with NLP
      const nlpResponse = await nlpService.processQuery(text)

      // Add bot's friendly response
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        content: nlpResponse.friendly_message,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, botMessage])

      // Fetch colleges based on intent
      if (nlpResponse.intent === 'search' || nlpResponse.intent === 'recommend') {
        const searchResponse = await collegeService.search(nlpResponse.api_params)

        if (searchResponse.results.length > 0) {
          const resultsMessage: Message = {
            id: (Date.now() + 2).toString(),
            type: 'bot',
            content: `I found ${searchResponse.total} colleges matching your criteria. Here are the top results:`,
            timestamp: new Date(),
            colleges: searchResponse.results.slice(0, 6),
          }
          setMessages((prev) => [...prev, resultsMessage])
        } else {
          const noResultsMessage: Message = {
            id: (Date.now() + 2).toString(),
            type: 'bot',
            content: 'No colleges found matching your criteria. Try adjusting your filters.',
            timestamp: new Date(),
          }
          setMessages((prev) => [...prev, noResultsMessage])
        }
      } else if (nlpResponse.intent === 'greeting') {
        // Greeting already handled by friendly_message
      } else if (nlpResponse.intent === 'info' && nlpResponse.entities.colleges.length > 0) {
        const infoMessage: Message = {
          id: (Date.now() + 2).toString(),
          type: 'bot',
          content: 'Let me search for that college information...',
          timestamp: new Date(),
        }
        setMessages((prev) => [...prev, infoMessage])
      }
    } catch (error: any) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        content: `Sorry, I encountered an error: ${error.message || 'Please try again.'}`,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="flex flex-col h-screen max-w-6xl mx-auto">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200 py-4 px-6">
        <h1 className="text-2xl font-bold text-primary-700">🎓 College Recommendation Assistant</h1>
        <p className="text-sm text-gray-600 mt-1">Find your perfect engineering college</p>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((message) => (
          <div key={message.id}>
            <MessageBubble message={message} />
            {message.colleges && message.colleges.length > 0 && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4 ml-12">
                {message.colleges.map((college) => (
                  <CollegeCard key={college.college_id} college={college} />
                ))}
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="message-bubble message-bot">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Actions */}
      <QuickActions onActionClick={handleQuickAction} />

      {/* Input Area */}
      <div className="bg-white border-t border-gray-200 p-4">
        <div className="max-w-4xl mx-auto flex gap-2">
          <input
            ref={inputRef}
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me about colleges... (e.g., 'Find CS colleges in Karnataka')"
            className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            disabled={isLoading}
          />
          <button
            onClick={() => handleSendMessage()}
            disabled={isLoading || !inputValue.trim()}
            className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors duration-200 font-medium"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  )
}
