import { create } from "zustand";

const initSRT = [
  {
    id: 1,
    parsed: [
      "Machiko!",
      "Machiko!",
      "Machiko!",
      "Machiko!",
      "Machiko!",
      "Machiko!",
      "Machiko!",
    ],
    timestamp: "00:00:16,780 --> 00:00:17,330",
    text: "Machiko!",
  },
  {
    id: 2,
    parsed: [
      "Anh! Đây là đâu vậy?",
      "Anh! Đây là đâu vậy?",
      "Anh! Đây là đâu vậy?",
      "Anh! Đây là đâu vậy?",
      "Anh! Đây là đâu vậy?",
      "Anh! Đây là đâu vậy?",
      "Anh! Đây là đâu vậy?",
    ],
    timestamp: "00:00:17,330 --> 00:00:18,370",
    text: "Anh! Đây là đâu vậy?",
  },
  {
    id: 3,
    parsed: [
      "Anh! Đây là đầu vậy?",
      "Anh! Đây là đầu vậy?",
      "Anh! Đây là đầu vậy?",
      "Anh! Đây là đầu vậy?",
      "Anh! Đây là đầu vậy?",
      "Anh! Đây là đầu vậy?",
      "Anh! Đây là đầu vậy?",
    ],
    timestamp: "00:00:18,370 --> 00:00:19,790",
    text: "Anh! Đây là đầu vậy?",
  },
  {
    id: 4,
    parsed: [
      "Anh! Đây là đâu vậy?",
      "Không biết nữa",
      "Không biết nữa",
      "Không biết nữa",
      "Không biết nữa",
      "Không biết nữa",
      "Không biết nữa",
    ],
    timestamp: "00:00:19,790 --> 00:00:20,830",
    text: "Không biết nữa",
  },
  {
    id: 5,
    parsed: [
      "Anh chẳng nhớ gì cả",
      "Anh chẳng nhớ gì cả",
      "Anh chẳng nhớ gì cả",
      "Anh chẳng nhớ gì cả",
      "Anh chẳng nhớ gì cả",
      "Anh chẳng nhớ gì cả",
      "Anh chẳng nhớ gì cả",
    ],
    timestamp: "00:00:20,830 --> 00:00:22,370",
    text: "Anh chẳng nhớ gì cả",
  },
];

export type SRTType = {
  id: number;
  parsed: string[];
  timestamp: string;
  text: string;
};
interface SRTState {
  srt: SRTType[];
  setSRT: (srt: SRTType[]) => void;
  addSRT: (srt: SRTType) => void;
  clearSRT: () => void;
}

export const useParsedSRTStore = create<SRTState>((set) => ({
  srt: initSRT as SRTType[],
  setSRT: (srt: SRTType[]) => set({ srt }),
  addSRT: (srt: SRTType) =>
    set((state: { srt: SRTType[] }) => ({
      srt: [...state.srt, srt],
    })),
  clearSRT: () => set({ srt: [] }),
}));
