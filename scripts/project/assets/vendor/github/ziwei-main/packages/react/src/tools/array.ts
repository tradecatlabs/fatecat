export function isArrayEqual<T>(array1: T[], array2: T[]): boolean {
  if (array1 !== array2) {
    if (array1.length !== array2.length) {
      return false;
    }
    for (let i = 0; i < array1.length; i++) {
      if (!Object.is(array1[i], array2[i])) {
        return false;
      }
    }
  }
  return true;
}
