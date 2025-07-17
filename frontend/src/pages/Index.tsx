import { useState } from "react";
import { WelcomeScreen } from "@/components/WelcomeScreen";
import { LiveTranslationScreen } from "@/components/LiveTranslationScreen";
import { ChatInterface } from "@/components/ChatInterface";
import { SettingsScreen } from "@/components/SettingsScreen";

type Screen = 'welcome' | 'translation' | 'chat' | 'settings';

const Index = () => {
  const [currentScreen, setCurrentScreen] = useState<Screen>('welcome');

  const renderScreen = () => {
    switch (currentScreen) {
      case 'welcome':
        return <WelcomeScreen onGetStarted={() => setCurrentScreen('translation')} />;
      case 'translation':
        return (
          <LiveTranslationScreen 
            onBack={() => setCurrentScreen('welcome')}
            onSettings={() => setCurrentScreen('settings')}
            onOpenChat={() => setCurrentScreen('chat')}
          />
        );
      case 'chat':
        return <ChatInterface onBack={() => setCurrentScreen('translation')} />;
      case 'settings':
        return <SettingsScreen onBack={() => setCurrentScreen('translation')} />;
      default:
        return <WelcomeScreen onGetStarted={() => setCurrentScreen('translation')} />;
    }
  };

  return (
    <div className="w-full">
      {renderScreen()}
    </div>
  );
};

export default Index;
