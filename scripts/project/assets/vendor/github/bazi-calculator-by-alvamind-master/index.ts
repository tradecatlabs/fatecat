// Example usage
import { BaziCalculator } from './src/bazi-calculator';

const calculator = new BaziCalculator(1990, 5, 10, 12, 'male');
const analysis = calculator.getCompleteAnalysis();
console.dir(analysis, {
  depth: null,  // Show all nesting levels
  colors: true  // Enable colors
});
