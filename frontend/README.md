# Frontend Setup Guide

## Installation Steps

### 1. Install Node.js Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Create `.env.local` file:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### 3. Run Development Server

```bash
npm run dev
```

Frontend will be available at: http://localhost:3000

## Project Structure

```
frontend/
├── app/                    # Next.js 14 App Router
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Landing page
│   ├── globals.css        # Global styles
│   ├── auth/              # Authentication pages
│   │   ├── login/
│   │   └── signup/
│   ├── onboarding/        # Onboarding flow
│   ├── dashboard/         # Main dashboard
│   ├── universities/      # University discovery
│   ├── counselor/         # AI Counselor chat
│   └── profile/           # Profile management
├── lib/                   # Utilities
│   ├── api.ts            # API client
│   ├── store.ts          # Zustand store
│   └── types.ts          # TypeScript types
├── components/           # Reusable components
├── public/              # Static assets
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── next.config.js
```

## Available Scripts

```bash
# Development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Lint code
npm run lint
```

## Key Technologies

- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Zustand**: Lightweight state management
- **Axios**: HTTP client for API calls

## Features Implementation

### Authentication
- JWT token stored in localStorage
- Protected routes redirect to login
- Auto-redirect authenticated users

### Onboarding
- 4-step wizard
- Form validation
- Progress indicator
- Auto-save on completion

### Dashboard
- Real-time data from API
- Profile strength visualization
- Task management
- Quick actions

### University Discovery
- Filter and search
- Category badges (Dream/Target/Safe)
- Shortlist functionality
- Lock/unlock universities

### AI Counselor
- Real-time chat interface
- Message history
- Context-aware responses
- Action indicators

## Styling

The project uses Tailwind CSS with a custom color palette:

```javascript
// tailwind.config.js
theme: {
  extend: {
    colors: {
      primary: {
        50-900: // Blue color scale
      },
    },
  },
}
```

## State Management

Using Zustand for global state:

```typescript
// lib/store.ts
export const useAuthStore = create((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,
  login: (user, token) => { /* ... */ },
  logout: () => { /* ... */ },
}));
```

## API Integration

All API calls are centralized in `lib/api.ts`:

```typescript
import { authAPI, dashboardAPI, universitiesAPI } from '@/lib/api';

// Usage
const response = await authAPI.login(credentials);
const dashboard = await dashboardAPI.get();
```

## Common Issues

### API Connection Failed
- Ensure backend is running on http://localhost:8000
- Check NEXT_PUBLIC_API_URL in .env.local
- Verify CORS settings in backend

### Build Errors
```bash
# Clear Next.js cache
rm -rf .next
npm run build
```

### TypeScript Errors
```bash
# Check types
npx tsc --noEmit
```

## Production Deployment

### Vercel (Recommended)

1. Push code to GitHub
2. Import project in Vercel
3. Add environment variable: `NEXT_PUBLIC_API_URL`
4. Deploy

### Manual Build

```bash
npm run build
npm start
```

## Environment Variables

- `NEXT_PUBLIC_API_URL`: Backend API URL (must start with NEXT_PUBLIC_ to be accessible in browser)

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Performance

- Code splitting with Next.js
- Image optimization
- CSS purging with Tailwind
- Client-side caching with Zustand persist

## Accessibility

- Semantic HTML
- ARIA labels
- Keyboard navigation
- Focus management

## Development Tips

1. Use React DevTools for debugging
2. Install Tailwind CSS IntelliSense extension
3. Enable TypeScript strict mode
4. Use Next.js Image component for images
5. Leverage Next.js API routes if needed
