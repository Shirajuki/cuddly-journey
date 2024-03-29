import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { TTS_VOICES } from "@/lib/consts";
import { useState } from "react";
import { Switch } from "@/components/ui/switch";

export default function TTS() {
  const [checked, setChecked] = useState(false);

  return (
    <Card>
      <CardHeader>
        <CardTitle>TTS</CardTitle>
        <CardDescription>Includes scripts for audio generation through audio inference and TTS</CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <div className="flex gap-4">
          <Card className="w-full bg-black/45">
            <CardContent className="pt-6 h-full flex flex-col gap-4">
              <div className="flex gap-4">
                <div className="w-full">
                  <p className="text-base font-bold">Use a voice model</p>
                  <p className="text-sm text-muted-foreground">
                    Toggle voice model usage for audio inference, making the finalized audio more realistic.
                  </p>
                </div>
                <Switch checked={checked} onCheckedChange={setChecked} />
              </div>
              <div className="space-y-1">
                <Label htmlFor="voice-model">Voice model (.pth)</Label>
                <Input id="video-input" defaultValue="/tmp/model.pth" disabled={!checked} />
              </div>
            </CardContent>
          </Card>
        </div>
        <Card className="bg-black/45">
          <CardContent className="pt-6 h-full flex flex-col gap-4">
            <div className="space-y-1 w-full">
              <Label htmlFor="based-srt-input">TTS Voices</Label>
              <Select>
                <SelectTrigger>
                  <SelectValue placeholder="vi-VN-HoaiMyNeural ♀" />
                </SelectTrigger>
                <SelectContent>
                  {TTS_VOICES.map((voice) => (
                    <SelectItem value={voice.name}>
                      {voice.name} {voice.gender === "Female" ? "♀" : "♂"}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-1 w-full">
              <Label htmlFor="based-srt-input">Text to Synthesize</Label>
              <Textarea className="h-full resize-none" />
            </div>
          </CardContent>
        </Card>

        <Button variant="outline">Convert TTS</Button>
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
