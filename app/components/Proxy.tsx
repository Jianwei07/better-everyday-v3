import React, { useState, useEffect, useRef } from "react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Smile, Paperclip, Send, ChevronDown, ArrowLeft } from "lucide-react";

type ChatMessage = {
  sender: string;
  text: string;
  timestamp?: string;
};

const topics = [
  "Get Quick Tips",
  "Eye Health",
  "Neuro",
  "Cancer Prevention",
  "Strength and Weights Training",
  "Fat Loss",
  "Random Advice",
];

const QuickResponseButton = ({
  text,
  onSend,
}: {
  text: string;
  onSend: (message: string) => void;
}) => (
  <Button
    variant="outline"
    className="bg-blue-50 text-blue-600 border-blue-100 hover:bg-blue-100 hover:text-blue-700"
    onClick={() => onSend(text)}
  >
    {text}
  </Button>
);

const Chatbot = () => {
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([
    {
      sender: "Eva",
      text: "Hello! I'm Eva, your health and wellness assistant. How can I help you today? You can select a topic or ask me anything!",
      timestamp: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
    },
  ]);
  const [selectedTopic, setSelectedTopic] = useState<string | null>(null);
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatHistory]);

  const handleTopicSelect = (topic: string) => {
    setSelectedTopic(topic);
    const timestamp = new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
    setChatHistory([
      {
        sender: "Eva",
        text: `You've selected the topic: ${topic}. How can I assist you with this topic?`,
        timestamp,
      },
    ]);
  };

  const handleBackToMenu = () => {
    setSelectedTopic(null);
    setChatHistory([
      {
        sender: "Eva",
        text: "Welcome back! How else can I assist you today?",
        timestamp: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      },
    ]);
    setMessage("");
  };

  const sendMessage = async (messageToSend = message) => {
    if (!messageToSend.trim()) return;
    const timestamp = new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });

    setChatHistory((prev) => [
      ...prev,
      { sender: "User", text: messageToSend, timestamp },
    ]);
    setIsLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: messageToSend, topic: selectedTopic }),
      });
      const data = await res.json();

      if (typeof data.response === "string") {
        setChatHistory((prev) => [
          ...prev,
          {
            sender: "Eva",
            text: data.response,
            timestamp: new Date().toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            }),
          },
        ]);
      }
    } catch (error) {
      console.error("Error:", error);
      setChatHistory((prev) => [
        ...prev,
        { sender: "Eva", text: "Sorry, something went wrong.", timestamp },
      ]);
    }

    setMessage("");
    setIsLoading(false);
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter" && !isLoading) {
      sendMessage();
    }
  };

  const handleQuickResponse = (quickMessage: string) => {
    setMessage(quickMessage);
    sendMessage(quickMessage);
  };

  const renderChatMessages = () => (
    <div className="h-[400px] overflow-y-auto p-6 bg-gray-50">
      {chatHistory.map((chat, index) => (
        <div
          key={index}
          className={`flex ${
            chat.sender === "Eva" ? "justify-start" : "justify-end"
          } mb-4`}
        >
          <div
            className={`flex flex-col ${
              chat.sender === "Eva" ? "items-start" : "items-end"
            }`}
          >
            {chat.sender === "Eva" && (
              <div className="flex items-center gap-2 mb-1">
                <Avatar className="w-6 h-6">
                  <AvatarImage src="nextjs\src\image\chatbot-avatar-v1.png" />
                  <AvatarFallback className="text-xs">EVA</AvatarFallback>
                </Avatar>
                <span className="text-xs text-gray-400">{chat.timestamp}</span>
              </div>
            )}
            <div
              className={`p-3 rounded-2xl max-w-[80%] ${
                chat.sender === "Eva"
                  ? "bg-white text-gray-800 rounded-tl-none shadow-sm"
                  : "bg-blue-600 text-white rounded-tr-none"
              }`}
            >
              {chat.text}
            </div>
            {chat.sender === "User" && (
              <span className="text-xs text-gray-400 mt-1">
                {chat.timestamp}
              </span>
            )}
          </div>
        </div>
      ))}
      <div ref={chatEndRef} />
    </div>
  );

  return (
    <Card className="max-w-lg mx-auto mt-10 shadow-xl border-0">
      <CardHeader className="border-b bg-white">
        <div className="flex items-center gap-3">
          {selectedTopic && (
            <Button
              variant="ghost"
              size="icon"
              className="mr-2 text-gray-600 hover:text-gray-800"
              onClick={handleBackToMenu}
            >
              <ArrowLeft size={20} />
            </Button>
          )}
          <Avatar>
            <AvatarImage src="nextjs\src\image\chatbot-avatar-v1.png" />
            <AvatarFallback className="bg-white text-[#0066ff]">
              EVA
            </AvatarFallback>
          </Avatar>
          <div>
            <CardTitle className="text-lg font-medium">Eva Assistant</CardTitle>
            <p className="text-sm text-gray-500">
              Usually replies in a few minutes
            </p>
          </div>
          <Button
            variant="ghost"
            size="icon"
            className="ml-auto text-gray-600 hover:text-gray-800"
          >
            <ChevronDown size={20} />
          </Button>
        </div>
      </CardHeader>

      <CardContent className="p-0">
        {!selectedTopic ? (
          <div className="flex flex-col">
            {renderChatMessages()}
            <div className="p-6 bg-[#0066ff]/5 border-b">
              <h3 className="text-lg font-medium mb-2 text-[#0066ff]">
                Quick Access Topics
              </h3>
              <p className="text-sm text-gray-500 mb-4">
                Select from above menu for quick advice or start chat to find
                out more about me and our sources
              </p>
              <div className="grid grid-cols-2 gap-2">
                {topics.map((topic) => (
                  <Button
                    key={topic}
                    variant="outline"
                    className="bg-gray-50 hover:bg-gray-100 text-gray-700"
                    onClick={() => handleTopicSelect(topic)}
                  >
                    {topic}
                  </Button>
                ))}
              </div>
            </div>

            <div className="p-4">
              <div className="flex items-center gap-2">
                <Input
                  type="text"
                  className="flex-1"
                  placeholder="Ask me anything..."
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyDown={handleKeyDown}
                />
                <Button
                  onClick={() => sendMessage()}
                  className="bg-[#0066ff] hover:bg-[#0066ff]/90"
                >
                  <Send size={20} />
                </Button>
              </div>
            </div>
          </div>
        ) : (
          <>
            {renderChatMessages()}
            <div className="p-4 border-t bg-white">
              {!isLoading && (
                <div className="mb-4 flex gap-2 overflow-x-auto pb-2">
                  <QuickResponseButton
                    text="Tell me more about this topic"
                    onSend={handleQuickResponse}
                  />
                  <QuickResponseButton
                    text="What are the best practices?"
                    onSend={handleQuickResponse}
                  />
                </div>
              )}

              <div className="flex items-center gap-2">
                <Button
                  variant="ghost"
                  size="icon"
                  className="text-gray-400 hover:text-gray-600"
                >
                  <Paperclip size={20} />
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  className="text-gray-400 hover:text-gray-600"
                >
                  <Smile size={20} />
                </Button>
                <Input
                  type="text"
                  className="flex-1"
                  placeholder={
                    isLoading ? "Eva is typing..." : "Type your message..."
                  }
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyDown={handleKeyDown}
                  disabled={isLoading}
                />
                <Button
                  onClick={() => sendMessage()}
                  disabled={isLoading}
                  className="bg-blue-600 hover:bg-blue-700"
                >
                  <Send size={20} />
                </Button>
              </div>
            </div>
          </>
        )}
      </CardContent>
    </Card>
  );
};

export default Chatbot;
