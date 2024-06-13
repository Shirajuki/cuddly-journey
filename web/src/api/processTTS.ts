import { CONFIG } from "@/lib/consts";

type Props = {
  engine: string;
  voice: string;
  input?: string;
};

const apiProcessTTS = async ({ engine, voice, input }: Props) => {
  const res = await fetch(`${CONFIG.SERVER_URL}/process-tts`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      engine: engine,
      voice: voice,
      input: input,
    }),
  });

  const files: string[] = await res.json();
  return { files, ok: res.ok };
};

export { apiProcessTTS };
