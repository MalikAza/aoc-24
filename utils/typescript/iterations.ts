export function pairwise(iterable: Array<any>) {
  let pairs = []
  
  for (const [i, item] of iterable.entries()) {
    if (i === iterable.length - 1) break

    pairs.push([item, iterable[i + 1]])
  }

  return pairs
}

export function isTwoArraysHaveSameOrderedElements(array1: Array<any>, array2: Array<any>): boolean {
  return array1.every((item, index) => item === array2[index])
}

export function* combinations(iterable: Array<any>, length: number): Generator<Array<any>> {
  if (length === 1) {
    for (const item of iterable) {
      yield [item]
    }
    return
  }

  for (let i = 0; i <= iterable.length - length; i++) {
    for (const comb of combinations(iterable.slice(i + 1), length - 1)) {
      yield [iterable[i], ...comb]
    }
  }
}

export function product<Item>(iterable: Item[], repeat: number): Item[][] {
  if (repeat <= 0 || iterable.length === 0) {
    return []
  }

  let pools = Array(repeat).fill(iterable)
  let result = pools[0].map((x: Item) => [x])

    for (let i = 1; i < pools.length; i++) {
        const temp = []
        for (const x of result) {
            for (const y of pools[i]) {
                temp.push([...x, y])
            }
        }
        result = temp
    }

    return result
}