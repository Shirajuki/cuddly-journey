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
	.get('/', () => 'Hello Elysia (*/ω＼*)')
  .group("/api", app => {
    return app
      .get("/file", async ({ query }) => {
        const { filename, preview } = query;
        if (preview == "1") return await Bun.file(filename).text();
        return Bun.file(filename);
      }, {
        query: t.Object({
          filename: t.String(),
          preview: t.String()
        })
      })
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
        // TODO: run actual script and handle progress bar
        return body;
      })
      .post("/process-srt", async ({ body }) => {
        const {input, options} = body;
        await clear("srt");

        // Only process if file exist
        if (!await Bun.file(input.trim()).exists()) {
          await $`echo 100 > progress-process-srt.txt`.cwd("../scripts/output").quiet();
          return ["ERROR_INPUT_FILE_NOT_FOUND"];
        }
        await $`python3 process_srt.py ${input.trim()} ${capitalize(String(options.langdiff))} ${capitalize(String(options.merge))} ${capitalize(String(options.crosstalk))} ${capitalize(String(options.upper))}`.cwd("../scripts/tts_srt_parsing").quiet();

        const files = await readdir("../scripts/output");
        return files.filter(f => f === "subbed.srt" || f === "filtered.srt");
      }, {
        body: t.Object({
          input: t.String(),
          options: t.Object({
            langdiff: t.Boolean(),
            merge: t.Boolean(),
            crosstalk: t.Boolean(),
            upper: t.Boolean(),
          }),
        })
      })
      .post("/process-tts", async ({ body }) => {
        const {engine, voice, input} = body;
        await clear("mp3");
        await clear("wav");

        // Only process if file exist
        if (!await Bun.file(input.trim()).exists()) {
          await $`echo 100 > progress-process-tts.txt`.cwd("../scripts/output").quiet();
          return ["ERROR_INPUT_FILE_NOT_FOUND"];
        }

        // TODO: parse custom tts voice
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

        // Only process if config is valid
        if (config.trim() === "standalone") {
          try {
            await $`python3 standalone.py`.cwd("../scripts/process_audio").quiet();
          } catch (_e) {
            // Return early if specific files does not exists when processing
            await $`echo 100 > progress-process-audio.txt`.cwd("../scripts/output").quiet();
            return ["ERROR_AUDIO_AND_SRT_FILES_NOT_FOUND"];
          }
        } else {
          await $`echo 100 > progress-process-audio.txt`.cwd("../scripts/output").quiet();
        }
        const files = await readdir("../scripts/output");
        return files.filter(f => f === "output.mp3");
      }, {
        body: t.Object({
          config: t.String(),
        })
      })
      .post("/batch-edit", async ({ body }) => {
        const { index } = body;

        // Check if specific files exist before processing
        if (!await Bun.file("../scripts/output/filtered.srt").exists()) return [];
        const filtered = `batch/${String(index).padStart(3, "0")}-filtered.srt`
        await $`cp filtered.srt ${filtered}`.cwd("../scripts/output").quiet();

        if (!await Bun.file("../scripts/output/subbed.srt").exists()) return [filtered];
        const subbed = `batch/${String(index).padStart(3, "0")}-subbed.srt`
        await $`cp subbed.srt ${subbed}`.cwd("../scripts/output").quiet();

        if (!await Bun.file("../scripts/output/output.mp3").exists()) return [filtered, subbed];
        const output = `batch/${String(index).padStart(3, "0")}-output.mp3`
        await $`cp output.mp3 ${output}`.cwd("../scripts/output").quiet();

        return [filtered, subbed, output];
      }, {
        body: t.Object({
          index: t.Number(),
        })
      })
  })
	.listen(3000)

console.log(`🦊 Elysia is running at on port ${app.server?.port}...`)
