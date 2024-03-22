import { createLazyFileRoute } from "@tanstack/react-router";

export const Route = createLazyFileRoute("/documentation")({
  component: Documentation,
});

function Documentation() {
  return (
    <>
      <h1>Documentation</h1>
    </>
  );
}
