# Bazi Calculator by Alvamind 八字计算器

<div align="center">

[![npm version](https://badge.fury.io/js/bazi-calculator-by-alvamind.svg)](https://badge.fury.io/js/bazi-calculator-by-alvamind)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![TypeScript](https://img.shields.io/badge/TypeScript-Ready-blue.svg)](https://www.typescriptlang.org/)
[![Downloads](https://img.shields.io/npm/dt/bazi-calculator-by-alvamind.svg)](https://www.npmjs.com/package/bazi-calculator-by-alvamind)

A modern, accurate, and comprehensive Bazi (八字 / Four Pillars of Destiny) calculator and analyzer for Node.js environments.

[Installation](#installation) • [Quick Start](#quick-start) • [Documentation](#detailed-documentation) • [Contributing](#contributing)

</div>

## 📢 Disclaimer

This package is provided for educational and research purposes only. The calculations and interpretations should not be used as the sole basis for making important life decisions. Chinese Metaphysics and Bazi analysis require professional expertise and years of study.

## ✨ Features

### Core Calculations
- **Four Pillars (四柱)**
  - Year Pillar (年柱)
  - Month Pillar (月柱)
  - Day Pillar (日柱)
  - Hour Pillar (時柱)
- **Solar/Lunar Calendar Conversions**
- **Precise Time Calculations**

### Analysis Components
- **Five Elements (五行) Analysis**
  - Element Distribution
  - Element Relationships
  - Element Strength Calculations
- **Day Master (日主) Analysis**
  - Yin/Yang Nature
  - Element Properties
  - Stem Relationships
- **Eight Mansions (八宅) Feng Shui**
  - Life Gua Calculation
  - Direction Analysis
  - Lucky/Unlucky Sectors
- **Destiny Indicators**
  - Nobleman (貴人)
  - Intelligence Star (文昌)
  - Sky Horse (天馬)
  - Peach Blossom (桃花)

### Technical Features
- 🔒 Type-safe with TypeScript
- 📦 ES Module Support
- 🏗️ SOLID Architecture
- 🔄 JSON-based Date Mapping
- 📝 Comprehensive Type Definitions
- ⚡ Optimized Performance

## 🚀 Installation

```bash
# Using npm
npm install bazi-calculator-by-alvamind

# Using yarn
yarn add bazi-calculator-by-alvamind

# Using pnpm
pnpm add bazi-calculator-by-alvamind
```

## 🎯 Quick Start

```typescript
import { BaziCalculator } from 'bazi-calculator-by-alvamind';

// Initialize calculator
const calculator = new BaziCalculator(
  1990,    // Year
  5,       // Month
  10,      // Day
  12,      // Hour (24-hour format)
  'male'   // Gender
);

// Get complete analysis
const analysis = calculator.getCompleteAnalysis();

// Display Chinese characters
console.log(calculator.toString()); // 庚午年辛巳月乙酉日壬午時
```

## 📖 Detailed Documentation

### Basic Usage

#### Getting Basic Analysis
```typescript
const basicAnalysis = calculator.calculateBasicAnalysis();
```

#### Calculating Pillars Only
```typescript
const pillars = calculator.calculatePillars();
```

### Example Output

<details>
<summary>Click to view complete analysis output</summary>

```json
{
  "mainPillars": {
    "year": {
      "chinese": "庚午",
      "element": "METAL",
      "animal": "Horse",
      "branch": { "element": "FIRE" }
    },
    "month": {
      "chinese": "辛巳",
      "element": "METAL",
      "animal": "Snake",
      "branch": { "element": "FIRE" }
    },
    "day": {
      "chinese": "乙酉",
      "element": "WOOD",
      "animal": "Rooster",
      "branch": { "element": "METAL" }
    },
    "time": {
      "chinese": "壬午",
      "element": "WATER",
      "animal": "Horse",
      "branch": { "element": "FIRE" }
    }
  },
  "basicAnalysis": {
    "lifeGua": 1,
    "dayMaster": {
      "stem": "乙",
      "nature": "Yin",
      "element": "WOOD"
    },
    "nobleman": ["子", "申"],
    "intelligence": "巳",
    "skyHorse": "卯",
    "peachBlossom": "酉",
    "fiveFactors": {
      "WOOD": 13,
      "FIRE": 38,
      "EARTH": 0,
      "METAL": 38,
      "WATER": 12
    },
    "eightMansions": {
      "group": "East",
      "lucky": {
        "wealth": "SE",
        "health": "E",
        "romance": "S",
        "career": "N"
      },
      "unlucky": {
        "obstacles": "NW",
        "quarrels": "W",
        "setbacks": "SW",
        "totalLoss": "NE"
      }
    }
  }
}
```
</details>

### API Reference

#### BaziCalculator Class

```typescript
class BaziCalculator {
  constructor(
    year: number,     // Gregorian year
    month: number,    // Month (1-12)
    day: number,      // Day (1-31)
    hour: number,     // Hour (0-23)
    gender?: GenderType // 'male' | 'female'
  )

  // Main methods
  calculatePillars(): Pillars
  calculateBasicAnalysis(): BasicAnalysis
  getCompleteAnalysis(): CompleteAnalysis
  toString(): string
}
```

## 🤝 Contributing

We welcome contributions! See our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/bazi-calculator-by-alvamind.git

# Install dependencies
npm install

# Run tests
npm test

# Build
npm run build
```

## 📝 Important Notes

### Calculation Methods
- Solar calendar based calculations
- Traditional Chinese time system (12 two-hour periods)
- Standard Stem-Branch (干支) system
- Eight Mansions Feng Shui principles

### Limitations
- Time zone considerations
- Lunar calendar approximations
- Regional variations in interpretations

## 🙏 Acknowledgements

- Traditional Chinese Metaphysics texts and masters
- Modern Bazi research and practitioners
- Open source community contributors
- Chinese calendar conversion references

## 📄 License

MIT License - see the [LICENSE](LICENSE) file for details.

## 💬 Support

- 📧 Email: support@alvamind.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/bazi-calculator-by-alvamind/issues)
- 📚 Wiki: [Documentation](https://github.com/yourusername/bazi-calculator-by-alvamind/wiki)

## 🌟 References

1. Chinese Metaphysics Classics
2. Modern Bazi Analysis Methods
3. Traditional Calendar Systems
4. Stem-Branch Theory

---

<div align="center">

**Made with ❤️ by [Alvamind](https://github.com/alvamind)**

*For professional consultations, please consult a qualified Bazi practitioner.*

</div>
