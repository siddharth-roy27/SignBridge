import { Button } from "@/components/ui/button";
import { Camera, Mic, MessageSquare, Settings } from "lucide-react";

interface WelcomeScreenProps {
  onGetStarted: () => void;
}

export const WelcomeScreen = ({ onGetStarted }: WelcomeScreenProps) => {
  return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-center relative overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-20 left-10 w-32 h-32 bg-gradient-teal rounded-full blur-3xl"></div>
        <div className="absolute bottom-40 right-10 w-40 h-40 bg-gradient-violet rounded-full blur-3xl"></div>
        <div className="absolute top-1/2 left-1/4 w-20 h-20 bg-gold rounded-full blur-2xl"></div>
      </div>

      {/* Main Content */}
      <div className="relative z-10 text-center px-6 max-w-md mx-auto">
        {/* Logo/Icon */}
        <div className="mb-8">
          <div className="w-32 h-32 mx-auto bg-card rounded-full flex items-center justify-center shadow-teal">
            <div className="relative">
              {/* Sign Language Hand Icon */}
              <div className="w-20 h-20 bg-gradient-teal rounded-full flex items-center justify-center">
                <div className="text-4xl">👋</div>
              </div>
              {/* Communication Rings */}
              <div className="absolute -top-2 -right-2 w-6 h-6 bg-gold rounded-full animate-pulse"></div>
              <div className="absolute -bottom-2 -left-2 w-4 h-4 bg-accent rounded-full animate-pulse delay-300"></div>
            </div>
          </div>
        </div>

        {/* App Name */}
        <h1 className="text-4xl font-bold text-foreground mb-4 tracking-tight">
          SignBridge
        </h1>

        {/* Tagline */}
        <p className="text-lg text-secondary mb-12 leading-relaxed">
          Breaking Barriers with Sign Language AI
        </p>

        {/* Get Started Button */}
        <Button 
          variant="get-started" 
          size="xl" 
          onClick={onGetStarted}
          className="w-full mb-8 rounded-2xl"
        >
          Get Started
        </Button>

        {/* Feature Preview */}
        <div className="grid grid-cols-2 gap-4 mt-8">
          <div className="flex flex-col items-center p-4 bg-card/50 rounded-xl backdrop-blur-sm">
            <Camera className="w-6 h-6 text-secondary mb-2" />
            <span className="text-sm text-muted-foreground">Live Translation</span>
          </div>
          <div className="flex flex-col items-center p-4 bg-card/50 rounded-xl backdrop-blur-sm">
            <Mic className="w-6 h-6 text-accent mb-2" />
            <span className="text-sm text-muted-foreground">Voice to Sign</span>
          </div>
          <div className="flex flex-col items-center p-4 bg-card/50 rounded-xl backdrop-blur-sm">
            <MessageSquare className="w-6 h-6 text-gold mb-2" />
            <span className="text-sm text-muted-foreground">Chat History</span>
          </div>
          <div className="flex flex-col items-center p-4 bg-card/50 rounded-xl backdrop-blur-sm">
            <Settings className="w-6 h-6 text-muted-foreground mb-2" />
            <span className="text-sm text-muted-foreground">Customizable</span>
          </div>
        </div>
      </div>
    </div>
  );
};