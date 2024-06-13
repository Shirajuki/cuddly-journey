import { CONFIG } from "@/lib/consts";

type Props = {
  input?: string;
  options: {
    langdiff: boolean;
    merge: boolean;
    crosstalk: boolean;
  };
};

const apiProcessSRT = async ({ input, options }: Props) => {
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

  const files: string[] = await res.json();
  return { files, ok: res.ok };
};

export { apiProcessSRT };
