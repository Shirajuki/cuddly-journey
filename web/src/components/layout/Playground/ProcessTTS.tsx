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
import { poll } from "@/api/poll";
import { apiProcessTTS, apiTestTTS } from "@/api/processTTS";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Textarea } from "@/components/ui/textarea";

export default function TTS() {
  const { startProcess, finishProcess, progress, setProgress, disabled, files } = useProcessing();
  const [engine, setEngine] = useState("edge");
  const [voice, setVoice] = useState("vi-VN-HoaiMyNeural");
  const inputRef = useRef<HTMLInputElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const voices = useMemo(() => {
    if (engine === "edge") return TTS_EDGE_VOICES;
    if (engine === "volcengine") return TTS_VOLCENGINE_VOICES;
    if (engine === "youdao") return TTS_YOUDAO_VOICES;
  }, [engine]);

  const convertTTS = useCallback(async () => {
    startProcess();
    poll({ progressCallback: setProgress, type: "process-tts" });
    const { files } = await apiProcessTTS({ engine, voice, input: inputRef.current?.value });
    setTimeout(() => {
      finishProcess(files);
    }, 2000);
  }, [engine, finishProcess, startProcess, setProgress, voice]);

  const testTTS = useCallback(async () => {
    startProcess();
    poll({ progressCallback: setProgress, type: "test-tts" });
    const { files } = await apiTestTTS({ engine, voice, input: textareaRef.current?.value });
    setTimeout(() => {
      finishProcess(files);
    }, 2000);
  }, [engine, finishProcess, startProcess, setProgress, voice]);

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

        <Card className="bg-black/45">
          <CardContent className="h-full flex flex-col gap-4">
            <Accordion type="single" collapsible>
              <AccordionItem value="item-1">
                <AccordionTrigger>Test TTS</AccordionTrigger>
                <AccordionContent className="h-full flex flex-col gap-4">
                  <div>
                    <p className="text-base font-bold">Text input</p>
                    <p className="text-sm text-muted-foreground">
                      The text input to test the TTS voice output.
                    </p>
                  </div>
                  <div className="flex gap-4">
                    <div className="space-y-1 w-full">
                      <Textarea ref={textareaRef} className="h-full resize-none" />
                    </div>
                  </div>
                  <Button variant="outline" onClick={testTTS} disabled={disabled}>
                    {disabled ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <></>}
                    Test TTS
                  </Button>
                </AccordionContent>
              </AccordionItem>
            </Accordion>
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
