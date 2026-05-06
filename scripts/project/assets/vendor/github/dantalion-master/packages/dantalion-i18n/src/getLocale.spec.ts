import getLocale from './getLocale';

describe('`getLocale()` function', () => {
  describe('getLocale()', () => {
    it('Get the string', () => expect(getLocale()).toEqual(expect.any(String)));
  });
});
