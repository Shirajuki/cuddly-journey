import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import ExtractSRT from "./ExtractSRT";
import ProcessSRT from "./ProcessSRT";
import ProcessAudio from "./ProcessAudio";
import ProcessTTS from "./ProcessTTS";
import { type PlaygroundTabsOptions, Route } from "@/routes/playground";
import { useNavigate } from "@tanstack/react-router";

export default function PlaygroundPage() {
  const navigate = useNavigate({ from: Route.fullPath });
  const { tab } = Route.useSearch();

  const tabsChangeHandler = (value: PlaygroundTabsOptions) => {
    navigate({
      search: () => ({ tab: value }),
    });
  };

  return (
    <>
      <div className="mb-6">
        <h1 className="text-4xl font-semibold mb-1">Playground</h1>
        <p className="text-sm text-muted-foreground">Try out the standalone scripts and all of its features here.</p>
      </div>
      <Tabs defaultValue={tab}>
        <TabsList className="">
          <TabsTrigger value="extract-srt" onClick={() => tabsChangeHandler("extract-srt")}>
            Extract SRT
          </TabsTrigger>
          <TabsTrigger value="process-srt" onClick={() => tabsChangeHandler("process-srt")}>
            Process SRT
          </TabsTrigger>
          <TabsTrigger value="process-tts" onClick={() => tabsChangeHandler("process-tts")}>
            Process TTS
          </TabsTrigger>
          <TabsTrigger value="process-audio" onClick={() => tabsChangeHandler("process-audio")}>
            Process audio
          </TabsTrigger>
          {/* <TabsTrigger value="ai-translate" onClick={() => tabsChangeHandler("ai-translate")}>
            AI Translate
          </TabsTrigger> */}
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
              <CardDescription>TBA</CardDescription>
            </CardHeader>
            <CardContent>
              <p>TBA</p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </>
  );
}
