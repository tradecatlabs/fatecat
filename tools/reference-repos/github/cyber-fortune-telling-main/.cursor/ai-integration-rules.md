# AI Integration Rules - DeepSeek & Fortune Telling

## AI Service Configuration

### DeepSeek API Setup
```javascript
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  baseURL: process.env.OPENAI_BASE_URL || "https://api.deepseek.com/v1",
  timeout: 30000,
  maxRetries: 3,
});
```

### Model Selection
- **Primary Model**: `deepseek-chat` for general fortune telling
- **Fallback Strategy**: Implement graceful degradation when API fails
- **Temperature**: 0.7 for balanced creativity and consistency
- **Max Tokens**: 4000 for comprehensive responses

## Prompt Engineering Guidelines

### Fortune Telling Prompt Structure
```javascript
const buildFortuneTellingPrompt = (userInfo) => {
  const { birthDate, birthTime, gender, location } = userInfo;
  
  return `
You are a master fortune teller with deep knowledge of Chinese traditional astrology, feng shui, and divination.

User Information:
- Birth Date: ${birthDate}
- Birth Time: ${birthTime}
- Gender: ${gender}
- Location: ${location}

Current Context:
- Date: ${new Date().toISOString().split('T')[0]}
- Lunar Date: ${getLunarDate()}
- Time: ${getChineseTraditionalTime()}

Please provide a comprehensive fortune reading that includes:
1. Daily fortune analysis based on birth chart
2. Feng shui ornament recommendation with specific image
3. Lucky numbers and colors for today
4. Relationship and career advice
5. Health and wellness suggestions
6. Auspicious activities for today

Format the response with proper markdown structure and include specific feng shui ornament images using: ![ornament](image_url)

Remember to maintain cultural sensitivity and provide positive, constructive guidance.
`;
};
```

### Chat Conversation Prompts
```javascript
const buildChatPrompt = (userMessage, context) => {
  return `
You are a wise and knowledgeable fortune teller assistant. The user has the following birth chart information:
${context.userInfo}

Current conversation context:
${context.previousMessages}

User's question: ${userMessage}

Please respond in a helpful, mystical yet practical manner. Include relevant Chinese traditional wisdom when appropriate.
`;
};
```

## Chinese Traditional Elements Integration

### Lunar Calendar Integration
```javascript
const getLunarCalendarInfo = (date) => {
  const lunar = Lunar.fromDate(date);
  return {
    lunarDate: lunar.toString(),
    zodiacAnimal: lunar.getYearZodiac(),
    heavenlyStem: lunar.getYearInGanZhi(),
    element: lunar.getYearNaYin(),
    constellation: lunar.getXiu(),
    gua: lunar.getDayLunar().getGua()
  };
};
```

### Ba Zi (Eight Characters) Calculation
```javascript
const calculateBaZi = (birthDate, birthTime) => {
  const lunar = Lunar.fromDate(birthDate);
  return {
    year: {
      stem: lunar.getYearGan(),
      branch: lunar.getYearZhi(),
      element: lunar.getYearNaYin()
    },
    month: {
      stem: lunar.getMonthGan(),
      branch: lunar.getMonthZhi(),
      element: lunar.getMonthNaYin()
    },
    day: {
      stem: lunar.getDayGan(),
      branch: lunar.getDayZhi(),
      element: lunar.getDayNaYin()
    },
    hour: calculateHourPillar(birthTime)
  };
};
```

## Feng Shui Ornament Selection

### Ornament Database
```javascript
const fengShuiOrnaments = {
  wealth: ['金蟾', '貔貅', '五帝钱'],
  career: ['文昌塔', '龙龟'],
  love: ['福禄寿三星', '大象'],
  health: ['水晶洞', '葫芦'],
  protection: ['关公像']
};

const selectOrnament = (userInfo, dailyFortune) => {
  const { element, zodiac, currentNeed } = analyzeBaZi(userInfo);
  return matchOrnamentToNeeds(element, zodiac, currentNeed);
};
```

### Image Path Generation
```javascript
const generateOrnamentImagePath = (ornamentName) => {
  const baseUrl = '/desk-decor/';
  const variants = getOrnamentVariants(ornamentName);
  return `${baseUrl}${ornamentName}${getRandomVariant(variants)}.png`;
};
```

## Response Processing

### Markdown Content Extraction
```javascript
const extractDesktopDecoration = (content) => {
  const parser = new DOMParser();
  const doc = parser.parseFromString(content, "text/html");
  const deskDecorImg = doc.querySelector("img.desk-decor");
  return deskDecorImg ? deskDecorImg.getAttribute("src") : "";
};
```

### Content Validation
```javascript
const validateAIResponse = (response) => {
  const requiredElements = [
    'daily fortune',
    'feng shui ornament',
    'lucky numbers',
    'lucky colors',
    'advice'
  ];
  
  return requiredElements.every(element => 
    response.toLowerCase().includes(element.toLowerCase())
  );
};
```

## Error Handling & Fallbacks

