import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import ExtractSRT from "./ExtractSRT";
import ProcessSRT from "./ProcessSRT";
import ProcessAudio from "./ProcessAudio";
import ProcessTTS from "./ProcessTTS";

export default function PlaygroundPage() {
  return (
    <>
      <div className="mb-6">
        <h1 className="text-4xl font-semibold mb-1">Playground</h1>
        <p className="text-sm text-muted-foreground">
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Blanditiis sequi dolor et animi, ab porro tenetur
          accusamus rerum architecto quis!
        </p>
      </div>
      <Tabs defaultValue="extract-srt" className="">
        <TabsList className="">
          <TabsTrigger value="extract-srt">Extract SRT</TabsTrigger>
          <TabsTrigger value="process-srt">Process SRT</TabsTrigger>
          <TabsTrigger value="process-tts">Process TTS</TabsTrigger>
          <TabsTrigger value="process-audio">Process audio</TabsTrigger>
          <TabsTrigger value="ai-translate">AI Translate</TabsTrigger>
        </TabsList>

        <TabsContent value="extract-srt">
          <ExtractSRT />
        </TabsContent>

        <TabsContent value="process-srt">
          <ProcessSRT />
        </TabsContent>

        <TabsContent value="process-tts">
          <ProcessTTS />
        </TabsContent>

        <TabsContent value="process-audio">
          <ProcessAudio />
        </TabsContent>

        <TabsContent value="ai-translate">
          <Card>
            <CardHeader>
              <CardTitle>AI translate</CardTitle>
              <CardDescription>Card Description</CardDescription>
            </CardHeader>
            <CardContent>
              <p>Card Content</p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </>
  );
}
