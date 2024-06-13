import { pollBatch } from "@/api/poll";
import { apiProcessAudio } from "@/api/processAudio";
import { apiProcessSRT } from "@/api/processSRT";
import { apiProcessTTS } from "@/api/processTTS";
import Divider from "@/components/custom/Divider";
import File from "@/components/custom/File";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Textarea } from "@/components/ui/textarea";
import { Toggle } from "@/components/ui/toggle";
import useBatchProcessing from "@/lib/useBatchProcessing";
import { Loader2 } from "lucide-react";
import { useCallback, useRef } from "react";

const sleep = async (duration: number) => await new Promise((res) => setTimeout(res, duration));

export default function BatchEditPage() {
  const {
    startProcess,
    finishProcess,
    batchProgress,
    updateProgress,
    resetProgress,
    progressText,
    setProgressText,
    disabled,
    files,
    setFiles,
  } = useBatchProcessing();

  const extractSRTRef = useRef<HTMLButtonElement>(null);
  const processSRTRef = useRef<HTMLButtonElement>(null);
  const processTTSRef = useRef<HTMLButtonElement>(null);
  const processAudioRef = useRef<HTMLButtonElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const processSRT = useCallback(
    async (filename: string) => {
      pollBatch({ progressCallback: updateProgress, index: 1, type: "process-srt" });
      await apiProcessSRT({
        input: filename,
        options: {
          langdiff: false,
          merge: false,
          crosstalk: false,
        },
      });
      await sleep(1000);
    },
    [updateProgress],
  );

  const processTTS = useCallback(
    async (filename: string) => {
      pollBatch({ progressCallback: updateProgress, index: 2, type: "process-tts" });
      await apiProcessTTS({ engine: "edge", voice: "vi-VN-HoaiMyNeural", input: filename });
      await sleep(1000);
    },
    [updateProgress],
  );

  const processAudio = useCallback(async () => {
    pollBatch({ progressCallback: updateProgress, index: 3, type: "process-audio" });
    await apiProcessAudio({ config: "standalone" });
    await sleep(1000);
  }, [updateProgress]);

  const processBatch = useCallback(async () => {
    startProcess();
    const toggles = [
      extractSRTRef.current?.ariaPressed === "true",
      processSRTRef.current?.ariaPressed === "true",
      processTTSRef.current?.ariaPressed === "true",
      processAudioRef.current?.ariaPressed === "true",
    ];
    const files = textareaRef.current?.value?.split("\n") ?? [];

    for (let i = 0; i < files.length; i++) {
      resetProgress();
      await sleep(1000);
      let filename = files[i];

      setProgressText(`[RUN: ${i}] Extracting SRT...`);
      if (toggles[0]) {
        // TODO
      } else {
        updateProgress(0, 100);
      }

      setProgressText(`[RUN: ${i}] Processing SRT...`);
      if (toggles[1]) {
        await processSRT(filename);
        filename = "/home/juki/github/cuddly-journey/scripts/output/subbed.srt";
      } else {
        updateProgress(1, 100);
      }

      setProgressText(`[RUN: ${i}] Processing TTS...`);
      if (toggles[2]) await processTTS(filename);
      else updateProgress(2, 100);

      setProgressText(`[RUN: ${i}] Processing audio...`);
      if (toggles[3]) await processAudio();
      else updateProgress(3, 100);

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
      const nfiles: string[] = await res.json();
      if (res.ok && nfiles.length > 0) {
        setFiles((ofiles) => [...ofiles, ...nfiles]);
      }
    }

    finishProcess();
  }, [
    finishProcess,
    processAudio,
    processSRT,
    processTTS,
    resetProgress,
    setFiles,
    setProgressText,
    startProcess,
    updateProgress,
  ]);

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
                  <File filename={filename} key={filename} />
                ))}
              </div>
            </CardContent>
          </Card>
        </CardContent>
      </Card>
    </>
  );
}
