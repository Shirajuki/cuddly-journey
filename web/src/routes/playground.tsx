import PlaygroundPage from "@/components/layout/Playground/PlaygroundPage";
import { createFileRoute } from "@tanstack/react-router";

export type PlaygroundTabsOptions = "extract-srt" | "process-srt" | "process-tts" | "process-audio" | "ai-translate";
type PlaygroundTabs = {
  tab: PlaygroundTabsOptions;
};

export const Route = createFileRoute("/playground")({
  validateSearch: (search: Record<string, unknown>): PlaygroundTabs => {
    return {
      tab: (search.tab as PlaygroundTabsOptions) || "extract-srt",
    };
  },
  component: Playground,
});

function Playground() {
  return <PlaygroundPage />;
}
