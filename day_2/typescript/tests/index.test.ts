import { getReports, Report } from ".."

describe('index example part one', () => {
  var reports: number[][]
  var file: string

  beforeAll(() => {
    file = "7 6 4 2 1\n1 2 7 8 9\n9 7 6 2 1\n1 3 2 4 5\n8 6 4 4 1\n1 3 6 7 9"
    reports = getReports(file)
  })

  test('reports length', () => {
    expect(reports.length).toBe(6)
  })

  test('first report is safe', () => {
    const reportObject = new Report(reports[0])

    expect(reportObject.isSafe()).toBe(true)
  })

  test('second report is unsafe', () => {
    const reportObject = new Report(reports[1])

    expect(reportObject.isSafe()).toBe(false)
  })

  test('third report is unsafe', () => {
    const reportObject = new Report(reports[2])

    expect(reportObject.isSafe()).toBe(false)
  })

  test('fourth report is unsafe', () => {
    const reportObject = new Report(reports[3])

    expect(reportObject.isSafe()).toBe(false)
  })

  test('fifth report is unsafe', () => {
    const reportObject = new Report(reports[4])

    expect(reportObject.isSafe()).toBe(false)
  })

  test('sixth report is safe', () => {
    const reportObject = new Report(reports[5])

    expect(reportObject.isSafe()).toBe(true)
  })

  test('length of reports which are safe', () => {
    const safeReports = reports.filter(report => new Report(report).isSafe())

    expect(safeReports.length).toBe(2)
  })
})

describe('Report.isContinuous', () => {
  test('should return true if the report is continuous', () => {
    const report = new Report([1, 2, 3])

    expect(report.isContinuous()).toBe(true)
  })

  test('should return true if the report is continuous in reverse', () => {
    const report = new Report([3, 2, 1])

    expect(report.isContinuous()).toBe(true)
  })

  test('should return false if the report is not continuous', () => {
    const report = new Report([1, 3, 2])

    expect(report.isContinuous()).toBe(false)
  })

  test('should return false if the report is not continuous in reverse', () => {
    const report = new Report([3, 1, 2])

    expect(report.isContinuous()).toBe(false)
  })
})

describe('Report.respectDifferences', () => {
  test('should return true if the report respect differences by 1', () => {
    const report = new Report([1, 2, 3])

    expect(report.respectDifferences()).toBe(true)
  })

  test('should return true if the report respect differences by 2', () => {
    const report = new Report([1, 3, 5])

    expect(report.respectDifferences()).toBe(true)
  })

  test('should return true if the report respect differences by 3', () => {
    const report = new Report([1, 4, 7])

    expect(report.respectDifferences()).toBe(true)
  })

  test('should return false if the report does not respect differences by 4', () => {
    const report = new Report([1, 3, 7])

    expect(report.respectDifferences()).toBe(false)
  })

  test('should return false if the report does not have differences', () => {
    const report = new Report([1, 1, 1])

    expect(report.respectDifferences()).toBe(false)
  })
})