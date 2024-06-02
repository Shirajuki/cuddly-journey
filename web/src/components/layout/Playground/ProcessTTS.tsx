import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Progress } from "@/components/ui/progress";
import { TTS_EDGE_VOICES, TTS_VOLCENGINE_VOICES, TTS_YOUDAO_VOICES } from "@/lib/consts";
import { Loader2 } from "lucide-react";
import { useCallback, useMemo, useRef, useState } from "react";

export default function TTS() {
  const [engine, setEngine] = useState("edge");
  const [voice, setVoice] = useState("vi-VN-HoaiMyNeural");
  const [progress, setProgress] = useState(0);
  const [disabled, setDisabled] = useState(false);
  const [files, setFiles] = useState<string[]>([]);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const voices = useMemo(() => {
    if (engine === "edge") return TTS_EDGE_VOICES;
    if (engine === "volcengine") return TTS_VOLCENGINE_VOICES;
    if (engine === "youdao") return TTS_YOUDAO_VOICES;
  }, [engine]);

  const convertTTS = useCallback(async () => {
    setDisabled(true);
    const interval = setInterval(async () => {
      const res = await fetch("http://localhost:3000/api/progress?type=process-tts");
      const progress = Number(await res.text());
      setProgress(progress);
      if (progress >= 100) {
        clearInterval(interval);
      }
    }, 2000);
    const res = await fetch("http://localhost:3000/api/process-tts", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        engine: engine,
        voice: voice,
        text: textareaRef.current?.value,
      }),
    });
    const files = [...(await res.json())].reverse();
    setFiles(files);
    setDisabled(false);
  }, [engine, voice]);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Process TTS</CardTitle>
        <CardDescription>Includes scripts for audio generation through audio inference and TTS</CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <Card className="bg-black/45">
          <CardContent className="pt-6 h-full flex flex-col gap-4">
            <div className="space-y-1 w-full">
              <Label htmlFor="based-srt-input">TTS Engine</Label>
              <Select
                defaultValue="edge"
                onValueChange={(value: string) => {
                  setEngine(value);
                  setVoice("");
                }}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Edge" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="edge">Edge</SelectItem>
                  <SelectItem value="volcengine">Volcengine</SelectItem>
                  <SelectItem value="youdao">Youdao</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-1 w-full">
              <Label htmlFor="based-srt-input">TTS Voices</Label>
              <Select onValueChange={(value: string) => setVoice(value)} value={voice}>
                <SelectTrigger>
                  <SelectValue placeholder={voice} />
                </SelectTrigger>
                <SelectContent className="max-h-[280px]">
                  {voices?.map((voice) => (
                    <SelectItem value={voice.name} key={voice.name}>
                      {voice.name} {voice.gender ? `[${voice.gender}]` : ""}{" "}
                      {voice.language ? `[${voice.language}]` : ""}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-black/45">
          <CardContent className="pt-6 h-full flex flex-col gap-4">
            <div className="space-y-1 w-full">
              <Label htmlFor="based-srt-input">SRT to Synthesize</Label>
              <Textarea className="h-full resize-none" ref={textareaRef} />
            </div>
          </CardContent>
        </Card>

        <Button variant="outline" onClick={convertTTS} disabled={disabled}>
          {disabled ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <></>}
          Convert TTS
        </Button>
        <br />
        <hr />
        <br />

        <Card className="w-[calc(100%-1rem)]">
          <CardContent className="pt-6 flex flex-col justify-center items-center gap-4">
            <div className="space-y-1 w-full">
              <Progress value={progress} />
            </div>
            <div className="space-y-1 w-full">
              {files.map((filename) => (
                <div className="bg-white/5 rounded-md w-full">
                  <Button variant="link" key={filename}>
                    {filename}
                  </Button>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </CardContent>
    </Card>
  );
}
