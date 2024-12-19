import path from "node:path"
import fs from "node:fs"

export function getInputFileFromScriptFile(scriptFile: string): string {
  const inputPath = path.join(path.dirname(scriptFile), "../input.txt")

  return fs.readFileSync(inputPath, "utf-8")
}