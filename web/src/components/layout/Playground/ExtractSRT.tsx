import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ResizableHandle, ResizablePanel, ResizablePanelGroup } from "@/components/ui/resizable";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { useParsedSRTStore } from "@/lib/stores";

export default function ExtractSRT() {
  const [checked, setChecked] = useState(false);
  const parsedSRT = useParsedSRTStore((state) => state.srt);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Extract SRT</CardTitle>
        <CardDescription>Includes scripts that extracts hardcoded subtitles from a video file</CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <div className="flex gap-4">
          <Card className="w-full bg-black/45">
            <CardContent className="pt-6 h-full flex flex-col gap-4">
              <div>
                <p className="text-base font-bold">Input and output files</p>
                <p className="text-sm text-muted-foreground">The absolute system path to the files.</p>
              </div>
              <div className="space-y-1">
                <Label htmlFor="video-input">Video input (.mkv)</Label>
                <Input id="video-input" defaultValue="/tmp/movie.mkv" />
              </div>
              <div className="space-y-1">
                <Label htmlFor="srt-output">SRT output (.srt)</Label>
                <Input id="srt-output" defaultValue="/tmp/output.srt" />
              </div>
            </CardContent>
          </Card>
          <Card className="bg-black/45">
            <CardContent className="pt-6 h-full flex flex-col gap-4">
              <div className="flex gap-4">
                <div className="w-full">
                  <p className="text-base font-bold">Base extraction on an SRT file</p>
                  <p className="text-sm text-muted-foreground">
                    Extracts SRT from a video by parsing the same timestamp of an another SRT.
                  </p>
                </div>
                <Switch checked={checked} onCheckedChange={setChecked} />
              </div>
              <div className="space-y-1">
                <Label htmlFor="based-srt-input">Based SRT input</Label>
                <Input id="based-srt-input" defaultValue="/tmp/english.srt" disabled={!checked} />
              </div>
            </CardContent>
          </Card>
        </div>

        <Card className="bg-black/45">
          <CardContent className="h-full flex flex-col gap-4">
            <Accordion type="single" collapsible>
              <AccordionItem value="item-1">
                <AccordionTrigger>Advanced settings</AccordionTrigger>
                <AccordionContent>Nothing to see here...</AccordionContent>
              </AccordionItem>
            </Accordion>
          </CardContent>
        </Card>

        <Button variant="outline">Extract SRT</Button>
        <br />
        <hr />
        <br />

        <Card className="bg-black/45">
          <CardContent className="h-full flex flex-col gap-4">
            <Accordion type="single" collapsible>
              <AccordionItem value="item-1">
                <AccordionTrigger>Prompt settings</AccordionTrigger>
                <AccordionContent className="h-full flex flex-col gap-4">
                  <div>
                    <p className="text-base font-bold">AI prompt to be ran after finishing extraction</p>
                    <p className="text-sm text-muted-foreground">
                      The variables $VAR1, $VAR2 and $VAR3 will be replaced with the actual data.
                    </p>
                  </div>
                  <div className="flex gap-4">
                    <div className="space-y-1 w-full">
                      <Label htmlFor="based-srt-input">Context prompt</Label>
                      <Textarea className="h-full resize-none" />
                    </div>
                    <div className="space-y-1 w-full">
                      <Label htmlFor="based-srt-input">Cleanup prompt</Label>
                      <Textarea className="h-full resize-none" />
                    </div>
                  </div>
                  <br />
                </AccordionContent>
              </AccordionItem>
            </Accordion>
          </CardContent>
        </Card>

        <ResizablePanelGroup direction="horizontal">
          <ResizablePanel defaultSize={75}>
            <Card className="w-[calc(100%-1rem)]">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-[100px]">ID</TableHead>
                    <TableHead className="min-w-[120px]">Timestamp</TableHead>
                    <TableHead>Text</TableHead>
                    <TableHead>Parsed OCR</TableHead>
                    <TableHead className="min-w-[100px]">AI cleanup</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {parsedSRT.map((srt) => (
                    <TableRow key={`srt-${srt.id}`}>
                      <TableCell className="font-medium">{srt.id}</TableCell>
                      <TableCell>{srt.timestamp}</TableCell>
                      <TableCell>{srt.text}</TableCell>
                      <TableCell>{JSON.stringify(srt.parsed)}</TableCell>
                      <TableCell>{srt.text}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </Card>
          </ResizablePanel>

          <ResizableHandle withHandle />

          <ResizablePanel defaultSize={25}>
            <Textarea
              className="h-full resize-none w-[calc(100%-1rem)] ml-auto"
              readOnly
              value={parsedSRT.map(({ id, timestamp, text }) => `${id}\n${timestamp}\n${text}`).join("\n\n")}
            />
          </ResizablePanel>
        </ResizablePanelGroup>
      </CardContent>
    </Card>
  );
}
