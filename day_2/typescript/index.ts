import { getInputFileFromScriptFile } from "@utils/input"
import { combinations, isTwoArraysHaveSameOrderedElements, pairwise } from "@utils/iterations"
import { solutionLog } from "@utils/solutionLog"

export function getReports(file: string): Array<number[]> {
  const lines = file.split('\n')
  const reports = lines.map(line => line.split(' ').map(Number))

  return reports
}

export class Report {
  public report: number[]

  private MAX_DIFFERENCE: number = 3
  private MIN_DIFFERENCE: number = 1

  constructor(report: number[]) {
    this.report = report
  }

  public isContinuous(): boolean {
    const report = [...this.report]
    const sorted = report.sort((a, b) => a - b)

    return isTwoArraysHaveSameOrderedElements(sorted, this.report)
           || isTwoArraysHaveSameOrderedElements(sorted.reverse(), this.report)
  }

  public respectDifferences(): boolean {
    const differences = pairwise(this.report).map(([a, b]) => Math.abs(a - b))

    return differences.every(diff => this.MIN_DIFFERENCE <= diff && diff <= this.MAX_DIFFERENCE)
  }

  public isSafe(): boolean {
    return this.isContinuous() && this.respectDifferences()
  }
}

function run() {
  const file = getInputFileFromScriptFile(__filename)
  const reports = getReports(file)

  const safeReportsPartOne = reports.filter(report => new Report(report).isSafe())
  const safeReportsPartTwo = reports.filter(report =>
    Array.from(combinations(report, report.length - 1)).some(comb => new Report(comb).isSafe())
  )

  solutionLog(1, safeReportsPartOne.length)
  solutionLog(2, safeReportsPartTwo.length)
}

if (require.main === module) {
  run()
}