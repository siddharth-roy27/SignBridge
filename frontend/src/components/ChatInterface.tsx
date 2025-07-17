import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Send, Mic, Camera, ArrowLeft, Bot, User } from "lucide-react";

interface Message {
  id: string;
  type: 'user' | 'ai';
  content: string;
  timestamp: Date;
  mode: 'text' | 'sign' | 'voice';
}

interface ChatInterfaceProps {
  onBack: () => void;
}

export const ChatInterface = ({ onBack }: ChatInterfaceProps) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'ai',
      content: 'Hello! I can help translate between sign language, text, and speech. How would you like to communicate?',
      timestamp: new Date(),
      mode: 'text'
    }
  ]);
  const [inputText, setInputText] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [showAvatar, setShowAvatar] = useState(true);
  const videoRef = useRef<HTMLVideoElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    // Initialize camera for sign language input
    const startCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (error) {
        console.error("Error accessing camera:", error);
      }
    };

    startCamera();
  }, []);

  const sendMessage = (content: string, mode: 'text' | 'sign' | 'voice' = 'text') => {
    const newMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content,
      timestamp: new Date(),
      mode
    };

    setMessages(prev => [...prev, newMessage]);

    // Simulate AI response
    setTimeout(() => {
      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        type: 'ai',
        content: `I understand you said "${content}". Here's the sign language translation:`,
        timestamp: new Date(),
        mode: 'text'
      };
      setMessages(prev => [...prev, aiResponse]);
    }, 1000);

    setInputText("");
  };

  const handleSendText = () => {
    if (inputText.trim()) {
      sendMessage(inputText, 'text');
    }
  };

  const handleVoiceInput = () => {
    setIsRecording(!isRecording);
    if (!isRecording) {
      // Simulate voice recording
      setTimeout(() => {
        sendMessage("Hello, how are you?", 'voice');
        setIsRecording(false);
      }, 2000);
    }
  };

  const handleSignInput = () => {
    sendMessage("👋 Hello! Nice to meet you.", 'sign');
  };

  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between p-4 bg-card/50 backdrop-blur-sm border-b border-border">
        <Button variant="ghost" size="icon" onClick={onBack}>
          <ArrowLeft className="w-5 h-5" />
        </Button>
        <h1 className="text-lg font-semibold text-foreground">SignBridge Chat</h1>
        <Button 
          variant="ghost" 
          size="sm"
          onClick={() => setShowAvatar(!showAvatar)}
        >
          {showAvatar ? 'Hide Avatar' : 'Show Avatar'}
        </Button>
      </div>

      <div className="flex-1 flex">
        {/* Chat Messages */}
        <div className="flex-1 flex flex-col">
          <div className="flex-1 p-4 overflow-y-auto">
            <div className="space-y-4 max-w-2xl mx-auto">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex items-start gap-3 ${
                    message.type === 'user' ? 'flex-row-reverse' : ''
                  }`}
                >
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                    message.type === 'user' 
                      ? 'bg-gradient-teal' 
                      : 'bg-gradient-violet'
                  }`}>
                    {message.type === 'user' ? (
                      <User className="w-4 h-4 text-white" />
                    ) : (
                      <Bot className="w-4 h-4 text-white" />
                    )}
                  </div>
                  <div className={`flex-1 max-w-xs lg:max-w-md ${
                    message.type === 'user' ? 'text-right' : ''
                  }`}>
                    <div className={`p-3 rounded-lg ${
                      message.type === 'user'
                        ? 'bg-gradient-teal text-white'
                        : 'bg-card text-card-foreground'
                    }`}>
                      <p className="text-sm">{message.content}</p>
                      <div className="flex items-center gap-2 mt-2 text-xs opacity-70">
                        <span>{message.mode}</span>
                        <span>•</span>
                        <span>{message.timestamp.toLocaleTimeString()}</span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
          </div>

          {/* Input Area */}
          <div className="p-4 bg-card/30 backdrop-blur-sm border-t border-border">
            <div className="max-w-2xl mx-auto">
              <div className="flex items-center gap-2 mb-3">
                <div className="flex-1 flex items-center gap-2 bg-background rounded-lg p-2">
                  <Input
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    placeholder="Type a message..."
                    className="border-0 bg-transparent focus-visible:ring-0"
                    onKeyPress={(e) => e.key === 'Enter' && handleSendText()}
                  />
                  <Button size="icon" variant="ghost" onClick={handleSendText}>
                    <Send className="w-4 h-4" />
                  </Button>
                </div>
              </div>
              
              <div className="flex justify-center gap-4">
                <Button
                  variant={isRecording ? "destructive" : "gold"}
                  size="icon"
                  onClick={handleVoiceInput}
                  className="rounded-full"
                >
                  <Mic className="w-4 h-4" />
                </Button>
                <Button
                  variant="teal"
                  size="icon"
                  onClick={handleSignInput}
                  className="rounded-full"
                >
                  <Camera className="w-4 h-4" />
                </Button>
              </div>
            </div>
          </div>
        </div>

        {/* Avatar Panel */}
        {showAvatar && (
          <div className="w-80 bg-card/50 backdrop-blur-sm border-l border-border">
            <div className="p-4">
              <h3 className="text-sm font-medium text-muted-foreground mb-4">Sign Language Avatar</h3>
              <div className="aspect-square bg-muted/30 rounded-lg flex items-center justify-center mb-4">
                <div className="text-6xl">🧑‍🦽</div>
              </div>
              <div className="space-y-2 text-xs text-muted-foreground">
                <p>• Real-time sign translation</p>
                <p>• Multiple sign languages</p>
                <p>• Animated demonstrations</p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Live Camera Feed for Sign Input */}
      <div className="fixed bottom-20 right-4 w-32 h-24 bg-card rounded-lg overflow-hidden shadow-lg">
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="w-full h-full object-cover"
        />
        <div className="absolute top-1 right-1 w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
      </div>
    </div>
  );
};