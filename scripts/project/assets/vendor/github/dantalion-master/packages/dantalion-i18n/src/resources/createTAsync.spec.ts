import createTAsync from './createTAsync';

describe('`createTAsync()` function', () => {
  it('Get the function', async () =>
    expect(await createTAsync()).toEqual(expect.any(Function)));
});
