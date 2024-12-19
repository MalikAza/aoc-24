export function solutionLog(part: number, solution: number) {
  let partString: string = ''
  
  switch (part) {
    case 1:
      partString = 'one'
      break
    case 2:
      partString = 'two'
      break
  }

  console.log(`Part ${partString} solution is: ${solution}`)
}