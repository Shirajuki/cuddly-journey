import { CONFIG } from "@/lib/consts";

type Props = {
  input?: string;
  options: {
    langdiff: boolean;
    merge: boolean;
    crosstalk: boolean;
  };
};

const processSrt = async ({ input, options }: Props) => {
  const res = await fetch(`${CONFIG.SERVER_URL}/process-srt`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      input: input,
      options: {
        langdiff: options.langdiff,
        merge: options.merge,
        crosstalk: options.crosstalk,
      },
    }),
  });

  const files = await res.json();
  return { files, status: res.ok };
};

const pollProcessSrt = (progressCallback: React.Dispatch<React.SetStateAction<number>>) => {
  const interval = setInterval(async () => {
    const res = await fetch(`${CONFIG.SERVER_URL}/progress?type=process-srt`);
    const progress = Number(await res.text());
    progressCallback(progress);
    if (progress >= 100) {
      clearInterval(interval);
    }
  }, 2000);
};

export { processSrt, pollProcessSrt };
