import { useCallback, useState } from "react";

const useBatchProcessing = () => {
  const [disabled, setDisabled] = useState(false);
  const [batchProgress, setBatchProgress] = useState([0, 0, 0, 0]);
  const [progressText, setProgressText] = useState("");
  const [files, setFiles] = useState<string[]>([]);

  const startProcess = useCallback(() => {
    setBatchProgress([0, 0, 0, 0]);
    setDisabled(true);
    setFiles([]);
  }, []);

  const finishProcess = useCallback(() => {
    setProgressText("");
    setDisabled(false);
  }, []);

  const updateProgress = useCallback((index: number, progress: number) => {
    setBatchProgress((op) => {
      const np = [...op];
      np[index] = progress;
      return np;
    });
  }, []);

  const resetProgress = useCallback(() => {
    setBatchProgress([0, 0, 0, 0]);
  }, []);

  return {
    startProcess,
    finishProcess,
    batchProgress,
    updateProgress,
    resetProgress,
    progressText,
    setProgressText,
    disabled,
    files,
    setFiles,
  };
};
export default useBatchProcessing;
