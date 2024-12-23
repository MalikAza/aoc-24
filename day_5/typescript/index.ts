import { getInputFileFromScriptFile } from "@utils/input"
import { solutionLog } from "@utils/solutionLog"
import { Part } from "@utils/types"

class RulesStore {
  private rules: { [key: string]: string[] }

  constructor(data: string) {
    const rulesData = data.split('\n')
    this.rules = {}

    for (const rules of rulesData) {
      const [key, value] = rules.split('|')

      if (!(key in this.rules)) {
        this.rules[key] = []
      }

      this.rules[key].push(value)
    }
  }

  getAll() {
    return this.rules
  }
}

class Printing {
  private order: string[]

  constructor(data: string) {
    this.order = data.split(',')
  }

  getOrder() {
    return this.order
  }
}

class PrintingsStore {
  private printings: Printing[]

  constructor(data: string) {
    this.printings = data.split('\n').map(printing => new Printing(printing))
  }

  getAll() {
    return this.printings.map(printing => printing.getOrder())
  }
}

class Solution {
  private rules: { [key: string]: string[] }
  private printings: Array<Array<string>>
  private correctPrintings: Array<Array<string>>
  private incorrectPrintings: Array<Array<string>>

  constructor(rules: string, printings: string) {
    this.rules = new RulesStore(rules).getAll()
    this.printings = new PrintingsStore(printings).getAll()
    this.correctPrintings = []
    this.incorrectPrintings = []
    this.filterPrintings()
  }

  private isValidPrinting(printing: string[]) {
    for (const [index, page] of printing.entries()) {
      if (!(page in this.rules)) {
        continue
      }

      const pageRules = this.rules[page]
      const beforePage = printing.slice(0, index)
      const isIncorrect = beforePage.some(rule => pageRules.includes(rule))

      if (isIncorrect) {
        return false
      }
    }

    return true
  }

  private filterPrintings() {
    for (const printing of this.printings) {
      if (this.isValidPrinting(printing)) {
        this.correctPrintings.push(printing)
      } else {
        this.incorrectPrintings.push(printing)
      }
    }
  }

  private getMiddlePage(printing: string[]) {
    const middleIndex = Math.floor(printing.length / 2)
    return parseInt(printing[middleIndex])
  }

  private fixIncorrectPrintings() {
    for (const printing of this.incorrectPrintings) {
      printing.sort((a, b) => {
        if (a in this.rules && this.rules[a].includes(b)) {
          return -1
        } else if (b in this.rules && this.rules[b].includes(a)) {
          return 1
        }
        return 0
      })
    }
  }

  public solve(part: Part) {
    switch (part) {
      case 1:
        return this.correctPrintings.reduce((acc, printing) => acc + this.getMiddlePage(printing), 0)
      case 2:
        this.fixIncorrectPrintings()
        return this.incorrectPrintings.reduce((acc, printing) => acc + this.getMiddlePage(printing), 0)
    }
  }
}

function run() {
  const file = getInputFileFromScriptFile(__filename)
  const [r, p] = file.split('\n\n')
  const solution = new Solution(r, p)

  solutionLog(1, solution.solve(1))
  solutionLog(2, solution.solve(2))
}

if (require.main === module) {
  run()
}