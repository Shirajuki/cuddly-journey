import { useCallback, useState } from "react";

const useProcessing = () => {
  const [progress, setProgress] = useState(0);
  const [disabled, setDisabled] = useState(false);
  const [files, setFiles] = useState<string[]>([]);

  const reset = useCallback(() => {
    setProgress(0);
    setDisabled(true);
    setFiles([]);
  }, []);

  const finish = useCallback((files: string[]) => {
    setProgress(100);
    setDisabled(false);
    setFiles(files);
  }, []);

  return { reset, finish, progress, setProgress, disabled, files };
};
export default useProcessing;
