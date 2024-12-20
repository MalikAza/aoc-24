import { isTwoArraysHaveSameOrderedElements, pairwise } from "@utils/iterations"

describe('isTwoArraysHaveSameOrderedElements', () => {
  test('should return true if two arrays have the same ordered elements', () => {
    const array1 = [1, 2, 3]
    const array2 = [1, 2, 3]

    expect(isTwoArraysHaveSameOrderedElements(array1, array2)).toBe(true)
  })

  test('should return false if two arrays have different ordered elements', () => {
    const array1 = [1, 2, 3]
    const array2 = [1, 3, 2]

    expect(isTwoArraysHaveSameOrderedElements(array1, array2)).toBe(false)
  })
})

describe('pairwise', () => {
  test('should return an array of pairs', () => {
    const array = [1, 2, 3, 4]
    const expected = [[1, 2], [2, 3], [3, 4]]

    expect(pairwise(array)).toEqual(expected)
  })
})