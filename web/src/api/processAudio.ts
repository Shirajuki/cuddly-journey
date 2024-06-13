import { CONFIG } from "@/lib/consts";

type Props = {
  config: string;
};

const apiProcessAudio = async ({ config }: Props) => {
  const res = await fetch(`${CONFIG.SERVER_URL}/process-audio`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      config: config,
    }),
  });

  const files: string[] = await res.json();
  return { files, ok: res.ok };
};

export { apiProcessAudio };
