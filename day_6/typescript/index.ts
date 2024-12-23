import { getInputFileFromScriptFile } from "@utils/input"
import { MapUtils } from "@utils/map"
import { solutionLog } from "@utils/solutionLog"

class Map extends MapUtils {
  private guardIcon: '^' | '>' | 'v' | '<'
  private visitedCells: Array<[number, number]> = []
  private guardPosition: [number, number] | null

  constructor(data: string) {
    super(data, '^')
    this.guardPosition = this.start
    this.guardIcon = '^'
  }

  getNextGuardPosition() {
    return this.getPositionToDirection(this.guardPosition!, this.guardIcon)
  }

  turnGuardRight() {
    switch (this.guardIcon) {
      case '^':
        this.guardIcon = '>'
        break
      case '>':
        this.guardIcon = 'v'
        break
      case 'v':
        this.guardIcon = '<'
        break
      case '<':
        this.guardIcon = '^'
        break
    }
  }

  isGuardOutOfBounds() {
    return this.isPositionOutOfBounds(this.guardPosition!)
  }

  solvePartOne() {
    while (!this.isGuardOutOfBounds()) {
      this.visitedCells.push(this.guardPosition!)
      let nextGuardPos = this.getNextGuardPosition()
      if (!this.isPositionOutOfBounds(nextGuardPos) && this.getCellValueFromPosition(nextGuardPos) === '#') {
        this.turnGuardRight()
        nextGuardPos = this.getPositionToDirection(this.guardPosition!, this.guardIcon)
      }

      this.guardPosition = nextGuardPos
    }

    return new Set(this.visitedCells.map((pos) => `${pos[0]},${pos[1]}`)).size
  }
}

function run() {
  const file = getInputFileFromScriptFile(__filename)
  const map = new Map(file)

  solutionLog(1, map.solvePartOne())
}

if (require.main === module) {
  run()
}