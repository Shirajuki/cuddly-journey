import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableFooter, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { ResizableHandle, ResizablePanel, ResizablePanelGroup } from "@/components/ui/resizable";
import { Textarea } from "@/components/ui/textarea";

const data = [
  {
    invoice: "INV001",
    paymentStatus: "Paid",
    totalAmount: "$250.00",
    paymentMethod: "Credit Card",
  },
  {
    invoice: "INV002",
    paymentStatus: "Pending",
    totalAmount: "$150.00",
    paymentMethod: "PayPal",
  },
  {
    invoice: "INV003",
    paymentStatus: "Unpaid",
    totalAmount: "$350.00",
    paymentMethod: "Bank Transfer",
  },
  {
    invoice: "INV004",
    paymentStatus: "Paid",
    totalAmount: "$450.00",
    paymentMethod: "Credit Card",
  },
  {
    invoice: "INV005",
    paymentStatus: "Paid",
    totalAmount: "$550.00",
    paymentMethod: "PayPal",
  },
  {
    invoice: "INV006",
    paymentStatus: "Pending",
    totalAmount: "$200.00",
    paymentMethod: "Bank Transfer",
  },
  {
    invoice: "INV007",
    paymentStatus: "Unpaid",
    totalAmount: "$300.00",
    paymentMethod: "Credit Card",
  },
];

export default function PlaygroundPage() {
  return (
    <>
      <div className="mb-6">
        <h1 className="text-4xl font-semibold mb-1">Playground</h1>
        <p className="text-sm text-muted-foreground">
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Blanditiis sequi dolor et animi, ab porro tenetur
          accusamus rerum architecto quis!
        </p>
      </div>
      <Tabs defaultValue="extract-srt" className="">
        <TabsList className="">
          <TabsTrigger value="extract-srt">Extract SRT</TabsTrigger>
          <TabsTrigger value="process-srt">Process SRT</TabsTrigger>
          <TabsTrigger value="tts">TTS</TabsTrigger>
          <TabsTrigger value="process-audio">Process audio</TabsTrigger>
          <TabsTrigger value="ai-translate">AI Translate</TabsTrigger>
        </TabsList>

        <TabsContent value="extract-srt">
          <Card>
            <CardHeader>
              <CardTitle>Extract SRT</CardTitle>
              <CardDescription>Card Description</CardDescription>
            </CardHeader>
            <CardContent>
              <ResizablePanelGroup direction="horizontal">
                <ResizablePanel defaultSize={75}>
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead className="w-[100px]">Invoice</TableHead>
                        <TableHead>Status</TableHead>
                        <TableHead>Method</TableHead>
                        <TableHead className="text-right">Amount</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {data.map((invoice) => (
                        <TableRow key={invoice.invoice}>
                          <TableCell className="font-medium">{invoice.invoice}</TableCell>
                          <TableCell>{invoice.paymentStatus}</TableCell>
                          <TableCell>{invoice.paymentMethod}</TableCell>
                          <TableCell className="text-right">{invoice.totalAmount}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                    <TableFooter>
                      <TableRow>
                        <TableCell colSpan={3}>Total</TableCell>
                        <TableCell className="text-right">$2,500.00</TableCell>
                      </TableRow>
                    </TableFooter>
                  </Table>
                </ResizablePanel>
                <ResizableHandle withHandle />
                <ResizablePanel defaultSize={25}>
                  <Textarea className="w-full h-full resize-none" readOnly value={"yoyo\nasd"} />
                </ResizablePanel>
              </ResizablePanelGroup>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="process-srt">
          <Card>
            <CardHeader>
              <CardTitle>Process SRT</CardTitle>
              <CardDescription>Card Description</CardDescription>
            </CardHeader>
            <CardContent>
              <p>Card Content</p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="tts">
          <Card>
            <CardHeader>
              <CardTitle>TTS</CardTitle>
              <CardDescription>Card Description</CardDescription>
            </CardHeader>
            <CardContent>
              <p>Card Content</p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="process-audio">
          <Card>
            <CardHeader>
              <CardTitle>Process audio</CardTitle>
              <CardDescription>Card Description</CardDescription>
            </CardHeader>
            <CardContent>
              <p>Card Content</p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="ai-translate">
          <Card>
            <CardHeader>
              <CardTitle>AI translate</CardTitle>
              <CardDescription>Card Description</CardDescription>
            </CardHeader>
            <CardContent>
              <p>Card Content</p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </>
  );
}