### API Failure Handling
```javascript
const callAIWithFallback = async (prompt, retries = 3) => {
  for (let i = 0; i < retries; i++) {
    try {
      const response = await openai.chat.completions.create({
        model: "deepseek-chat",
        messages: [{ role: "user", content: prompt }],
        temperature: 0.7,
        max_tokens: 4000,
      });
      
      return response.choices[0].message.content;
    } catch (error) {
      console.error(`AI API attempt ${i + 1} failed:`, error);
      
      if (i === retries - 1) {
        return getDefaultFortune(); // Fallback to default content
      }
      
      await delay(1000 * Math.pow(2, i)); // Exponential backoff
    }
  }
};
```

### Default Fortune Content
```javascript
const getDefaultFortune = () => {
  return `
# 今日运势

由于网络原因，无法获取个性化运势，以下是通用建议：

## 整体运势
今日宜保持乐观心态，适合进行日常工作和学习。

## 推荐摆件
![金蟾](/desk-decor/金蟾.png)
金蟾具有招财进宝的寓意，可以提升财运。

## 幸运数字
8, 6, 9

## 幸运颜色
金色、红色

## 建议
- 保持积极心态
- 与朋友保持联系
- 注意身体健康
`;
};
```

## Performance Optimization

### Response Caching
```javascript
const cacheAIResponse = async (cacheKey, response) => {
  const cacheData = {
    content: response,
    timestamp: Date.now(),
    expiresAt: Date.now() + (24 * 60 * 60 * 1000) // 24 hours
  };
  
  await redis.setex(cacheKey, 86400, JSON.stringify(cacheData));
};

const getCachedResponse = async (cacheKey) => {
  const cached = await redis.get(cacheKey);
  if (cached) {
    const data = JSON.parse(cached);
    if (data.expiresAt > Date.now()) {
      return data.content;
    }
  }
  return null;
};
```

### Rate Limiting
```javascript
const rateLimitAI = new Map();

const checkRateLimit = (userId) => {
  const now = Date.now();
  const userLimit = rateLimitAI.get(userId) || { count: 0, resetTime: now + 60000 };
  
  if (now > userLimit.resetTime) {
    userLimit.count = 0;
    userLimit.resetTime = now + 60000;
  }
  
  if (userLimit.count >= 10) { // 10 requests per minute
    throw new Error('Rate limit exceeded');
  }
  
  userLimit.count++;
  rateLimitAI.set(userId, userLimit);
};
```

## Content Quality Assurance

### Response Filtering
```javascript
const filterAIResponse = (response) => {
  // Remove potentially harmful content
  const forbiddenPatterns = [
    /死亡|疾病|灾难/g,
    /负面|消极|不幸/g
  ];
  
  let filteredResponse = response;
  forbiddenPatterns.forEach(pattern => {
    filteredResponse = filteredResponse.replace(pattern, '转运');
  });
  
  return filteredResponse;
};
```

### Content Enhancement
```javascript
const enhanceResponse = (response) => {
  // Add encouraging phrases
  const encouragingPhrases = [
    '愿您今日吉祥如意',
    '祝您好运连连',
    '愿您事事顺心'
  ];
  
  const randomPhrase = encouragingPhrases[Math.floor(Math.random() * encouragingPhrases.length)];
  return `${response}\n\n${randomPhrase} 🌟`;
};
```

## Monitoring & Analytics

### Usage Tracking
```javascript
const trackAIUsage = async (userId, requestType, responseLength) => {
  await strapi.entityService.create('api::ai-usage.ai-usage', {
    data: {
      userId,
      requestType,
      responseLength,
      timestamp: new Date(),
      cost: calculateCost(responseLength)
    }
  });
};
```

### Performance Metrics
```javascript
const measureAIPerformance = (startTime, endTime, success) => {
  const duration = endTime - startTime;
  
  console.log(`AI Request - Duration: ${duration}ms, Success: ${success}`);
  
  // Send to monitoring service
  if (global.metrics) {
    global.metrics.increment('ai.requests.total');
    global.metrics.timing('ai.requests.duration', duration);
    
    if (success) {
      global.metrics.increment('ai.requests.success');
    } else {
      global.metrics.increment('ai.requests.failure');
    }
  }
};
```

## Cultural Sensitivity Guidelines

### Language Considerations
- Use traditional Chinese terminology for astrology concepts
- Maintain respectful tone towards traditional beliefs
- Avoid overly superstitious or harmful predictions
- Include positive and constructive advice

### Cultural Accuracy
- Verify accuracy of Chinese traditional elements
- Use correct lunar calendar calculations
- Respect cultural significance of feng shui concepts
- Provide educational context when appropriate

## Testing AI Integration

### Mock AI Responses
```javascript
const mockAIResponse = {
  dailyFortune: "Mock daily fortune response",
  ornament: "金蟾",
  ornamentImage: "/desk-decor/金蟾.png",
  luckyNumbers: [8, 6, 9],
  luckyColors: ["金色", "红色"],
  advice: "Mock advice content"
};

const useMockAI = process.env.NODE_ENV === 'test';
```

### Integration Testing
```javascript
describe('AI Integration', () => {
  test('should generate valid fortune response', async () => {
    const mockUser = {
      birthDate: '1990-01-01',
      birthTime: '12:00',
      gender: 'male'
    };
    
    const response = await generateFortune(mockUser);
    
    expect(response).toContain('daily fortune');
    expect(response).toContain('feng shui ornament');
    expect(response).toContain('lucky numbers');
  });
});
``` 