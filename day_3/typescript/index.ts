import { getInputFileFromScriptFile } from "@utils/input"
import { solutionLog } from "@utils/solutionLog"
import { Part } from "@utils/types"

type MulArray = [number, number]

class Memory {
  memory: string

  constructor(memory: string) {
    this.memory = memory
  }

  private extractMuls(): MulArray[] {
    const pattern = /mul\((\d{1,3}),\s*(\d{1,3})\)/g
    const matches = Array.from(this.memory.matchAll(pattern))

    return matches.map(match => [parseInt(match[1]), parseInt(match[2])])
  }

  private extractMulsWithInstructions(): MulArray[] {
    const pattern = /(don't\(\)|do\(\))|mul\((\d{1,3}),\s*(\d{1,3})\)/g
    const matches = Array.from(this.memory.matchAll(pattern))

    let correctMatches: MulArray[] = []
    let doInstruction = true
    
    matches.forEach(match => {
      if (match[1] === "do()" || match[1] === "don't()") {
        doInstruction = match[1] === "do()"
      } else if (doInstruction) {
        correctMatches.push([parseInt(match[2]), parseInt(match[3])])
      }
    })

    return correctMatches
  }

  public solve(part: Part): number {
    const muls = part === 1 ?
      this.extractMuls() :
      this.extractMulsWithInstructions()

    return muls.reduce((acc, [a, b]) => acc + (a * b), 0)
  }
}

function run() {
  const file = getInputFileFromScriptFile(__filename)
  const memory = new Memory(file)

  solutionLog(1, memory.solve(1))
  solutionLog(2, memory.solve(2))
}

if (require.main === module) {
  run()
}