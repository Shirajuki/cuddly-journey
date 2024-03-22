import { createLazyFileRoute } from "@tanstack/react-router";

export const Route = createLazyFileRoute("/editor")({
  component: Editor,
});

function Editor() {
  return (
    <>
      <h1>Editor</h1>
    </>
  );
}
