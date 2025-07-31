import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Camera, Eye, History, MessageSquare, Loader2 } from 'lucide-react';
import { toast } from '@/components/ui/use-toast';

interface Screenshot {
  id: string;
  url: string;
  timestamp: string;
  viewport: { width: number; height: number };
  file_path: string;
  file_size: number;
  metadata?: any;
  annotations?: any[];
}

interface VisionPanelProps {
  apiUrl?: string;
}

export const VisionPanel: React.FC<VisionPanelProps> = ({ 
  apiUrl = 'http://localhost:8000' 
}) => {
  const [isCapturing, setIsCapturing] = useState(false);
  const [captureUrl, setCaptureUrl] = useState(window.location.href);
  const [screenshots, setScreenshots] = useState<Screenshot[]>([]);
  const [selectedScreenshot, setSelectedScreenshot] = useState<Screenshot | null>(null);
  const [annotation, setAnnotation] = useState('');

  // Fetch screenshot history on mount
  useEffect(() => {
    fetchScreenshotHistory();
  }, []);

  const fetchScreenshotHistory = async () => {
    try {
      const response = await fetch(`${apiUrl}/api/vision/history`);
      const data = await response.json();
      if (data.success) {
        setScreenshots(data.screenshots);
      }
    } catch (error) {
      console.error('Failed to fetch history:', error);
    }
  };

  const captureCurrentPage = async () => {
    setIsCapturing(true);
    try {
      const response = await fetch(`${apiUrl}/api/vision/capture`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          url: captureUrl,
          viewport: { width: window.innerWidth, height: window.innerHeight },
          full_page: true
        })
      });

      const data = await response.json();
      if (data.success) {
        toast({
          title: "Screenshot captured!",
          description: `ID: ${data.screenshot.id}`
        });
        fetchScreenshotHistory(); // Refresh history
      }
    } catch (error) {
      toast({
        title: "Capture failed",
        description: error.message,
        variant: "destructive"
      });
    } finally {
      setIsCapturing(false);
    }
  };

  const addAnnotation = async () => {
    if (!selectedScreenshot || !annotation.trim()) return;

    try {
      const response = await fetch(`${apiUrl}/api/vision/annotate/${selectedScreenshot.id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          author: 'CASCADE Team',
          type: 'observation',
          content: annotation
        })
      });

      const data = await response.json();
      if (data.success) {
        toast({
          title: "Annotation added",
          description: "Your note has been saved"
        });
        setAnnotation('');
        fetchScreenshotHistory(); // Refresh to show new annotation
      }
    } catch (error) {
      toast({
        title: "Failed to add annotation",
        description: error.message,
        variant: "destructive"
      });
    }
  };

  return (
    <Card className="w-full max-w-6xl mx-auto">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Eye className="w-6 h-6" />
          CASCADE Vision System
        </CardTitle>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="capture" className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="capture">
              <Camera className="w-4 h-4 mr-2" />
              Capture
            </TabsTrigger>
            <TabsTrigger value="history">
              <History className="w-4 h-4 mr-2" />
              History
            </TabsTrigger>
            <TabsTrigger value="annotate">
              <MessageSquare className="w-4 h-4 mr-2" />
              Annotate
            </TabsTrigger>
          </TabsList>

          <TabsContent value="capture" className="space-y-4">
            <div className="flex gap-2">
              <Input
                value={captureUrl}
                onChange={(e) => setCaptureUrl(e.target.value)}
                placeholder="Enter URL to capture..."
                className="flex-1"
              />
              <Button 
                onClick={captureCurrentPage}
                disabled={isCapturing}
              >
                {isCapturing ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Capturing...
                  </>
                ) : (
                  <>
                    <Camera className="w-4 h-4 mr-2" />
                    Capture
                  </>
                )}
              </Button>
            </div>

            <div className="text-sm text-muted-foreground">
              <p>Capture the visual state of any CASCADE page for debugging and design review.</p>
              <p className="mt-2">Features:</p>
              <ul className="list-disc list-inside ml-4">
                <li>Full page screenshots</li>
                <li>Multiple viewport sizes</li>
                <li>Annotation support</li>
                <li>Visual history tracking</li>
              </ul>
            </div>
          </TabsContent>

          <TabsContent value="history" className="space-y-4">
            <div className="grid gap-4">
              {screenshots.length === 0 ? (
                <p className="text-center text-muted-foreground py-8">
                  No screenshots captured yet
                </p>
              ) : (
                screenshots.map((screenshot) => (
                  <div 
                    key={screenshot.id}
                    className="border rounded-lg p-4 hover:bg-accent cursor-pointer"
                    onClick={() => setSelectedScreenshot(screenshot)}
                  >
                    <div className="flex justify-between items-start">
                      <div>
                        <p className="font-medium text-sm">{screenshot.url}</p>
                        <p className="text-xs text-muted-foreground">
                          {new Date(screenshot.timestamp).toLocaleString()}
                        </p>
                      </div>
                      <div className="text-xs text-muted-foreground">
                        {screenshot.viewport.width}x{screenshot.viewport.height}
                      </div>
                    </div>
                    {screenshot.annotations && screenshot.annotations.length > 0 && (
                      <div className="mt-2">
                        <span className="text-xs bg-primary/10 text-primary px-2 py-1 rounded">
                          {screenshot.annotations.length} annotations
                        </span>
                      </div>
                    )}
                  </div>
                ))
              )}
            </div>
          </TabsContent>

          <TabsContent value="annotate" className="space-y-4">
            {selectedScreenshot ? (
              <>
                <div className="border rounded-lg p-4">
                  <p className="font-medium">{selectedScreenshot.url}</p>
                  <p className="text-sm text-muted-foreground">
                    ID: {selectedScreenshot.id}
                  </p>
                </div>

                <div className="space-y-2">
                  <Input
                    value={annotation}
                    onChange={(e) => setAnnotation(e.target.value)}
                    placeholder="Add a note about this screenshot..."
                  />
                  <Button 
                    onClick={addAnnotation}
                    disabled={!annotation.trim()}
                    className="w-full"
                  >
                    Add Annotation
                  </Button>
                </div>

                {selectedScreenshot.annotations && selectedScreenshot.annotations.length > 0 && (
                  <div className="space-y-2">
                    <h4 className="font-medium">Existing Annotations:</h4>
                    {selectedScreenshot.annotations.map((ann, idx) => (
                      <div key={idx} className="border-l-2 pl-3 text-sm">
                        <p>{ann.content}</p>
                        <p className="text-xs text-muted-foreground">
                          {ann.author} - {new Date(ann.timestamp).toLocaleString()}
                        </p>
                      </div>
                    ))}
                  </div>
                )}
              </>
            ) : (
              <p className="text-center text-muted-foreground py-8">
                Select a screenshot from the history to annotate
              </p>
            )}
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
};