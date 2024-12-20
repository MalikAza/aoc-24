import { getInputFileFromScriptFile } from "@utils/input";
import { solutionLog } from "@utils/solutionLog";

function getLeftAndRight(file: string): Array<Array<number>> {
  const lines = file.split("\n")
  let left: Array<number> = []
  let right: Array<number> = []

  for (const line of lines) {
    const [l, r] = line.split("   ").map(Number)
    left.push(l)
    right.push(r)
  }

  return [left, right]
}

function pairMinLeftWithMinRight(left: Array<number>, right: Array<number>): Array<[number, number]> {
  left.sort((a, b) => a - b)
  right.sort((a, b) => a - b)

  return left.map((_, i) => [left[i], right[i]])
}

function partOneSolution(left: Array<number>, right: Array<number>): number {
  const paired = pairMinLeftWithMinRight([...left], [...right])

  return paired.reduce((acc, pair) => acc + (Math.max(...pair) - Math.min(...pair)), 0)
}

function partTwoSolution(left: Array<number>, right: Array<number>): number {
  return left.reduce((acc, n) => acc + (n * right.filter((x) => x === n).length), 0)
}

function run() {
  const file = getInputFileFromScriptFile(__filename)
  const [left, right] = getLeftAndRight(file)

  solutionLog(1, partOneSolution(left, right))
  solutionLog(2, partTwoSolution(left, right))
}

if (require.main === module) {
  run()
}