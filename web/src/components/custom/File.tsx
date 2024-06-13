import { CONFIG } from "@/lib/consts";
import { Button } from "../ui/button";
import { File as FileIcon, Download } from "lucide-react";

type Props = {
  base?: string;
  filename: string;
};

const File = ({ base = "../scripts/output/", filename }: Props) => {
  const downloadURL = `${CONFIG.SERVER_URL}/file?filename=${base}${filename}&preview=0`;
  const previewURL = `${CONFIG.SERVER_URL}/file?filename=${base}${filename}&preview=1`;

  return (
    <div className="bg-white/5 rounded-md w-full flex justify-between items-center p-2">
      <div className="flex items-center px-2">
        <FileIcon />
        <a href={filename.endsWith(".mp3") ? downloadURL : previewURL} target="_blank" rel="noreferrer">
          <Button variant="link">
            {base}
            {filename}
          </Button>
        </a>
      </div>
      <div className="flex items-center">
        <a href={downloadURL} target="_blank" rel="noreferrer">
          <Button variant="outline" size="icon">
            <Download />
          </Button>
        </a>
      </div>
    </div>
  );
};
export default File;
