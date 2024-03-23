import { Button } from "@/components/ui/button";
import { Link } from "@tanstack/react-router";

export default function Home() {
  return (
    <>
      <div className="h-[40rem] relative w-full flex flex-col items-center justify-center overflow-hidden rounded-md bg-grid-white/10">
        <div className="absolute pointer-events-none inset-0 flex items-center justify-center bg-background [mask-image:radial-gradient(ellipse_at_center,transparent_30%,black,black)]" />
        <div className="-translate-y-12 flex flex-col items-center justify-center">
          <h1 className="md:text-5xl text-3xl lg:text-6xl font-bold text-center text-white relative z-20 max-w-2xl lg:max-w-4xl tracking-tight md:tracking-tighter py-5">
            Hardsub -&gt; Softsub + TTS = 🍿
          </h1>
          <p className="text-sm md:text-md font-mono max-w-xl tracking-wide text-center">
            An open-source all-in-one tool and ecosystem that hosts utility scripts for easier video subbing and
            dubbing.
          </p>
        </div>
        <div className="flex gap-4">
          <Link to="/playground">
            <Button>Playground</Button>
          </Link>
          <Link to="/editor">
            <Button>Editor</Button>
          </Link>
        </div>
      </div>
    </>
  );
}
