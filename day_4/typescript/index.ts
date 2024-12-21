import { getInputFileFromScriptFile } from "@utils/input"
import { MapUtils } from "@utils/map"
import { solutionLog } from "@utils/solutionLog"
import { Part } from "@utils/types"

type Direction = 'downRight' | 'downLeft' | 'upRight' | 'upLeft' | 'right' | 'left' | 'down' | 'up'

class Map extends MapUtils {
  constructor(data: string) {
    super(data)
  }

  private howManyXmasOrSamx(to_search: string): number {
    const pattern = /(XMAS|SAMX)/g
    const matches = Array.from(to_search.matchAll(pattern))

    return matches.length
  }

  private regroupMaxFourElementsInDirectionFromPosition(pos: [number, number], direction: Direction) {
    let positions = [pos]
    let currentPos = pos

    for (let i = 0; i < 3; i++) {
      currentPos = this.getPositionsAround(currentPos)[direction]

      if (!this.isPositionOutOfBounds(currentPos)) {
        positions.push(currentPos)
      }
    }

    return positions.map(pos => this.getCellValueFromPosition(pos) as string).reduce((acc, curr) => `${acc}${curr}`, '')
  }

  private howManyInDirectionForPosition(pos: [number, number], directions: Direction[]): number {
    return directions.map(direction =>
      this.howManyXmasOrSamx(
        this.regroupMaxFourElementsInDirectionFromPosition(pos, direction)
      )
    ).reduce((acc, curr) => acc + curr, 0)
  }

  private isPositionXMased(pos: [number, number]): boolean {
    const value = this.getCellValueFromPosition(pos)

    if (value !== 'A') {
      return false
    }

    const corners = this.getPositionsInCorners(pos)

    // Ms at bottom and Ss at top
    if (this.getCellValueFromPosition(corners.downLeft) == 'M' &&
        this.getCellValueFromPosition(corners.downRight) == 'M' &&
        this.getCellValueFromPosition(corners.upLeft) == 'S' &&
        this.getCellValueFromPosition(corners.upRight) == 'S'
    ) return true

    // Ms at top and Ss at bottom
    if (this.getCellValueFromPosition(corners.downLeft) == 'S' &&
        this.getCellValueFromPosition(corners.downRight) == 'S' &&
        this.getCellValueFromPosition(corners.upLeft) == 'M' &&
        this.getCellValueFromPosition(corners.upRight) == 'M'
    ) return true

    // Ms at left and Ss at right
    if (this.getCellValueFromPosition(corners.downLeft) == 'M' &&
        this.getCellValueFromPosition(corners.downRight) == 'S' &&
        this.getCellValueFromPosition(corners.upLeft) == 'M' &&
        this.getCellValueFromPosition(corners.upRight) == 'S'
    ) return true

    // Ms at right and Ss at left
    if (this.getCellValueFromPosition(corners.downLeft) == 'S' &&
        this.getCellValueFromPosition(corners.downRight) == 'M' &&
        this.getCellValueFromPosition(corners.upLeft) == 'S' &&
        this.getCellValueFromPosition(corners.upRight) == 'M'
    ) return true

    return false
  }

  solve(part: Part): number {
    switch (part) {
      case 1:
        return this.map.reduce((acc, row, y) => {
          return acc + Array.from(row).reduce((acc, cell, x) => {
            return acc + this.howManyInDirectionForPosition([x, y], ['right', 'down', 'downRight', 'downLeft'])
          }, 0)
        }, 0)
      case 2:
        return this.map.reduce((acc, row, y) => {
          return acc + Array.from(row).reduce((acc, cell, x) => {
            return this.isPositionXMased([x, y]) ? acc + 1 : acc
          }, 0)
        }, 0)
    }
  }
}

function run() {
  const file = getInputFileFromScriptFile(__filename)
  const map = new Map(file)

  solutionLog(1, map.solve(1))
  solutionLog(2, map.solve(2))
}

if (require.main === module) {
  run()
}