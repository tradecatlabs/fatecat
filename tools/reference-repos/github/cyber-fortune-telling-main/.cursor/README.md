# Cursor AI Rules for Cyber Fortune Telling

This directory contains specialized Cursor AI rules tailored for the Cyber Fortune Telling project. These rules help the AI assistant understand the project context, architecture, and development guidelines.

## Rule Files Overview

### 📋 [project-rules.md](./project-rules.md)
**Overall project guidelines and architecture**
- Project overview and core features
- Technology stack and dependencies
- Development environment setup
- Security and deployment considerations

### 🎨 [frontend-rules.md](./frontend-rules.md)
**Next.js, React, and Material-UI specific rules**
- Component development patterns
- Material-UI best practices
- Performance optimization
- Chinese traditional calendar integration
- PWA and animation guidelines

### ⚙️ [backend-rules.md](./backend-rules.md)
**Strapi CMS and Node.js backend rules**
- API development patterns
- Database management (PostgreSQL/SQLite)
- Authentication and security
- Performance optimization
- Error handling and logging

### 🤖 [ai-integration-rules.md](./ai-integration-rules.md)
**AI integration and prompt engineering**
- DeepSeek API configuration
- Prompt engineering for fortune telling
- Chinese traditional elements integration
- Response processing and validation
- Cultural sensitivity guidelines

### 🐳 [docker-deployment-rules.md](./docker-deployment-rules.md)
**Containerization and deployment guidelines**
- Docker Compose configuration
- Environment management
- Security and monitoring
- Backup and recovery strategies
- Production deployment practices

## How to Use These Rules

### 1. Main Configuration
The primary `.cursorrules` file in the project root references these specialized rules and provides a comprehensive overview for the AI assistant.

### 2. Context-Aware Development
When working on specific parts of the project, the AI will automatically apply the relevant rules:
- Frontend work → `frontend-rules.md`
- Backend development → `backend-rules.md`
- AI integration → `ai-integration-rules.md`
- Deployment tasks → `docker-deployment-rules.md`

### 3. Cultural Sensitivity
Special attention is given to Chinese traditional elements throughout all rules, ensuring culturally appropriate:
- Lunar calendar calculations
- Ba Zi (Eight Characters) analysis
- Feng shui ornament recommendations
- Traditional terminology usage

## Key Features Covered

### 🔮 Fortune Telling Logic
- Birth chart analysis using Chinese astrology
- Daily fortune generation with AI
- Personalized recommendations
- Cultural context integration

### 🎯 AI Integration
- DeepSeek API integration patterns
- Prompt engineering best practices
- Error handling and fallback strategies
- Response validation and processing

### 🏗️ Architecture
- Full-stack Next.js + Strapi setup
- PostgreSQL database management
- Docker containerization
- PWA capabilities

### 🎨 User Experience
- Material-UI component patterns
- Framer Motion animations
- Responsive design principles
- Accessibility considerations

## Development Workflow

### 1. Setup
```bash
# Copy environment template
cp example.env .env

# Start development environment
docker-compose up -d
```

### 2. Development
- Frontend: `cd frontend && pnpm dev`
- Backend: `cd backend && npm run dev`
- Database: Access via Docker Compose

### 3. Testing
- Unit tests for utilities
- Component testing
- API integration testing
- AI functionality testing

## Best Practices Enforced

### Code Quality
- TypeScript usage where applicable
- Proper error handling
- Performance optimization
- Security considerations

### Cultural Sensitivity
- Respectful handling of traditional beliefs
- Accurate lunar calendar calculations
- Appropriate feng shui representations
- Educational context provision

### AI Integration
- Robust prompt engineering
- Fallback mechanisms
- Response validation
- Rate limiting and caching

## Troubleshooting

### Common Issues
1. **AI API failures**: Check API keys and rate limits
2. **Database connection**: Verify Docker containers are running
3. **Port conflicts**: Ensure ports 4000 and 1337 are available
4. **Environment variables**: Verify all required variables are set

### Debug Commands
```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs -f [service-name]

# Access database
docker-compose exec database psql -U strapi -d fortune_telling
```

## Contributing

When adding new rules or modifying existing ones:

1. **Maintain consistency** with existing patterns
2. **Include practical examples** with code snippets
3. **Consider cultural sensitivity** for Chinese elements
4. **Update the main `.cursorrules`** file if needed
5. **Test the rules** with actual development scenarios

## Support

For issues or questions about these rules:
- Check the project's main README.md
- Review the example.env file for configuration
- Consult the Docker Compose logs for runtime issues
- Open an issue on the project repository

---

*These rules are designed to help Cursor AI provide contextually appropriate assistance for the Cyber Fortune Telling project, balancing technical excellence with cultural sensitivity.* 