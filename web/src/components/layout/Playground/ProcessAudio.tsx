import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useCallback, useState } from "react";
import { Progress } from "@/components/ui/progress";
import { Loader2 } from "lucide-react";

export default function ProcessAudio() {
  const [config, setConfig] = useState("standalone");
  const [progress, setProgress] = useState(0);
  const [disabled, setDisabled] = useState(false);
  const [files, setFiles] = useState<string[]>([]);

  const processAudio = useCallback(async () => {
    // Reset status
    setProgress(0);
    setDisabled(true);
    setFiles([]);

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
    const files = await res.json();
    setTimeout(() => {
      setFiles(files);
      setDisabled(false);
    }, 2000);
  }, [config]);

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
