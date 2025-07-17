import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Switch } from "@/components/ui/switch";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { ArrowLeft, User, Globe, Volume2, Camera, Palette, Info, LogOut } from "lucide-react";

interface SettingsScreenProps {
  onBack: () => void;
}

export const SettingsScreen = ({ onBack }: SettingsScreenProps) => {
  const [settings, setSettings] = useState({
    primaryLanguage: "isl",
    voiceEnabled: true,
    cameraEnabled: true,
    highContrast: false,
    handDetectionSensitivity: "medium",
    avatarStyle: "realistic",
    autoSpeak: false,
    saveHistory: true
  });

  const updateSetting = (key: string, value: any) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="flex items-center justify-between p-4 bg-card/50 backdrop-blur-sm border-b border-border">
        <Button variant="ghost" size="icon" onClick={onBack}>
          <ArrowLeft className="w-5 h-5" />
        </Button>
        <h1 className="text-lg font-semibold text-foreground">Settings</h1>
        <div></div>
      </div>

      <div className="p-4 space-y-6 max-w-2xl mx-auto">
        {/* Profile Section */}
        <Card className="p-6">
          <div className="flex items-center gap-4 mb-4">
            <div className="w-16 h-16 bg-gradient-teal rounded-full flex items-center justify-center">
              <User className="w-8 h-8 text-white" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-foreground">Welcome User</h3>
              <p className="text-sm text-muted-foreground">SignBridge Premium</p>
            </div>
          </div>
          <Button variant="outline" className="w-full">
            Edit Profile
          </Button>
        </Card>

        {/* Language Settings */}
        <Card className="p-6">
          <div className="flex items-center gap-3 mb-4">
            <Globe className="w-5 h-5 text-secondary" />
            <h3 className="text-lg font-semibold text-foreground">Language</h3>
          </div>
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium text-muted-foreground">Primary Sign Language</label>
              <Select value={settings.primaryLanguage} onValueChange={(value) => updateSetting('primaryLanguage', value)}>
                <SelectTrigger className="mt-2">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="isl">Indian Sign Language (ISL)</SelectItem>
                  <SelectItem value="asl">American Sign Language (ASL)</SelectItem>
                  <SelectItem value="bsl">British Sign Language (BSL)</SelectItem>
                  <SelectItem value="fsl">French Sign Language (FSL)</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </Card>

        {/* Audio & Video Settings */}
        <Card className="p-6">
          <div className="flex items-center gap-3 mb-4">
            <Volume2 className="w-5 h-5 text-accent" />
            <h3 className="text-lg font-semibold text-foreground">Audio & Video</h3>
          </div>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-foreground">Voice Output</p>
                <p className="text-xs text-muted-foreground">Enable text-to-speech</p>
              </div>
              <Switch 
                checked={settings.voiceEnabled} 
                onCheckedChange={(checked) => updateSetting('voiceEnabled', checked)}
              />
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-foreground">Camera Access</p>
                <p className="text-xs text-muted-foreground">Allow sign language detection</p>
              </div>
              <Switch 
                checked={settings.cameraEnabled} 
                onCheckedChange={(checked) => updateSetting('cameraEnabled', checked)}
              />
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-foreground">Auto-Speak</p>
                <p className="text-xs text-muted-foreground">Automatically speak detected text</p>
              </div>
              <Switch 
                checked={settings.autoSpeak} 
                onCheckedChange={(checked) => updateSetting('autoSpeak', checked)}
              />
            </div>
          </div>
        </Card>

        {/* Detection Settings */}
        <Card className="p-6">
          <div className="flex items-center gap-3 mb-4">
            <Camera className="w-5 h-5 text-gold" />
            <h3 className="text-lg font-semibold text-foreground">Detection</h3>
          </div>
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium text-muted-foreground">Hand Detection Sensitivity</label>
              <Select value={settings.handDetectionSensitivity} onValueChange={(value) => updateSetting('handDetectionSensitivity', value)}>
                <SelectTrigger className="mt-2">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="low">Low - Less sensitive</SelectItem>
                  <SelectItem value="medium">Medium - Balanced</SelectItem>
                  <SelectItem value="high">High - Very sensitive</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <label className="text-sm font-medium text-muted-foreground">Avatar Style</label>
              <Select value={settings.avatarStyle} onValueChange={(value) => updateSetting('avatarStyle', value)}>
                <SelectTrigger className="mt-2">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="realistic">Realistic 3D</SelectItem>
                  <SelectItem value="cartoon">Cartoon Style</SelectItem>
                  <SelectItem value="minimal">Minimal Icons</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </Card>

        {/* Accessibility Settings */}
        <Card className="p-6">
          <div className="flex items-center gap-3 mb-4">
            <Palette className="w-5 h-5 text-muted-foreground" />
            <h3 className="text-lg font-semibold text-foreground">Accessibility</h3>
          </div>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-foreground">High Contrast</p>
                <p className="text-xs text-muted-foreground">Enhance visual contrast</p>
              </div>
              <Switch 
                checked={settings.highContrast} 
                onCheckedChange={(checked) => updateSetting('highContrast', checked)}
              />
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-foreground">Save Chat History</p>
                <p className="text-xs text-muted-foreground">Keep conversation logs</p>
              </div>
              <Switch 
                checked={settings.saveHistory} 
                onCheckedChange={(checked) => updateSetting('saveHistory', checked)}
              />
            </div>
          </div>
        </Card>

        {/* App Info */}
        <Card className="p-6">
          <div className="flex items-center gap-3 mb-4">
            <Info className="w-5 h-5 text-muted-foreground" />
            <h3 className="text-lg font-semibold text-foreground">About</h3>
          </div>
          <div className="space-y-3">
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Version</span>
              <span className="text-foreground">1.0.0</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Build</span>
              <span className="text-foreground">2024.01.15</span>
            </div>
            <Button variant="outline" className="w-full mt-4">
              Privacy Policy
            </Button>
            <Button variant="outline" className="w-full">
              Terms of Service
            </Button>
          </div>
        </Card>

        {/* Logout */}
        <Card className="p-6">
          <Button variant="destructive" className="w-full">
            <LogOut className="w-4 h-4 mr-2" />
            Sign Out
          </Button>
        </Card>
      </div>
    </div>
  );
};