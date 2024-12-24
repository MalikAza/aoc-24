import { getInputFileFromScriptFile } from "@utils/input"
import { memoize } from "@utils/memoize"
import { solutionLog } from "@utils/solutionLog"
import { Part } from "@utils/types"

class Solution {
  private patterns: string[]
  private designs: string[]

  constructor(data: string) {
    const [patterns, designs] = data.split('\n\n')
    this.patterns = patterns.split(', ')
    this.designs = designs.split('\n')
  }

  howManyPatternsCanCraftDesign = memoize((design: string): number => {
    if (design.length == 0) {
      return 1
    }

    let solutions = 0
    for (const pattern of this.patterns) {
      if (design.startsWith(pattern)) {
        solutions += this.howManyPatternsCanCraftDesign(design.slice(pattern.length))
      }
    }

    return solutions
  })

  solve(part: Part) {
    switch (part) {
      case 1:
        return this.designs.reduce((acc, design) => acc + (this.howManyPatternsCanCraftDesign(design) > 0 ? 1 : 0), 0)
      case 2:
        return this.designs.reduce((acc, design) => acc + this.howManyPatternsCanCraftDesign(design), 0)
    }
  }
}

function run() {
  const file = getInputFileFromScriptFile(__filename)
  const solution = new Solution(file)

  solutionLog(1, solution.solve(1))
  solutionLog(2, solution.solve(2))
}

if (require.main == module) {
  run()
}