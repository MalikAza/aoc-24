import { memoize } from "@utils/memoize"

export type CornersPositions = {
  downRight: [number, number],
  downLeft: [number, number],
  upRight: [number, number],
  upLeft: [number, number]
}

export type NSEWPositions = {
  down: [number, number],
  right: [number, number],
  up: [number, number],
  left: [number, number]
}

export type AroundPositions = CornersPositions & NSEWPositions

export type Direction = '^' | '>' | 'v' | '<'

export class MapUtils {
  private startValue: string | null
  private endValue: string | null

  map: string[] | string[][]

  possibleDirections: Direction[] = ['^', '>', 'v', '<']
  start: [number, number] | null = null
  end: [number, number] | null = null

  constructor(data: string = '', startValue: string | null = null, endValue: string | null = null) {
    this.map = data.split('\n')
    this.startValue = startValue
    this.endValue = endValue

    this.searchStartAndEnd()
  }

  private searchStartAndEnd() {
    this.map.forEach((row, y) => {
      Array.from(row).forEach((cell, x) => {
        if (this.startValue && cell === this.startValue) {
          this.start = [x, y]
        }

        if (this.endValue && cell === this.endValue) {
          this.end = [x, y]
        }
      })
    })
  }

  isPositionOutOfBounds = memoize((position: [number, number]) => {
    const [x, y] = position
    return y < 0 || y >= this.map.length || x < 0 || x >= this.map[y].length
  })

  getPositionsToDown = memoize((position: [number, number]): [number, number] => {
    return [position[0], position[1] + 1]
  })

  getPositionsToRight = memoize((position: [number, number]): [number, number] => {
    return [position[0] + 1, position[1]]
  })

  getPositionsToUp = memoize((position: [number, number]): [number, number] => {
    return [position[0], position[1] - 1]
  })

  getPositionsToLeft = memoize((position: [number, number]): [number, number] => {
    return [position[0] - 1, position[1]]
  })

  getPositionsToDownRight = memoize((position: [number, number]): [number, number] => {
    return this.getPositionsToDown(this.getPositionsToRight(position))
  })

  getPositionsToDownLeft = memoize((position: [number, number]): [number, number] => {
    return this.getPositionsToDown(this.getPositionsToLeft(position))
  })

  getPositionsToUpRight = memoize((position: [number, number]): [number, number] => {
    return this.getPositionsToUp(this.getPositionsToRight(position))
  })

  getPositionsToUpLeft = memoize((position: [number, number]): [number, number] => {
    return this.getPositionsToUp(this.getPositionsToLeft(position))
  })

  getPositionsInCorners = memoize((position: [number, number]): CornersPositions => {
    return {
      downRight: this.getPositionsToDownRight(position),
      downLeft: this.getPositionsToDownLeft(position),
      upRight: this.getPositionsToUpRight(position),
      upLeft: this.getPositionsToUpLeft(position)
    }
  })

  getPositionsInNSEW = memoize((position: [number, number]): NSEWPositions => {
    return {
      down: this.getPositionsToDown(position),
      right: this.getPositionsToRight(position),
      up: this.getPositionsToUp(position),
      left: this.getPositionsToLeft(position)
    }
  })

  getPositionsAround = memoize((position: [number, number]): AroundPositions => {
    return {
      ...this.getPositionsInNSEW(position),
      ...this.getPositionsInCorners(position)
    }
  })

  getPositionToDirection = memoize((position: [number, number], direction: Direction): [number, number] => {
    switch (direction) {
      case '^':
        return this.getPositionsToUp(position)
      case '>':
        return this.getPositionsToRight(position)
      case 'v':
        return this.getPositionsToDown(position)
      case '<':
        return this.getPositionsToLeft(position)
    }
  })

  searchValue(value: string) {
    let positions: [number, number][] = []
    this.map.forEach((row, y) => {
      Array.from(row).forEach((cell, x) => {
        if (cell === value) {
          positions.push([x, y])
        }
      })
    })

    return positions
  }

  getCellValueFromPosition(position: [number, number]) {
    if (this.isPositionOutOfBounds(position)) {
      return null
    }

    return this.map[position[1]][position[0]]
  }
}