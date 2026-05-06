import { Genius, getDetail, getPersonality, toCC } from '.';
import {
  DetailTestData,
  getDetailTestData,
  getPersonalityTestData,
} from './tests';

describe('integration testing', () => {
  describe('get the details', () => {
    it.each(Object.entries(getDetailTestData()) as [Genius, DetailTestData][])(
      'Outputs the same value as the data source from all genius: %s',
      (genius, expected) => {
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        const { affinity, ...actual } = getDetail(genius);
        expect(actual).toStrictEqual(expected);
      }
    );
  });
  describe('get the personality', () => {
    const testData = getPersonalityTestData();
    it.each(['1873-01-31', '2051-01-01', 'NaN', ''])(
      'Return an undefined value when specified an out ranged date: “%s”',
      (date) => expect(getPersonality(date)).toBeUndefined()
    );
    it('Outputs the same value as the data source from all dates in the range', () => {
      testData.forEach((source) => {
        // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
        const result = getPersonality(source.date)!;
        expect({ ...result, date: source.date }).toStrictEqual({
          ...source,
          lifeBase: source.lifeBase ?? result.lifeBase,
        });
      });
    });
    it('Outputs the string from the toCC function', () =>
      expect(toCC(testData[0])).toEqual(expect.any(String)));
  });
});
