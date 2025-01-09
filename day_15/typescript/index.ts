import { getInputFileFromScriptFile } from "@utils/input"
import { Direction, MapUtils } from "@utils/map"
import { memoize } from "@utils/memoize"
import { solutionLog } from "@utils/solutionLog"
import { Part } from "@utils/types"

class Map extends MapUtils {
  map: string[][]
  directions: string[]
  robotPosition: [number, number]
  walls: [number, number][]

  ROBOT_SYMBOL = '@'
  WALL_SYMBOL = '#'
  BOX_SYMBOL = 'O'
  EMPTY_SYMBOL = '.'

  constructor(data: string) {
    super()
    const [map, directions] = data.split('\n\n')

    this.map = map.split('\n').map((row) => Array.from(row))
    this.directions = Array.from(directions.trim().replace(/\s+/g, ''))
    this.robotPosition = this.getRobotPosition()
    this.walls = this.getWalls()
  }

  isPositionWall = memoize((position: [number, number]) => {
    return this.walls.includes(position)
  })

  getRobotPosition() {
    return this.searchValue(this.ROBOT_SYMBOL)[0]
  }

  getWalls() {
    return this.searchValue(this.WALL_SYMBOL)
  }

  getBoxes() {
    return this.searchValue(this.BOX_SYMBOL)
  }

  howMuchDistanceBeforeWalls(position: [number, number], direction: Direction) {
    let distance = 1
    let nextPos = this.getPositionToDirection(position, direction)

    while (true) {
      if (this.getCellValueFromPosition(nextPos) == this.WALL_SYMBOL) {
        break
      }

      nextPos = this.getPositionToDirection(nextPos, direction)
      distance += 1
    }

    return distance
  }

  getGPSCoordinatesFromPosition(position: [number, number]) {
    const [fromLeft, fromTop] = position

    return 100 * fromTop + fromLeft
  }

  setRobotPosition(position: [number, number]) {
    this.map[this.robotPosition[1]][this.robotPosition[0]] = this.EMPTY_SYMBOL
    this.map[position[1]][position[0]] = this.ROBOT_SYMBOL
    this.robotPosition = position
  }

  robotAttemptToPush(boxPosition: [number, number], direction: Direction) {
    let nextPos = this.getPositionToDirection(boxPosition, direction)
    let nextPosValue = this.getCellValueFromPosition(nextPos)

    let next = true
    while (next) {
      switch (nextPosValue) {
        case this.WALL_SYMBOL:
          next = false
          break
        case this.EMPTY_SYMBOL:
          const robotPosition = this.robotPosition
          this.map[robotPosition[1]][robotPosition[0]] = this.EMPTY_SYMBOL

          this.setRobotPosition(boxPosition)
          this.map[nextPos[1]][nextPos[0]] = this.BOX_SYMBOL
          next = false
          break
        case this.BOX_SYMBOL:
          nextPos = this.getPositionToDirection(nextPos, direction)
          nextPosValue = this.getCellValueFromPosition(nextPos)
          continue
      }
    }
  }

  moveRobotInDirection(direction: Direction) {
    const nextPos = this.getPositionToDirection(this.robotPosition, direction)
    const nextPosValue = this.getCellValueFromPosition(nextPos)

    switch (nextPosValue) {
      case this.EMPTY_SYMBOL:
        this.setRobotPosition(nextPos)
        break
      case this.BOX_SYMBOL:
        this.robotAttemptToPush(nextPos, direction)
        break
    }
  }

  run() {
    for (const direction of this.directions) {
      this.moveRobotInDirection(direction as Direction)
    }
  }

  solve(part: Part): number {
    switch (part) {
      case 1:
        this.run()
        return this.getBoxes().reduce((acc, box) => acc + this.getGPSCoordinatesFromPosition(box), 0)
      case 2:
        return 0
    }
  }
}

function run() {
  const file = getInputFileFromScriptFile(__filename)
  const map = new Map(file)

  solutionLog(1, map.solve(1))
}

if (require.main === module) {
  run()
}