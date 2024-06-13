import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useCallback, useState } from "react";
import { Progress } from "@/components/ui/progress";
import { Loader2 } from "lucide-react";
import Divider from "@/components/custom/Divider";
import File from "@/components/custom/File";
import useProcessing from "@/lib/useProcessing";

export default function ProcessAudio() {
  const { reset, finish, progress, setProgress, disabled, files } = useProcessing();
  const [config, setConfig] = useState("standalone");

  const processAudio = useCallback(async () => {
    // Reset status
    reset();
    // Start fetching progress intervally
    const interval = setInterval(async () => {
      const res = await fetch("http://localhost:3000/api/progress?type=process-audio");
      const progress = Number(await res.text());
      setProgress(progress);
      if (progress >= 100) {
        clearInterval(interval);
      }
    }, 2000);

    // Request process TTS
    const res = await fetch("http://localhost:3000/api/process-audio", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        config: config,
      }),
    });

    // Retrieve response containing file list, making sure to update right after progress
    let files = [];
    if (res.ok) {
      files = await res.json();
    }
    setTimeout(() => {
      finish(files);
    }, 2000);
  }, [config, finish, reset, setProgress]);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Process Audio</CardTitle>
        <CardDescription>
          Includes scripts that processes given audio clips and generates finished audio/project file from it
        </CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <Card className="bg-black/45">
          <CardContent className="pt-6 h-full flex flex-col gap-4">
            <div className="space-y-1 w-full">
              <Label htmlFor="based-srt-input">Process configuration</Label>
              <Select onValueChange={(value: string) => setConfig(value)} value={config}>
                <SelectTrigger>
                  <SelectValue placeholder="Standalone" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="standalone">Standalone</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        <Button variant="outline" onClick={processAudio} disabled={disabled}>
          {disabled ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <></>}
          Process audio
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
