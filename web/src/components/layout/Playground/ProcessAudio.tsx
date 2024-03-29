import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

export default function ProcessAudio() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Process Audio</CardTitle>
        <CardDescription>
          Includes scripts that processes given audio clips and generates finished audio/project file from it
        </CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <Card className="w-full bg-black/45">
          <CardContent className="pt-6 h-full flex flex-col gap-4">
            <div>
              <p className="text-base font-bold">Input folder and output file</p>
              <p className="text-sm text-muted-foreground">
                The absolute system path to the folder containing the audio files to be combined and the output file.
              </p>
            </div>
            <div className="space-y-1">
              <Label htmlFor="video-input">Audio folder (.mp3/.wav)</Label>
              <Input id="video-input" defaultValue="/tmp/input_folder" />
            </div>
            <div className="space-y-1">
              <Label htmlFor="srt-output">Audio output (.mp3)</Label>
              <Input id="srt-output" defaultValue="/tmp/output.mp3" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-black/45">
          <CardContent className="pt-6 h-full flex flex-col gap-4">
            <div className="space-y-1 w-full">
              <Label htmlFor="based-srt-input">Process configuration</Label>
              <Select>
                <SelectTrigger>
                  <SelectValue placeholder="Standalone" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="standalone">Standalone</SelectItem>
                  <SelectItem value="capcut">Capcut</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        <Button variant="outline">Process audio</Button>
        <br />
        <hr />
        <br />

        <Card className="w-[calc(100%-1rem)]">
          <CardContent className="pt-6 flex justify-center items-center">Output file to be downloaded...</CardContent>
        </Card>
      </CardContent>
    </Card>
  );
}
