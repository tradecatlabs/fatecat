# Manseryeok (만세력)

Korean Saju (Four Pillars) and Manseryeok calculation library

한국 사주명리학의 만세력을 계산하는 TypeScript 라이브러리입니다.

양력/음력 날짜를 입력하면 정확한 사주팔자(년주, 월주, 일주, 시주)를 계산해줍니다.

## Features

- 🎯 정확한 사주팔자 계산 (년주, 월주, 일주, 시주)
- 🌙 음력/양력 자동 변환
- 📅 절기 기반 월주 계산
- 🔄 60갑자 순환 계산
- ⏰ 분(minute) 단위까지 고려한 정밀한 시주 계산
- ⚡ TypeScript 완벽 지원
- 🧪 철저한 테스트 커버리지

## Installation

```bash
npm install manseryeok
# or
yarn add manseryeok
# or
pnpm add manseryeok
```

## Usage

### Basic Usage (양력 사용)

```typescript
import { calculateFourPillars, fourPillarsToString } from 'manseryeok';

// 양력 날짜로 사주 계산
const result = calculateFourPillars({
  year: 1992,      // 연도 (양력)
  month: 10,       // 월 (양력, 1-12)
  day: 24,         // 일 (양력, 1-31)
  hour: 5,         // 시 (24시간제, 0-23)
  minute: 30       // 분 (0-59)
});

console.log(fourPillarsToString(result));
// 출력: 임신연주, 경술월주, 계유일주, 을묘시주

// 다양한 출력 형식
console.log(result.toString());
// 출력: 임신년주, 경술월주, 계유일주, 을묘시주

console.log(result.toObject());
// 출력: { year: '임신', month: '경술', day: '계유', hour: '을묘' }

console.log(result.toHanjaString());
// 출력: 壬申年柱, 庚戌月柱, 癸酉日柱, 乙卯時柱

console.log(result.toHanjaObject());
// 출력: {
//   year: { korean: '임신', hanja: '壬申' },
//   month: { korean: '경술', hanja: '庚戌' },
//   day: { korean: '계유', hanja: '癸酉' },
//   hour: { korean: '을묘', hanja: '乙卯' }
// }

// 음양오행 정보
console.log(result.dayElement);
// 출력: { stem: '수', branch: '금' }
// stem은 천간(계)의 오행, branch는 지지(유)의 오행

console.log(result.dayYinYang);
// 출력: { stem: '음', branch: '음' }
// stem은 천간(계)의 음양, branch는 지지(유)의 음양
```

### Using Lunar Calendar (음력 사용)

```typescript
// 음력 날짜로 사주 계산
const result = calculateFourPillars({
  year: 1992,              // 연도 (음력)
  month: 9,                // 월 (음력, 1-12)
  day: 29,                 // 일 (음력, 1-30)
  hour: 5,                 // 시 (24시간제, 0-23)
  minute: 30,              // 분 (0-59)
  isLunar: true,           // 음력 사용 여부 (필수)
  isLeapMonth: false       // 윤달 여부 (음력 사용시에만 필요)
});

// 위 음력 1992년 9월 29일은 양력 1992년 10월 24일과 동일
```

### Parameter Details

| 파라미터 | 타입 | 설명 | 범위/예시 |
|---------|------|------|----------|
| `year` | number | 연도 | 1900-2100 |
| `month` | number | 월 | 1-12 |
| `day` | number | 일 | 1-31 (양력), 1-30 (음력) |
| `hour` | number | 시 (24시간제) | 0-23 (0시 = 자정, 13시 = 오후 1시) |
| `minute` | number | 분 | 0-59 |
| `isLunar` | boolean? | 음력 사용 여부 | true/false (기본값: false) |
| `isLeapMonth` | boolean? | 윤달 여부 | true/false (음력일 때만 사용) |

### 시간 입력 예시

```typescript
// 새벽 3시 15분
const time1 = { hour: 3, minute: 15 };

// 오전 9시 정각
const time2 = { hour: 9, minute: 0 };

// 오후 2시 30분
const time3 = { hour: 14, minute: 30 };

// 밤 11시 45분
const time4 = { hour: 23, minute: 45 };
```

### Calendar Conversion (음력/양력 변환)

음력과 양력을 서로 변환할 수 있습니다:

```typescript
import { solarToLunar, lunarToSolar } from 'manseryeok';

// 양력 → 음력 변환
const lunar = solarToLunar(2024, 1, 1);
console.log(lunar); 
// { year: 2023, month: 11, day: 20, isLeapMonth: false }
// 2024년 1월 1일은 음력으로 2023년 11월 20일

// 음력 → 양력 변환
const solar = lunarToSolar(2023, 11, 20, false);
console.log(solar); 
// { year: 2024, month: 1, day: 1 }
// 음력 2023년 11월 20일은 양력으로 2024년 1월 1일

// 윤달 처리 예시
const leapMonthSolar = lunarToSolar(2020, 4, 1, true); // 2020년 윤4월 1일
console.log(leapMonthSolar);
// { year: 2020, month: 5, day: 23 }
```

