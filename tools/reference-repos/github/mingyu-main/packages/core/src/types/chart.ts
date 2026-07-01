export type ChartInput = {
  name: string;
  dateType: 'solar' | 'lunar';
  birthDate: string;
  birthTimeIndex: number;
  gender: '男' | '女';
  isLeapMonth?: boolean;
  fixLeap?: boolean;
  algorithm?: 'default' | 'zhongzhou';
  yearDivide?: 'normal' | 'exact';
  horoscopeDivide?: 'normal' | 'exact';
  ageDivide?: 'normal' | 'birthday';
  dayDivide?: 'current' | 'forward';
};
