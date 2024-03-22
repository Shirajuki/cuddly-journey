import PlaygroundPage from "@/components/layout/Playground/PlaygroundPage";
import { createLazyFileRoute } from "@tanstack/react-router";

export const Route = createLazyFileRoute("/playground")({
  component: Playground,
});

function Playground() {
  return <PlaygroundPage />;
}
