# PostIt - Pure Frontend Social Media App

A modern, minimalistic social media **frontend-only** application built with React 18, TypeScript, and the latest web technologies. **No backend required** - everything runs locally with mock data!

## Features

### Frontend-Only Features
- **Authentication System**: Login/register with local storage (demo: demo@example.com / password)
- **Modern UI**: Clean, minimalistic design with dark/light mode toggle
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Home Feed**: Infinite scrolling posts with create post functionality
- **Post Creation**: Create posts with images, hashtags, mentions
- **Post Interactions**: Like, comment, share, bookmark (local state)
- **User Profiles**: Profile pages with user information and posts
- **Explore Page**: Trending hashtags and user suggestions
- **Navigation**: Sidebar navigation with protected routes
- **State Management**: Zustand for global state management (no API calls)
- **Theme System**: Dark/light mode toggle with persistence
- **Mock Data**: Realistic mock data for all features
- **Local Storage**: All data persisted locally

### Perfect For
- Frontend development and testing
- UI/UX prototyping
- Learning React best practices
- Demos and presentations
- No backend setup required!

## Tech Stack

- **React 18** - Latest React with concurrent features
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Radix UI** - Accessible component primitives
- **React Router v6** - Client-side routing
- **Zustand** - Lightweight state management
- **React Query** - Server state management
- **React Hook Form** - Form handling with validation
- **Zod** - Schema validation
- **Axios** - HTTP client with interceptors
- **Framer Motion** - Animation library (ready to use)
- **React Hot Toast** - Toast notifications

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd post-it/frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Update the `.env` file with your configuration:
   ```env
   VITE_API_BASE_URL=http://localhost:8000/api
   VITE_APP_NAME=PostIt
   VITE_APP_VERSION=1.0.0
   VITE_ENABLE_DEV_TOOLS=true
   ```

4. **Start the development server**
   ```bash
   npm run dev
   ```

5. **Open your browser**
   Navigate to `http://localhost:5173`

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── ui/             # Base UI components (Button, Input, etc.)
│   ├── layout/         # Layout components (Navbar, Sidebar, etc.)
│   ├── auth/           # Authentication components
│   ├── posts/          # Post-related components
│   ├── profile/        # Profile components
│   ├── messaging/      # Messaging components
│   └── notifications/  # Notification components
├── pages/              # Page components
│   ├── auth/           # Authentication pages
│   ├── profile/        # Profile pages
│   ├── posts/          # Post pages
│   ├── messaging/      # Messaging pages
│   ├── notifications/  # Notification pages
│   └── explore/        # Explore pages
├── hooks/              # Custom React hooks
├── stores/             # Zustand stores
├── services/           # API services and configuration
├── types/              # TypeScript type definitions
├── utils/              # Utility functions
└── App.tsx             # Main App component
```

## Design System

The application uses a modern design system with:

- **Color Scheme**: CSS custom properties for theming
- **Typography**: System font stack with proper hierarchy
- **Spacing**: Consistent spacing scale
- **Components**: Reusable, accessible components
- **Animations**: Smooth transitions and micro-interactions

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

## Deployment

1. **Build the application**
   ```bash
   npm run build
   ```

2. **Preview the build**
   ```bash
   npm run preview
   ```

3. **Deploy to your hosting platform**
   The `dist` folder contains the production-ready files.

## Authentication Flow

The application includes a complete authentication system:

1. **Protected Routes**: Automatic redirection based on auth state
2. **Token Management**: Automatic token refresh and error handling
3. **Persistent Sessions**: Auth state persisted across browser sessions
4. **Form Validation**: Comprehensive form validation with Zod schemas

## Responsive Design

- **Mobile First**: Designed for mobile devices first
- **Breakpoints**: Responsive design for all screen sizes
- **Touch Friendly**: Optimized for touch interactions
- **Accessibility**: ARIA labels and keyboard navigation

## Performance Features

- **Code Splitting**: Lazy loading for routes
- **Image Optimization**: Lazy loading and optimization ready
- **Bundle Analysis**: Optimized bundle size
- **Caching**: Intelligent caching strategies with React Query

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

Built using modern web technologies