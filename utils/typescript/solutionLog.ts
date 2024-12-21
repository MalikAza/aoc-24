import { Part } from "@utils/types"

export function solutionLog(part: Part, solution: number) {
  console.log(`Part ${part === 1 ? "one" : "two"} solution is: ${solution}`)
}