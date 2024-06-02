import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";

export default function ProcessSRT() {
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
              <Input id="video-input" defaultValue="/tmp/input.srt" />
            </div>
            <div className="space-y-1">
              <Label htmlFor="srt-output">SRT output (.srt)</Label>
              <Input id="srt-output" defaultValue="/tmp/output.srt" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-black/45">
          <CardContent className="pt-6 h-full flex flex-col gap-4">
            <Accordion type="single" collapsible>
              <AccordionItem value="item-1">
                <AccordionTrigger>
                  <div className="text-left">
                    <p className="text-base font-bold">Advanced process settings</p>
                    <p className="text-sm text-muted-foreground">
                      Configure characters, words, sentences to be filtered.
                    </p>
                  </div>
                </AccordionTrigger>
                <AccordionContent>
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
                    <Label htmlFor="based-srt-input">Text to be removed</Label>
                    <Textarea className="h-full resize-none" />
                  </div>
                  <div className="space-y-1 w-full">
                    <Label htmlFor="based-srt-input">Regex to be filtered</Label>
                    <Textarea className="h-full resize-none" />
                  </div>
                </AccordionContent>
              </AccordionItem>
            </Accordion>
          </CardContent>
        </Card>

        <Button variant="outline">Process SRT</Button>
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
