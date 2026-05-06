declare module 'js-calendar-converter' {
    export declare const calendar: {
        solar2lunar: (
            solarYear: number,
            solarMonth: number,
            solarDay: number,
        ) =>
            | -1
            | {
                  lYear: number
                  lMonth: number
                  lDay: number
                  isLeap: boolean
                  gzYear: string
                  gzMonth: string
                  gzDay: string
              }
        lunar2solar: (
            lunarYear: number,
            lunarMonth: number,
            lunarDay: number,
            isLeapMonth: boolean,
        ) =>
            | -1
            | {
                  cYear: number
                  cMonth: number
                  cDay: number
                  gzYear: string
                  gzMonth: string
                  gzDay: string
              }
    }
}
