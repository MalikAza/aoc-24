import { getInputFileFromScriptFile } from "@utils/input"
import { memoize } from "@utils/memoize"
import { solutionLog } from "@utils/solutionLog"
import { Part } from "@utils/types"

class Solution {
  private stones: string[]

  constructor(data: string) {
    this.stones = data.split(' ')
  }

  private transformStone = memoize((stone: string): string[] => {
    if (stone === '0') return ['1']
    else if (stone.length % 2 === 0) {
      const midPoint = Math.floor(stone.length / 2)

      const stone1 = `${parseInt(stone.slice(0, midPoint))}`
      const stone2 = `${parseInt(stone.slice(midPoint))}`

      return [stone1, stone2]
    } else return [`${parseInt(stone) * 2024}`]
  })

  private howManyStonesProduceOneStone = memoize((stone: string, numberOfIterations: number): number => {
    if (numberOfIterations === 0) return 1

    return this.transformStone(stone).reduce((acc,  curr) => acc + this.howManyStonesProduceOneStone(curr, numberOfIterations - 1), 0)
  })

  public solve(part: Part) {
    let numberOfIterations: number

    switch (part) {
      case 1:
        numberOfIterations = 25
        break
      case 2:
        numberOfIterations = 75
        break
    }

    return this.stones.reduce((acc, curr) => acc + this.howManyStonesProduceOneStone(curr, numberOfIterations), 0)
  }
}

function run() {
  const file = getInputFileFromScriptFile(__filename)
  const solution = new Solution(file)

  solutionLog(1, solution.solve(1))
  solutionLog(2, solution.solve(2))
}

if (require.main === module) {
  run()
}