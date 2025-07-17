import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Camera, Volume2, RotateCcw, Settings, ArrowLeft, MessageSquare } from "lucide-react";

interface LiveTranslationScreenProps {
  onBack: () => void;
  onSettings: () => void;
  onOpenChat: () => void;
}

export const LiveTranslationScreen = ({ onBack, onSettings, onOpenChat }: LiveTranslationScreenProps) => {
  const [detectedText, setDetectedText] = useState("Ready to detect sign language...");
  const [isRecording, setIsRecording] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState("isl");
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    // Initialize camera
    const startCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (error) {
        console.error("Error accessing camera:", error);
        setDetectedText("Camera access denied. Please enable camera permissions.");
      }
    };

    startCamera();
  }, []);

  const handleSpeak = () => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(detectedText);
      utterance.rate = 0.8;
      utterance.pitch = 1;
      speechSynthesis.speak(utterance);
    }
  };

  const toggleRecording = () => {
    setIsRecording(!isRecording);
    if (!isRecording) {
      setDetectedText("Detecting sign language...");
      // Here you would integrate with MediaPipe or your AI model
      setTimeout(() => {
        setDetectedText("Hello, how are you today?");
      }, 2000);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="flex items-center justify-between p-4 bg-card/50 backdrop-blur-sm">
        <Button variant="ghost" size="icon" onClick={onBack}>
          <ArrowLeft className="w-5 h-5" />
        </Button>
        <h1 className="text-lg font-semibold text-foreground">Live Translation</h1>
        <Button variant="ghost" size="icon" onClick={onSettings}>
          <Settings className="w-5 h-5" />
        </Button>
      </div>

      <div className="p-4 space-y-6">
        {/* Language Selection */}
        <Card className="p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-muted-foreground">Sign Language</span>
          </div>
          <Select value={selectedLanguage} onValueChange={setSelectedLanguage}>
            <SelectTrigger className="w-full">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="isl">Indian Sign Language (ISL)</SelectItem>
              <SelectItem value="asl">American Sign Language (ASL)</SelectItem>
              <SelectItem value="bsl">British Sign Language (BSL)</SelectItem>
            </SelectContent>
          </Select>
        </Card>

        {/* Camera Feed */}
        <Card className="relative overflow-hidden">
          <video
            ref={videoRef}
            autoPlay
            playsInline
            muted
            className="w-full h-64 object-cover rounded-lg"
          />
          <div className="absolute bottom-4 left-4 right-4 flex justify-between items-center">
            <div className={`flex items-center gap-2 px-3 py-1 rounded-full ${
              isRecording ? 'bg-destructive/90' : 'bg-card/90'
            } backdrop-blur-sm`}>
              <div className={`w-2 h-2 rounded-full ${
                isRecording ? 'bg-white animate-pulse' : 'bg-muted'
              }`}></div>
              <span className="text-xs text-white">
                {isRecording ? 'Recording' : 'Paused'}
              </span>
            </div>
            <Button
              variant={isRecording ? "destructive" : "teal"}
              size="icon"
              onClick={toggleRecording}
              className="rounded-full"
            >
              <Camera className="w-5 h-5" />
            </Button>
          </div>
        </Card>

        {/* Detected Text Output */}
        <Card className="p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-foreground">Detected Text</h3>
            <Button variant="ghost" size="icon">
              <RotateCcw className="w-4 h-4" />
            </Button>
          </div>
          <div className="mb-4">
            <p className="text-lg text-foreground leading-relaxed min-h-[60px] p-4 bg-muted/30 rounded-lg">
              {detectedText}
            </p>
          </div>
          <Button 
            variant="gold" 
            onClick={handleSpeak}
            className="w-full"
            disabled={detectedText === "Ready to detect sign language..." || detectedText === "Detecting sign language..."}
          >
            <Volume2 className="w-4 h-4 mr-2" />
            Speak Text
          </Button>
        </Card>

        {/* Quick Actions */}
        <div className="grid grid-cols-2 gap-4">
          <Card className="p-4 text-center cursor-pointer hover:bg-card/80 transition-colors" onClick={onOpenChat}>
            <MessageSquare className="w-6 h-6 text-secondary mx-auto mb-2" />
            <span className="text-sm text-muted-foreground">Open Chat</span>
          </Card>
          <Card className="p-4 text-center cursor-pointer hover:bg-card/80 transition-colors">
            <Volume2 className="w-6 h-6 text-accent mx-auto mb-2" />
            <span className="text-sm text-muted-foreground">Voice Mode</span>
          </Card>
        </div>
      </div>
    </div>
  );
};