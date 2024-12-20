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