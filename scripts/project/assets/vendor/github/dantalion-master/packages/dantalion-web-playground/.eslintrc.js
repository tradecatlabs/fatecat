module.exports = {
  env: { es6: true, es2020: true },
  extends: [
    // TODO: I want to know the best practices for the settings here.
    // I don't know it, but these so many definitions are enough to make it feel non-exemplary.
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
    'plugin:import/recommended',
    'plugin:import/typescript',
    'plugin:@typescript-eslint/recommended',
    'next',
    'airbnb-typescript',
    'plugin:prettier/recommended',
  ],
  overrides: [
    {
      files: ['*.js'],
      rules: { '@typescript-eslint/no-var-requires': 'off' },
    },
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 2020,
    project: 'tsconfig.json',
    // ! I'm giving up using YAML just for this path resolution.
    tsconfigRootDir: __dirname,
  },
  root: true,
  rules: {
    'import/no-extraneous-dependencies': [
      'error',
      {
        devDependencies: [
          '**/*.config.{j,t}s',
          '**/*.{spec,stories,test}.{j,t}{s,sx}',
        ],
      },
    ],
    'import/order': 'warn',
    'react/prop-types': 'off',
    'react/react-in-jsx-scope': 'off',
    'sort-imports': ['warn', { ignoreCase: true, ignoreDeclarationSort: true }],
  },
  settings: {
    'import/resolver': { node: { path: ['src'] }, typescript: {} },
  },
};
