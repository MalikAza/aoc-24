const { execSync } = require('child_process')
const day = process.argv[2]

if (!day) {
  console.error('Please provide a day number, e.g.: yarn exec 1')
  process.exit(1)
}

const command = `ts-node -r tsconfig-paths/register day_${day}/typescript/index.ts`
console.log(`Executing: ${command}`)
execSync(command, { stdio: 'inherit' })