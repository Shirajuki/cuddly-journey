import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Progress } from "@/components/ui/progress";
import { TTS_EDGE_VOICES, TTS_VOLCENGINE_VOICES, TTS_YOUDAO_VOICES } from "@/lib/consts";
import { Loader2 } from "lucide-react";
import { useCallback, useMemo, useRef, useState } from "react";
import { Input } from "@/components/ui/input";
import Divider from "@/components/custom/Divider";
import File from "@/components/custom/File";
import useProcessing from "@/lib/useProcessing";

export default function TTS() {
  const { reset, finish, progress, setProgress, disabled, files } = useProcessing();
  const [engine, setEngine] = useState("edge");
  const [voice, setVoice] = useState("vi-VN-HoaiMyNeural");
  const inputRef = useRef<HTMLInputElement>(null);

  const voices = useMemo(() => {
    if (engine === "edge") return TTS_EDGE_VOICES;
    if (engine === "volcengine") return TTS_VOLCENGINE_VOICES;
    if (engine === "youdao") return TTS_YOUDAO_VOICES;
  }, [engine]);

  const convertTTS = useCallback(async () => {
    // Reset status
    reset();

    // Start fetching progress intervally
    const interval = setInterval(async () => {
      const res = await fetch("http://localhost:3000/api/progress?type=process-tts");
      const progress = Number(await res.text());
      setProgress(progress);
      if (progress >= 100) {
        clearInterval(interval);
      }
    }, 2000);

    // Request process TTS
    const res = await fetch("http://localhost:3000/api/process-tts", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        engine: engine,
        voice: voice,
        input: inputRef.current?.value,
      }),
    });

    // Retrieve response containing file list, making sure to update right after progress
    const files = await res.json();
    setTimeout(() => {
      finish(files);
    }, 2000);
  }, [engine, finish, reset, setProgress, voice]);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Process TTS</CardTitle>
        <CardDescription>Includes scripts for audio generation through audio inference and TTS</CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <Card className="w-full bg-black/45">
          <CardContent className="pt-6 h-full flex flex-col gap-4">
            <div>
              <p className="text-base font-bold">Input and output files</p>
              <p className="text-sm text-muted-foreground">The absolute system path to the files.</p>
            </div>
            <div className="space-y-1">
              <Label htmlFor="video-input">SRT input (.srt)</Label>
              <Input id="video-input" defaultValue="/tmp/input.srt" ref={inputRef} />
            </div>
          </CardContent>
        </Card>

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

        <Button variant="outline" onClick={convertTTS} disabled={disabled}>
          {disabled ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <></>}
          Convert TTS
        </Button>

        <Divider />

        <Card className="w-full">
          <CardContent className="pt-6 flex flex-col justify-center items-center gap-4">
            <div className="space-y-1 w-full">
              <Progress value={progress} />
            </div>
            <div className="space-y-1 w-full">
              {files.map((filename) => (
                <File filename={filename} key={filename} />
              ))}
            </div>
          </CardContent>
        </Card>
      </CardContent>
    </Card>
  );
}
