import { CONFIG } from "@/lib/consts";

type Props = {
  progressCallback: React.Dispatch<React.SetStateAction<number>>;
  type: "extract-srt" | "process-srt" | "process-tts" | "process-audio";
};
type BatchProps = {
  progressCallback: (index: number, progress: number) => void;
  index: number;
  type: "extract-srt" | "process-srt" | "process-tts" | "process-audio";
};

const poll = ({ progressCallback, type }: Props) => {
  const interval = setInterval(async () => {
    const res = await fetch(`${CONFIG.SERVER_URL}/progress?type=${type}`);
    const progress = Number(await res.text());
    progressCallback(progress);
    if (progress >= 100) {
      clearInterval(interval);
    }
  }, 2000);
};

const pollBatch = ({ progressCallback, index = 0, type }: BatchProps) => {
  const interval = setInterval(async () => {
    const res = await fetch(`${CONFIG.SERVER_URL}/progress?type=${type}`);
    const progress = Number(await res.text());
    progressCallback(index, progress);
    if (progress >= 100) {
      clearInterval(interval);
    }
  }, 3000);
};

export { poll, pollBatch };
