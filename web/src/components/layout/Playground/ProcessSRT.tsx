import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
// import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
// import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { useRef } from "react";
import { Progress } from "@/components/ui/progress";
import { Loader2 } from "lucide-react";
import Divider from "@/components/custom/Divider";
import File from "@/components/custom/File";
import { apiProcessSRT } from "@/api/processSRT";
import { poll } from "@/api/poll";
import useProcessing from "@/lib/useProcessing";

export default function ProcessSRT() {
  const { startProcess, finishProcess, progress, setProgress, disabled, files } = useProcessing();
  const inputRef = useRef<HTMLInputElement>(null);
  const langdiffRef = useRef<HTMLButtonElement>(null);
  const mergeRef = useRef<HTMLButtonElement>(null);
  const crosstalkRef = useRef<HTMLButtonElement>(null);
  const upperRef = useRef<HTMLButtonElement>(null);

  const processSRT = async () => {
    startProcess();
    poll({ progressCallback: setProgress, type: "process-srt" });
    const { files } = await apiProcessSRT({
      input: inputRef.current?.value,
      options: {
        langdiff: langdiffRef.current?.dataset?.state === "checked",
        merge: mergeRef.current?.dataset?.state === "checked",
        crosstalk: crosstalkRef.current?.dataset?.state === "checked",
        upper: upperRef.current?.dataset?.state === "checked",
      },
    });
    setTimeout(() => {
      finishProcess(files);
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
            <div className="space-y-1">
              <div className="items-top flex space-x-2">
                <Checkbox id="upper" ref={upperRef} />
                <div className="grid gap-1.5 leading-none">
                  <label
                    htmlFor="upper"
                    className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  >
                    Parse full uppercase text as normal subtitle text, instead of filtering it out
                  </label>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Button variant="outline" onClick={processSRT} disabled={disabled}>
          {disabled ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <></>}
          Process SRT
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
