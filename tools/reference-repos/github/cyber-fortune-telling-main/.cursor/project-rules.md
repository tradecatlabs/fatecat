# Cyber Fortune Telling Project Rules

## Project Overview
This is a full-stack AI-powered fortune telling application called "Cyber Fortune Telling" (基于大模型的风水算命摆件). The project provides digital feng shui ornaments and fortune telling services using large language models.

## Tech Stack
- **Frontend**: Next.js 15.1.7, React 19.0.0, Material-UI 7.1.0, Framer Motion 12.9.4
- **Backend**: Strapi 5.10.3, Node.js 22.14.0+
- **Database**: PostgreSQL 17.5 (production), SQLite3 (development)
- **AI Integration**: OpenAI API (DeepSeek), IntelliNode
- **Deployment**: Docker Compose
- **Additional**: PWA support, Lunar JavaScript, Moment.js, MQTT

## Architecture
```
cyber-fortune-telling/
├── frontend/          # Next.js application (port 4000)
├── backend/           # Strapi CMS 
├── docker-compose.yml # Container orchestration
└── example.env        # Environment template
```

## Core Features
1. **User Registration & Birth Chart**: Users input birth date/time for Chinese astrology calculations
2. **Daily Fortune Updates**: AI-generated fortune telling with feng shui ornament recommendations
3. **Interactive Chat**: Real-time AI conversation with fortune telling context
4. **Digital Ornaments**: Animated feng shui decorations with visual effects
5. **Multi-Theme Support**: Various color themes for different aesthetics
6. **PWA Capabilities**: Installable progressive web app
7. **Chinese Calendar Integration**: Traditional lunar calendar support
8. **Auto-refresh**: Daily fortune updates at midnight

## Development Guidelines

### Code Style
- Use TypeScript for type safety where possible
- Follow React hooks patterns and functional components
- Implement proper error handling and loading states
- Use Material-UI design system consistently
- Maintain responsive design for mobile-first approach

### API Integration
- Use Strapi for backend API management
- Implement proper authentication and authorization
- Handle AI API rate limits and failures gracefully
- Use environment variables for sensitive configuration

### Performance
- Optimize images and animations
- Implement lazy loading for components
- Use Next.js optimization features (Image, dynamic imports)
- Minimize bundle size and improve loading times

### AI Integration
- Use DeepSeek API as primary AI provider
- Implement fallback strategies for AI failures
- Create comprehensive prompts for fortune telling context
- Handle AI response parsing and formatting

### Chinese Cultural Context
- Respect traditional Chinese astrology and feng shui concepts
- Use appropriate lunar calendar calculations
- Implement proper zodiac animal and element systems
- Maintain cultural sensitivity in AI prompt design

## Environment Setup
- Node.js 22.14.0+ required
- Use pnpm for package management
- Docker Compose for containerized deployment
- PostgreSQL for production database

## Security Considerations
- Secure API keys and JWT secrets
- Implement proper user authentication
- Sanitize user inputs
- Use HTTPS in production
- Validate all AI-generated content

## Deployment
- Use Docker containers for consistent deployment
- Implement health checks for all services
- Use environment variables for configuration
- Set up proper logging and monitoring 