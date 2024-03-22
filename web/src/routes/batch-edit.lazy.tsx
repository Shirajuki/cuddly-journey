import { createLazyFileRoute } from "@tanstack/react-router";

export const Route = createLazyFileRoute("/batch-edit")({
  component: BatchEdit,
});

function BatchEdit() {
  return (
    <>
      <h1>Batch edit</h1>
    </>
  );
}
