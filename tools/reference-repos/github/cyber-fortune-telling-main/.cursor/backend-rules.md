# Backend Development Rules - Strapi + AI Integration

## Framework Standards
- **Strapi 5.10.3**: Use latest Strapi features and best practices
- **Node.js 22.14.0+**: Modern JavaScript/ES6+ features
- **OpenAI API 4.96.2**: AI integration with DeepSeek provider
- **IntelliNode 2.2.9**: Enhanced AI capabilities and model management

## Project Structure
```
backend/
├── config/             # Strapi configuration files
├── src/
│   ├── api/           # API endpoints and business logic
│   ├── admin/         # Admin panel customizations
│   ├── components/    # Reusable Strapi components
│   └── extensions/    # Strapi extensions
├── database/
│   └── migrations/    # Database migration files
└── public/
    └── uploads/      # File uploads directory
```

## API Development Guidelines

### Content Types
- **fortune-telling-user**: User birth chart information
- **anything-response**: AI-generated responses
- **anything-request**: Fortune telling requests
- **sign-in**: User authentication records

### Controller Structure
```javascript
'use strict';

/**
 * Controller for handling fortune telling requests
 * This module provides functionality to generate fortune telling predictions
 */
const { createCoreController } = require('@strapi/strapi').factories;

module.exports = createCoreController('api::model-name.model-name', ({ strapi }) => ({
  // Custom controller methods
}));
```

## AI Integration Best Practices

### DeepSeek API Configuration
```javascript
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  baseURL: process.env.OPENAI_BASE_URL || "https://api.deepseek.com/v1",
});
```

### IntelliNode Integration
```javascript
const { Chatbot, ChatGPTInput, SupportedChatModels } = require("intellinode");

// Initialize AI chatbot with proper configuration
const chatbot = new Chatbot(
  process.env.OPENAI_API_KEY,
  SupportedChatModels.OPENAI,
  {
    baseURL: process.env.OPENAI_BASE_URL
  }
);
```

### Prompt Engineering
- Use `buildFortuneTellingPrompt` for consistent prompt structure
- Include Chinese traditional elements in prompts
- Implement contextual awareness for user birth charts
- Handle multi-turn conversations effectively

### Error Handling
```javascript
// Implement robust error handling for AI APIs
try {
  const response = await openai.chat.completions.create({
    model: "deepseek-chat",
    messages: messages,
    temperature: 0.7,
    max_tokens: 4000,
  });
  
  return response.choices[0].message.content;
} catch (error) {
  console.error("AI API Error:", error);
  throw new ApplicationError("AI service temporarily unavailable", 503);
}
```

## Database Management

### PostgreSQL Configuration
```javascript
// config/database.js
module.exports = ({ env }) => ({
  connection: {
    client: 'postgres',
    connection: {
      host: env('DATABASE_HOST', 'localhost'),
      port: env.int('DATABASE_PORT', 5432),
      database: env('DATABASE_NAME', 'fortune_telling'),
      user: env('DATABASE_USERNAME', 'strapi'),
      password: env('DATABASE_PASSWORD', 'strapi'),
      ssl: env.bool('DATABASE_SSL', false),
    },
  },
});
```

### Data Validation
- Implement proper schema validation
- Use Strapi's built-in validation features
- Validate date formats for Chinese calendar
- Ensure user input sanitization

## Security Implementation

### Authentication & Authorization
- Use JWT tokens for API authentication
- Implement role-based access control
- Secure sensitive endpoints
- Validate user permissions

### API Security
```javascript
// Implement API rate limiting
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP'
});
```

### Environment Variables
```javascript
// Secure environment configuration
const requiredEnvVars = [
  'OPENAI_API_KEY',
  'JWT_SECRET',
  'ADMIN_JWT_SECRET',
  'DATABASE_PASSWORD'
];

requiredEnvVars.forEach(envVar => {
  if (!process.env[envVar]) {
    throw new Error(`Missing required environment variable: ${envVar}`);
  }
});
```

## Fortune Telling Logic

### Chinese Astrology Integration
```javascript
// Implement traditional Chinese astrology calculations
const calculateBaZi = (birthDate, birthTime) => {
  // Use lunar-javascript for accurate calculations
  const lunar = Lunar.fromDate(birthDate);
  return {
    year: lunar.getYearInGanZhi(),
    month: lunar.getMonthInGanZhi(),
    day: lunar.getDayInGanZhi(),
    hour: calculateHourPillar(birthTime)
  };
};
```

### Daily Fortune Generation
- Generate unique fortune content daily
- Include feng shui ornament recommendations
- Provide personalized advice based on birth chart
- Implement content caching for performance

## Service Architecture

### Custom Services
```javascript
// src/api/fortune-telling/services/fortune-telling.js
module.exports = ({ strapi }) => ({
  async generateDailyFortune(userId) {
    const user = await strapi.entityService.findOne('api::fortune-telling-user.fortune-telling-user', userId);
    const prompt = buildFortuneTellingPrompt(user);
    return await this.callAI(prompt);
  },

  async callAI(prompt) {
    // AI integration logic
  }
});
```

### Background Jobs
- Implement daily fortune generation
- Use MQTT for real-time updates
- Handle scheduled tasks efficiently
- Implement job queues for scalability

## Performance Optimization

### Caching Strategy
```javascript
// Implement Redis caching for AI responses
const redis = require('redis');
const client = redis.createClient();

const cacheKey = `fortune:${userId}:${date}`;
const cached = await client.get(cacheKey);

if (cached) {
  return JSON.parse(cached);
}

// Generate new fortune and cache it
const fortune = await generateFortune(userId, date);
await client.setex(cacheKey, 86400, JSON.stringify(fortune)); // Cache for 24 hours
```

### Database Optimization
- Use proper indexes for frequently queried fields
- Implement pagination for large datasets
- Optimize queries with select filters
- Use database pooling for connections

## Error Handling & Logging

### Structured Logging
```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});
```

### Error Response Format
```javascript
// Consistent error response structure
const formatError = (error, code = 500) => ({
  error: {
    status: code,
    name: error.name,
    message: error.message,
    details: error.details || null
  }
});
```

## Testing Guidelines

### Unit Testing
- Test AI integration functions
- Mock external API calls
- Test fortune generation logic
- Validate Chinese calendar calculations

### Integration Testing
- Test complete API endpoints
- Verify database interactions
- Test authentication flows
- Validate AI response processing

## Deployment Considerations

### Docker Configuration
```dockerfile
# Use multi-stage build for optimization
FROM node:22.14.0-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:22.14.0-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
EXPOSE 1337
CMD ["npm", "start"]
```

### Health Checks
```javascript
// Implement health check endpoint
module.exports = {
  async health(ctx) {
    const checks = {
      database: await checkDatabase(),
      ai: await checkAIService(),
      cache: await checkCache()
    };
    
    ctx.body = { status: 'healthy', checks };
  }
};
```

## Monitoring & Maintenance

### Performance Monitoring
- Track API response times
- Monitor AI API usage and costs
- Log database query performance
- Track error rates and patterns

### Maintenance Tasks
- Regular database cleanup
- AI prompt optimization
- Security updates
- Performance tuning 