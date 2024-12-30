import { getInputFileFromScriptFile } from "@utils/input"
import { solutionLog } from "@utils/solutionLog"
import { Part } from "@utils/types"

class Button {
  public x: number
  public y: number

  constructor(data: string) {
    const [x, y] = data.split(',')
    this.x = parseInt(x.split('+').pop() as string)
    this.y = parseInt(y.split('+').pop() as string) 
  }
}

class Prize {
  public x: number
  public y: number

  constructor(data: string) {
    const [x, y] = data.split(',')
    this.x = parseInt(x.split('=').pop() as string)
    this.y = parseInt(y.split('=').pop() as string)
  }
}

class Claw {
  private buttonA: Button
  private buttonB: Button
  private prize: Prize
  private best: number | null

  constructor(data: string) {
    const [buttonA, buttonB, prize] = data.split('\n')

    this.buttonA = new Button(buttonA)
    this.buttonB = new Button(buttonB)
    this.prize = new Prize(prize)
    this.best = null
  }

  private getLowestX() {
    return Math.min(this.buttonA.x, this.buttonB.x)
  }

  private getLowestY() {
    return Math.min(this.buttonA.y, this.buttonB.y)
  }

  private getMaxIterations(part: Part) {
    switch(part) {
      case 1:
        return 101
      case 2:
        return Math.max(Math.floor(this.prize.x / this.getLowestX()), Math.floor(this.prize.y / this.getLowestY()))
    }
  }

  private calculateBest(part: Part) {
    const maxIterations = this.getMaxIterations(part)
    for (let a = 0; a < maxIterations; a++) {
      for (let b = 0; b < maxIterations; b++) {
        const x = this.buttonA.x * a + this.buttonB.x * b
        const y = this.buttonA.y * a + this.buttonB.y * b

        if (x === this.prize.x && y === this.prize.y) {
          const cost = 3 * a + b
          this.best = this.best === null ? cost : Math.min(this.best, cost)
        }
      }
    }
  }

  public getBest(part: Part): number {
    if (part === 2) {
      this.prize.x += 10000000000000
      this.prize.y += 10000000000000
    }

    this.calculateBest(part)

    return this.best === null ? 0 : this.best
  }
}

class Solution {
  private claws: Claw[]

  constructor(data: string) {
    this.claws = data.split('\n\n').map(dataClaw => new Claw(dataClaw))
  }

  public solve(part: Part) {
    return this.claws.reduce((sum, claw) => sum + claw.getBest(part), 0)
  }
}

function run() {
  const file = getInputFileFromScriptFile(__filename)
  const solution = new Solution(file)

  solutionLog(1, solution.solve(1))
  // solutionLog(2, solution.solve(2))
}

if (require.main === module) {
  run()
}