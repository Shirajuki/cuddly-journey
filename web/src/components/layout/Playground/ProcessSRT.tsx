import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
// import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
// import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { useRef, useState } from "react";
import { Progress } from "@/components/ui/progress";
import { Loader2 } from "lucide-react";

export default function ProcessSRT() {
  const [progress, setProgress] = useState(0);
  const [disabled, setDisabled] = useState(false);
  const [files, setFiles] = useState<string[]>([]);
  const inputRef = useRef<HTMLInputElement>(null);
  const langdiffRef = useRef<HTMLButtonElement>(null);
  const mergeRef = useRef<HTMLButtonElement>(null);
  const crosstalkRef = useRef<HTMLButtonElement>(null);

  const processSRT = async () => {
    // Reset status
    setProgress(0);
    setDisabled(true);
    setFiles([]);

    // Start fetching progress intervally
    const interval = setInterval(async () => {
      const res = await fetch("http://localhost:3000/api/progress?type=process-srt");
      const progress = Number(await res.text());
      setProgress(progress);
      if (progress >= 100) {
        clearInterval(interval);
      }
    }, 2000);

    // Request process TTS
    const res = await fetch("http://localhost:3000/api/process-srt", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        input: inputRef.current?.value,
        options: {
          langdiff: langdiffRef.current?.dataset?.state === "checked",
          merge: mergeRef.current?.dataset?.state === "checked",
          crosstalk: crosstalkRef.current?.dataset?.state === "checked",
        },
      }),
    });

    // Retrieve response containing file list, making sure to update right after progress
    const files = await res.json();
    setTimeout(() => {
      setFiles(files);
      setDisabled(false);
    }, 2000);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Process SRT</CardTitle>
        <CardDescription>Includes scripts that processes subtitles and cleans it up</CardDescription>
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
        <Card className="w-full bg-black/45">
          <CardContent className="pt-6 h-full flex flex-col gap-4">
            <div>
              <p className="text-base font-bold">Options</p>
            </div>
            <div className="space-y-1">
              <div className="items-top flex space-x-2">
                <Checkbox id="langdiff" ref={langdiffRef} />
                <div className="grid gap-1.5 leading-none">
                  <label
                    htmlFor="langdiff"
                    className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  >
                    Filter out language difference and skip over wrong language subs
                  </label>
                </div>
              </div>
            </div>
            <div className="space-y-1">
              <div className="items-top flex space-x-2">
                <Checkbox id="merge" ref={mergeRef} />
                <div className="grid gap-1.5 leading-none">
                  <label
                    htmlFor="merge"
                    className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  >
                    Merge dialogues if duplicate, artifact resulted from extracting srt
                  </label>
                </div>
              </div>
            </div>
            <div className="space-y-1">
              <div className="items-top flex space-x-2">
                <Checkbox id="crosstalk" ref={crosstalkRef} />
                <div className="grid gap-1.5 leading-none">
                  <label
                    htmlFor="crosstalk"
                    className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  >
                    Parse multiple dialogues on the same timestamp, played at the same time
                  </label>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* <Card className="bg-black/45">
          <CardContent className="pt-6 h-full flex flex-col gap-4">
            <Accordion type="single" collapsible>
              <AccordionItem value="item-1">
                <AccordionTrigger>
                  <div className="text-left">
                    <p className="text-base font-bold">Advanced process settings (WIP)</p>
                    <p className="text-sm text-muted-foreground">
                      Configure characters, words, sentences to be filtered.
                    </p>
                  </div>
                </AccordionTrigger>
                <AccordionContent>
                  <div className="flex flex-col gap-4">
                    <div className="space-y-1 w-full">
                      <Label htmlFor="based-srt-input">Characters to be replaced</Label>
                      <Textarea className="h-full resize-none" />
                    </div>
                    <div className="space-y-1 w-full">
                      <Label htmlFor="based-srt-input">Words to be replaced</Label>
                      <Textarea className="h-full resize-none" />
                    </div>
                    <div className="space-y-1 w-full">
                      <Label htmlFor="based-srt-input">Sentences to be replaced</Label>
                      <Textarea className="h-full resize-none" />
                    </div>
                    <div className="space-y-1 w-full">
                      <Label htmlFor="based-srt-input">Regex to be filtered</Label>
                      <Textarea className="h-full resize-none" />
                    </div>
                  </div>
                </AccordionContent>
              </AccordionItem>
            </Accordion>
          </CardContent>
        </Card> */}

        <Button variant="outline" onClick={processSRT} disabled={disabled}>
          {disabled ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <></>}
          Process SRT
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
