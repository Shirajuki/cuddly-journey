import BatchEditPage from "@/components/layout/Editor/BatchEditPage";
import { createLazyFileRoute } from "@tanstack/react-router";

export const Route = createLazyFileRoute("/batch-edit")({
  component: BatchEdit,
});

function BatchEdit() {
  return <BatchEditPage />;
}
