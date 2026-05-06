'use strict'
/* eslint-env node */

module.exports = {
    moduleFileExtensions: ['ts', 'tsx', 'js'],
    transform: {
        '^.+\\.(ts|tsx)$': ['ts-jest', { tsconfigFile: 'tsconfig.json' }],
    },
    testEnvironment: 'node',
    testMatch: ['**/test/**/*.(test|spec).(ts|tsx|js)'],
    coverageThreshold: {
        global: {
            branches: 60,
            functions: 60,
            lines: 60,
            statements: 60,
        },
    },
    collectCoverageFrom: ['src/**/*.{js,ts}', '!src/lib/**', '!src/main.ts'],
}
