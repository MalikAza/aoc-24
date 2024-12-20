/** @type {import('ts-jest').JestConfigWithTsJest} */
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['.'],
  modulePaths: ['<rootDir>'],
  moduleNameMapper: {
    '^@utils/(.*)$': '<rootDir>/utils/typescript/$1',
  },
  transform: {
    '^.+\\test.tsx?$': [
      'ts-jest',
      {
        tsconfig: './tsconfig.json'
      }
    ]
  }
};