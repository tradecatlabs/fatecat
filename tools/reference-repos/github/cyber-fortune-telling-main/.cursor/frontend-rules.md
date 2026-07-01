# Frontend Development Rules - Next.js + React + Material-UI

## Framework Standards
- **Next.js 15.1.7**: Use latest Next.js features including App Router when applicable
- **React 19.0.0**: Utilize React hooks, functional components, and modern patterns
- **Material-UI 7.1.0**: Follow Material Design principles and MUI component usage
- **Framer Motion 12.9.4**: Implement smooth animations and transitions

## Component Structure
```
frontend/
├── components/         # Reusable UI components
├── pages/             # Next.js pages (using Pages Router)
├── styles/            # Global styles and theme configuration
├── tools/             # Utility functions and helpers
└── public/           # Static assets
```

## Code Style Guidelines

### Component Development
- Use functional components with hooks
- Implement proper TypeScript types when available
- Follow React best practices for state management
- Use Material-UI components consistently
- Implement proper error boundaries

### File Naming
- Use PascalCase for component files: `FortuneMasterAvatar.js`
- Use camelCase for utility files: `getChineseTraditionalTime.js`
- Use kebab-case for CSS modules: `fortune_telling_uid.module.css`

### Import Organization
```javascript
// React and Next.js imports
import { useEffect, useState } from "react";
import axios from "axios";

// Material-UI imports
import { Button, Card, Typography, Box } from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";

// Local imports
import styles from "@/styles/Markdown.module.css";
import converter from "@/tools/converter";
```

## Key Features Implementation

### Chinese Traditional Calendar
- Use `lunar-javascript` for lunar calendar calculations
- Implement `getChineseTraditionalDate` and `getChineseTraditionalTime`
- Support zodiac animals and traditional elements
- Handle timezone conversions properly

### AI Chat Integration
- Use `ChatInput` component for user interactions
- Implement `ChatMarkdownStack` for message display
- Handle AI response parsing and formatting
- Support markdown rendering with `StyledMarkdown`

### Animation and Visual Effects
- Use Framer Motion for smooth transitions
- Implement feng shui ornament animations
- Create engaging loading states
- Add visual feedback for user interactions

### PWA Support
- Configure `next-pwa` for offline functionality
- Implement proper service worker registration
- Add manifest.json for installable app
- Handle offline state gracefully

## Material-UI Best Practices

### Theme Configuration
```javascript
// Use centralized theme configuration
import { ThemeProvider } from '@mui/material/styles';
import theme from '@/styles/theme';

// Apply theme consistently
<ThemeProvider theme={theme}>
  <CssBaseline />
  <Component {...pageProps} />
</ThemeProvider>
```

### Component Usage
- Use MUI's responsive breakpoints
- Implement proper spacing with Box and Stack
- Use Typography for consistent text styling
- Apply elevation and shadows appropriately

### Form Handling
- Use TextField for input fields
- Implement RadioGroup for selections
- Add proper validation and error states
- Use IconButton for interactive elements

## Performance Optimization

### Image Optimization
- Use Next.js Image component for automatic optimization
- Implement lazy loading for images
- Use appropriate image formats (WebP, AVIF)
- Optimize asset loading for feng shui ornaments

### Bundle Optimization
- Use dynamic imports for large components
- Implement code splitting at route level
- Minimize bundle size with tree shaking
- Use Next.js analyzer for bundle analysis

### Loading States
- Implement skeleton screens for better UX
- Use loading indicators for AI responses
- Handle async operations gracefully
- Provide meaningful error messages

## Responsive Design

### Mobile-First Approach
- Design for mobile devices first
- Use MUI's breakpoint system
- Implement touch-friendly interactions
- Optimize for various screen sizes

### Accessibility
- Use semantic HTML elements
- Implement proper ARIA labels
- Ensure keyboard navigation
- Maintain color contrast ratios

## Environment Integration

### API Configuration
```javascript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:11337";
const API_TOKEN = process.env.NEXT_PUBLIC_API_TOKEN || "";
```

### Error Handling
- Implement try-catch blocks for API calls
- Use Material-UI Alert for error display
- Provide user-friendly error messages
- Log errors appropriately for debugging

## Testing Considerations
- Write unit tests for utility functions
- Test component rendering and interactions
- Mock API calls for consistent testing
- Ensure accessibility compliance

## Deployment
- Use Docker for consistent deployment
- Implement proper build optimization
- Configure environment variables
- Set up health checks for frontend service 