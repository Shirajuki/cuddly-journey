import { $ } from "bun";
import { Elysia, t } from 'elysia';
import { cors } from '@elysiajs/cors';
import { readdir } from "node:fs/promises";

const clear = async (extension: string) => {
  await $`rm -f *.${extension} || ls`.cwd("../scripts/output").quiet();
}
const capitalize = (str: string) => str.substring(0,1).toUpperCase() + str.substring(1,str.length).toLowerCase();

const app = new Elysia()
  .use(cors())
	.get('/', () => 'Hello Elysia')
  .group("/api", app => {
    return app
      .get("/progress", async ({ query }) => {
        const { type } = query;
        if (type === "extract-srt") {
          return (await Bun.file("../scripts/output/progress-extract-srt.txt").text()).trim();
        }
        if (type === "process-srt") {
          return (await Bun.file("../scripts/output/progress-process-srt.txt").text()).trim();
        }
        if (type === "process-tts") {
          return (await Bun.file("../scripts/output/progress-process-tts.txt").text()).trim();
        }
        if (type === "process-audio") {
          return (await Bun.file("../scripts/output/progress-process-audio.txt").text()).trim();
        }
        return 100;
      }, {
        query: t.Object({
          type: t.String()
        })
      })
      .post("/extract-srt", async ({ body }) => {
        return body;
      })
      .post("/process-srt", async ({ body }) => {
        const {input, options} = body;
        await clear("srt");

        // Only process if file exist
        if (!await Bun.file(input.trim()).exists()) {
          await $`echo 100 > progress-process-srt.txt`.cwd("../scripts/output").quiet();
          return [];
        }
        await $`python3 process_srt.py ${input.trim()} ${capitalize(String(options.langdiff))} ${capitalize(String(options.merge))} ${capitalize(String(options.crosstalk))}`.cwd("../scripts/tts_srt_parsing").quiet();

        const files = await readdir("../scripts/output");
        return files.filter(f => f === "subbed.srt" || f === "filtered.srt");
      }, {
        body: t.Object({
          input: t.String(),
          options: t.Object({
            langdiff: t.Boolean(), 
            merge: t.Boolean(), 
            crosstalk: t.Boolean(), 
          }),
        })
      })
      .post("/process-tts", async ({ body }) => {
        const {engine, voice, input} = body;

        await clear("mp3");
        await clear("wav");

        // await $`python3 tts-${engine}.py ${input ${voice}`.cwd("../scripts/tts_srt_parsing").text();
        await $`python3 tts-${engine}.py ${input}`.cwd("../scripts/tts_srt_parsing").quiet();

        const files = await readdir("../scripts/output");
        const filteredFiles = files.filter(f => (f.includes(".mp3") || f.includes(".wav")) && f.split(".")?.at(0) == String(Number(f.split(".")?.at(0))));
        return filteredFiles.sort((a, b) => Number(a.split(".").at(0)) - Number(b.split(".").at(0)));
      }, {
        body: t.Object({
          engine: t.String(),
          voice: t.String(),
          input: t.String()
        })
      })
      .post("/process-audio", async ({ body }) => {
        const { config } = body;
        if (config.trim() === "standalone") {
          await $`python3 standalone.py`.cwd("../scripts/process_video").quiet();
        }
        const files = await readdir("../scripts/output");
        return files.filter(f => f === "output.mp3");
      }, {
        body: t.Object({
          config: t.String(),
        })
      })
  })
	.listen(3000)

console.log(`🦊 Elysia is running at on port ${app.server?.port}...`)
