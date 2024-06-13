import { Button } from "../ui/button";

type Props = {
  base?: string;
  filename: string;
};

const File = ({ base = "../scripts/output/", filename }: Props) => {
  return (
    <div className="bg-white/5 rounded-md w-full">
      <a href={`http://localhost:3000/api/file?filename=${base}${filename}`} target="_blank" rel="noreferrer">
        <Button variant="link">
          {base}
          {filename}
        </Button>
      </a>
    </div>
  );
};
export default File;