### Additional Features

```typescript
import { 
  getHeavenlyStemYinYang,
  getHeavenlyStemElement,
  getEarthlyBranchElement 
} from 'manseryeok';

// 천간의 음양 확인
console.log(getHeavenlyStemYinYang('갑')); // '양'

// 천간의 오행 확인
console.log(getHeavenlyStemElement('갑')); // '목'

// 지지의 오행 확인
console.log(getEarthlyBranchElement('자')); // '수'
```

## API Reference

### Types

```typescript
interface BirthInfo {
  year: number;
  month: number;
  day: number;
  hour: number;
  minute: number;
  isLunar?: boolean;      // true면 음력, false/undefined면 양력
  isLeapMonth?: boolean;  // 음력 윤달 여부
}

interface Pillar {
  heavenlyStem: HeavenlyStem;   // 천간
  earthlyBranch: EarthlyBranch; // 지지
}

interface FourPillars {
  year: Pillar;   // 연주
  month: Pillar;  // 월주
  day: Pillar;    // 일주
  hour: Pillar;   // 시주
}
```

### Functions

- `calculateFourPillars(birthInfo: BirthInfo): FourPillars` - 사주 계산
- `fourPillarsToString(fourPillars: FourPillars): string` - 사주를 한국어 문자열로 변환
- `solarToLunar(year, month, day): LunarDate` - 양력을 음력으로 변환
- `lunarToSolar(year, month, day, isLeapMonth): SolarDate` - 음력을 양력으로 변환
- `getHeavenlyStemYinYang(stem: HeavenlyStem): YinYang` - 천간의 음양
- `getHeavenlyStemElement(stem: HeavenlyStem): FiveElement` - 천간의 오행
- `getEarthlyBranchElement(branch: EarthlyBranch): FiveElement` - 지지의 오행

## Time System (시간 체계)

### 12시진 체계

시주 계산은 다음의 12시진 체계를 따릅니다:

| 시진 | 시간대 | 24시간제 입력 예시 |
|------|--------|------------------|
| 자시(子時) | 23:00-01:00 | hour: 23 또는 hour: 0 |
| 축시(丑時) | 01:00-03:00 | hour: 1 또는 hour: 2 |
| 인시(寅時) | 03:00-05:00 | hour: 3 또는 hour: 4 |
| 묘시(卯時) | 05:00-07:00 | hour: 5 또는 hour: 6 |
| 진시(辰時) | 07:00-09:00 | hour: 7 또는 hour: 8 |
| 사시(巳時) | 09:00-11:00 | hour: 9 또는 hour: 10 |
| 오시(午時) | 11:00-13:00 | hour: 11 또는 hour: 12 |
| 미시(未時) | 13:00-15:00 | hour: 13 또는 hour: 14 |
| 신시(申時) | 15:00-17:00 | hour: 15 또는 hour: 16 |
| 유시(酉時) | 17:00-19:00 | hour: 17 또는 hour: 18 |
| 술시(戌時) | 19:00-21:00 | hour: 19 또는 hour: 20 |
| 해시(亥時) | 21:00-23:00 | hour: 21 또는 hour: 22 |

### 정확한 시주 계산

분(minute) 단위까지 고려하여 더 정확한 시주를 계산합니다:
- 각 시진의 경계에서 분을 고려하여 정확한 시진을 결정
- 예: 5시 30분은 묘시의 중반으로 정확하게 계산

## Development

```bash
# Install dependencies
pnpm install

# Run tests
pnpm test

# Build
pnpm build

# Lint
pnpm lint

# Format
pnpm format
```

## License

MIT © Yoohyojun

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## References

- 음력 데이터: 한국천문연구원
- 절기 계산: 천문학적 계산에 기반한 근사 공식
- 사주 계산: 전통 만세력 계산법

## Examples

### 실제 사용 예시

```typescript
// 1. 양력으로 입력
const saju1 = calculateFourPillars({
  year: 1990,
  month: 5,
  day: 15,
  hour: 14,    // 오후 2시
  minute: 30
});

// 2. 음력으로 입력 (음력 1990년 4월 21일)
const saju2 = calculateFourPillars({
  year: 1990,
  month: 4,
  day: 21,
  hour: 14,
  minute: 30,
  isLunar: true,
  isLeapMonth: false
});

// 3. 자정 출생
const saju3 = calculateFourPillars({
  year: 2000,
  month: 1,
  day: 1,
  hour: 0,     // 자정 (0시)
  minute: 0
});

// 4. 밤 11시 출생 (자시)
const saju4 = calculateFourPillars({
  year: 2000,
  month: 1,
  day: 1,
  hour: 23,    // 밤 11시 (자시)
  minute: 30
});
```