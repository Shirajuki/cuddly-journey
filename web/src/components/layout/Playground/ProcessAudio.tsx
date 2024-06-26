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
import { poll } from "@/api/poll";
import { apiProcessAudio } from "@/api/processAudio";

export default function ProcessAudio() {
  const { startProcess, finishProcess, progress, setProgress, disabled, files } = useProcessing();
  const [config, setConfig] = useState("standalone");

  const processAudio = useCallback(async () => {
    startProcess();
    poll({ progressCallback: setProgress, type: "process-audio" });
    const { files, ok } = await apiProcessAudio({ config });
    if (!ok) files.length = 0;
    setTimeout(() => {
      finishProcess(files);
    }, 2000);
  }, [config, finishProcess, startProcess, setProgress]);

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
