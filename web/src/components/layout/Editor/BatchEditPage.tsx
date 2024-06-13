import Divider from "@/components/custom/Divider";
import File from "@/components/custom/File";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Textarea } from "@/components/ui/textarea";
import { Toggle } from "@/components/ui/toggle";
import { Loader2 } from "lucide-react";
import { useCallback, useRef, useState } from "react";

export default function BatchEditPage() {
  const [disabled, setDisabled] = useState(false);
  const [batchProgress, setBatchProgress] = useState([0, 0, 0, 0]);
  const [progressText, setProgressText] = useState("");
  const [files, setFiles] = useState<string[]>([]);

  const extractSRTRef = useRef<HTMLButtonElement>(null);
  const processSRTRef = useRef<HTMLButtonElement>(null);
  const processTTSRef = useRef<HTMLButtonElement>(null);
  const processAudioRef = useRef<HTMLButtonElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const processSRT = useCallback(async (filename: string) => {
    const interval = setInterval(async () => {
      const res = await fetch("http://localhost:3000/api/progress?type=process-srt");
      const progress = Number(await res.text());
      setBatchProgress((bprogress) => {
        const p = [...bprogress];
        p[1] = progress;
        return p;
      });
      if (progress >= 100) {
        clearInterval(interval);
      }
    }, 3000);

    await fetch("http://localhost:3000/api/process-srt", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        input: filename,
        options: {
          langdiff: false,
          merge: false,
          crosstalk: false,
        },
      }),
    });
    await new Promise((res) => setTimeout(res, 1000));
  }, []);

  const processTTS = useCallback(async (filename: string) => {
    const interval = setInterval(async () => {
      const res = await fetch("http://localhost:3000/api/progress?type=process-tts");
      const progress = Number(await res.text());
      setBatchProgress((bprogress) => {
        const p = [...bprogress];
        p[2] = progress;
        return p;
      });
      if (progress >= 100) {
        clearInterval(interval);
      }
    }, 3000);

    await fetch("http://localhost:3000/api/process-tts", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        engine: "edge",
        voice: "vi-VN-HoaiMyNeural",
        input: filename,
      }),
    });
    await new Promise((res) => setTimeout(res, 1000));
  }, []);

  const processAudio = useCallback(async () => {
    const interval = setInterval(async () => {
      const res = await fetch("http://localhost:3000/api/progress?type=process-audio");
      const progress = Number(await res.text());
      setBatchProgress((bprogress) => {
        const p = [...bprogress];
        p[3] = progress;
        return p;
      });
      if (progress >= 100) {
        clearInterval(interval);
      }
    }, 3000);

    await fetch("http://localhost:3000/api/process-audio", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        config: "standalone",
      }),
    });
    await new Promise((res) => setTimeout(res, 1000));
  }, []);

  const processBatch = useCallback(async () => {
    setBatchProgress([0, 0, 0, 0]);
    setDisabled(true);
    setFiles([]);

    const toggles = [
      extractSRTRef.current?.ariaPressed === "true",
      processSRTRef.current?.ariaPressed === "true",
      processTTSRef.current?.ariaPressed === "true",
      processAudioRef.current?.ariaPressed === "true",
    ];
    const files = textareaRef.current?.value?.split("\n") ?? [];

    for (let i = 0; i < files.length; i++) {
      setBatchProgress([0, 0, 0, 0]);
      await new Promise((res) => setTimeout(res, 1000));
      let filename = files[i];

      // Process extract srt
      setProgressText(`[RUN: ${i}] Extracting SRT...`);
      if (toggles[0]) {
        // TODO
      } else {
        setBatchProgress((progress) => {
          const p = [...progress];
          p[0] = 100;
          return p;
        });
      }

      // Process process srt
      setProgressText(`[RUN: ${i}] Processing SRT...`);
      if (toggles[1]) {
        await processSRT(filename);
        filename = "/home/juki/github/cuddly-journey/scripts/output/subbed.srt";
      } else {
        setBatchProgress((progress) => {
          const p = [...progress];
          p[1] = 100;
          return p;
        });
      }

      // Process process tts
      setProgressText(`[RUN: ${i}] Processing TTS...`);
      if (toggles[2]) {
        await processTTS(filename);
      } else {
        setBatchProgress((progress) => {
          const p = [...progress];
          p[2] = 100;
          return p;
        });
      }

      // Process process audio
      setProgressText(`[RUN: ${i}] Processing audio...`);
      if (toggles[3]) {
        await processAudio();
      } else {
        setBatchProgress((progress) => {
          const p = [...progress];
          p[3] = 100;
          return p;
        });
      }

      setProgressText(`[RUN: ${i}] Batch save...`);
      const res = await fetch("http://localhost:3000/api/batch-edit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          index: i,
        }),
      });
      const ok = await res.json();
      if (ok) {
        const num = String(i).padStart(3, "0");
        setFiles((files) => [
          ...files,
          `./batch/${num}-filtered.srt`,
          `./batch/${num}-subbed.srt`,
          `./batch/${num}-output.mp3`,
        ]);
      }
    }

    setProgressText("");
    setDisabled(false);
  }, [processAudio, processSRT, processTTS]);

  return (
    <>
      <div className="mb-6">
        <h1 className="text-4xl font-semibold mb-1">Batch edit</h1>
        <p className="text-sm text-muted-foreground">
          Batch run and process the multiple scripts on multiple SRT files here.
        </p>
      </div>
      <Card>
        <CardContent className="pt-6 flex flex-col gap-4">
          <Card className="w-full bg-black/45">
            <CardHeader>
              <CardTitle>Configuration</CardTitle>
              <CardDescription>The configuration to which scripts is to be used.</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex gap-4 w-full">
                <Toggle variant="outline" size="lg" disabled ref={extractSRTRef}>
                  Extract SRT
                </Toggle>
                <Toggle variant="outline" size="lg" ref={processSRTRef}>
                  Process SRT
                </Toggle>
                <Toggle variant="outline" size="lg" ref={processTTSRef}>
                  Process TTS
                </Toggle>
                <Toggle variant="outline" size="lg" ref={processAudioRef}>
                  Process audio
                </Toggle>
              </div>
            </CardContent>
          </Card>

          <Card className="w-full bg-black/45">
            <CardContent className="pt-6 flex flex-col gap-4">
              <div>
                <p className="text-base font-bold">Input files</p>
                <p className="text-sm text-muted-foreground">
                  The absolute system path to the files separated by newlines to be processed in batch.
                </p>
              </div>
              <div className="space-y-1">
                <Textarea placeholder={"/tmp/input1.srt\n/tmp/input2.srt"} ref={textareaRef} />
              </div>
            </CardContent>
          </Card>

          <Button variant="outline" onClick={processBatch} disabled={disabled}>
            {disabled ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <></>}
            Process batch
          </Button>

          <Divider />

          <Card className="w-full">
            <CardContent className="pt-6 flex flex-col justify-center items-center gap-4">
              <div className="space-y-1 w-full">
                <Progress value={(batchProgress.reduce((r, a) => r + a, 0) / 400) * 100} />
              </div>
              <div className="py-1 text-center text-sm text-muted-foreground">{progressText}</div>
              <div className="space-y-1 w-full">
                {files.map((filename) => (
                  <File base="../scripts/output/batch/" filename={filename} key={filename} />
                ))}
              </div>
            </CardContent>
          </Card>
        </CardContent>
      </Card>
    </>
  );
}
