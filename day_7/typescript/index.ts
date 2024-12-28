import { getInputFileFromScriptFile } from "@utils/input"
import { product } from "@utils/iterations"
import { solutionLog } from "@utils/solutionLog"
import { Part } from "@utils/types"

class Solution {
  private data: Array<[number, number[]]>

  constructor(data: string) {
    this.data = data.split('\n').map(line => {
      const [value, operatorsString] = line.split(': ')
      const operators = operatorsString.split(' ').map(Number)

      return [parseInt(value), operators]
    })
  }

  private evaluateExpression(numbers: number[], operators: string[]): number {
    let result = numbers[0]

    for (let i = 1; i < numbers.length; i++) {
      switch (operators[i-1]) {
        case '+':
          result += numbers[i]
          break
        case '*':
          result *= numbers[i]
          break
        case '||':
          result = parseInt(`${result}` + `${numbers[i]}`)
          break
      }
    }

    return result
  }

  private isEquationPossible(finalValue: number, numbers: number[], operators: string[]): boolean {
    const ops = product(operators, numbers.length - 1)

    for (const operator of ops) {
      if (this.evaluateExpression(numbers, operator) === finalValue) {
        return true
      }
    }

    return false
  }

  public solve(part: Part) {
    let operators = ['+', '*']
    if (part === 2) operators.push('||')

    return this.data.reduce((acc, [finalValue, numbers]) => acc + (this.isEquationPossible(finalValue, numbers, operators) ? finalValue : 0), 0)
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