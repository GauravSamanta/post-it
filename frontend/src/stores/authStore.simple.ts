import { create } from 'zustand';

// Define types inline to avoid import issues
interface User {
  id: string;
  username: string;
  email: string;
  displayName: string;
  avatar?: string;
  bio?: string;
  verified: boolean;
  followersCount: number;
  followingCount: number;
  postsCount: number;
  createdAt: string;
  updatedAt: string;
}

interface LoginCredentials {
  email: string;
  password: string;
}

interface RegisterCredentials {
  email: string;
  username: string;
  password: string;
  confirmPassword: string;
  displayName: string;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

interface AuthActions {
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (credentials: RegisterCredentials) => Promise<void>;
  logout: () => void;
  updateUser: (userData: Partial<User>) => void;
  clearError: () => void;
  checkAuth: () => void;
}

type AuthStore = AuthState & AuthActions;

// Mock users for demo
const mockUsers = [
  {
    id: '1',
    username: 'demo',
    email: 'demo@example.com',
    displayName: 'Demo User',
    avatar: null,
    bio: 'This is a demo user for the frontend application',
    verified: true,
    followersCount: 1250,
    followingCount: 340,
    postsCount: 89,
    createdAt: '2024-01-15T10:00:00Z',
    updatedAt: '2024-01-15T10:00:00Z',
  },
];

export const useAuthStore = create<AuthStore>((set, get) => ({
  // Initial state
  user: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,

  // Actions
  login: async (credentials: LoginCredentials) => {
    set({ isLoading: true, error: null });
    
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Simple validation for demo
    if (credentials.email === 'demo@example.com' && credentials.password === 'password') {
      const user = mockUsers[0];
      
      // Store in localStorage
      localStorage.setItem('user', JSON.stringify(user));
      localStorage.setItem('isAuthenticated', 'true');
      
      set({
        user,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      });
    } else {
      set({
        isLoading: false,
        error: 'Invalid email or password. Try demo@example.com / password',
      });
      throw new Error('Invalid credentials');
    }
  },

  register: async (credentials: RegisterCredentials) => {
    set({ isLoading: true, error: null });
    
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Create new user from registration data
    const newUser: User = {
      id: Date.now().toString(),
      username: credentials.username,
      email: credentials.email,
      displayName: credentials.displayName,
      avatar: null,
      bio: null,
      verified: false,
      followersCount: 0,
      followingCount: 0,
      postsCount: 0,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    
    // Store in localStorage
    localStorage.setItem('user', JSON.stringify(newUser));
    localStorage.setItem('isAuthenticated', 'true');
    
    set({
      user: newUser,
      isAuthenticated: true,
      isLoading: false,
      error: null,
    });
  },

  logout: () => {
    localStorage.removeItem('user');
    localStorage.removeItem('isAuthenticated');
    
    set({
      user: null,
      isAuthenticated: false,
      error: null,
    });
  },

  updateUser: (userData: Partial<User>) => {
    const currentUser = get().user;
    if (currentUser) {
      const updatedUser = { ...currentUser, ...userData };
      localStorage.setItem('user', JSON.stringify(updatedUser));
      set({
        user: updatedUser,
      });
    }
  },

  clearError: () => {
    set({ error: null });
  },

  checkAuth: () => {
    // Check localStorage for existing auth
    const storedUser = localStorage.getItem('user');
    const storedAuth = localStorage.getItem('isAuthenticated');
    
    if (storedUser && storedAuth === 'true') {
      try {
        const user = JSON.parse(storedUser);
        set({
          user,
          isAuthenticated: true,
          isLoading: false,
        });
      } catch (error) {
        // Clear invalid data
        localStorage.removeItem('user');
        localStorage.removeItem('isAuthenticated');
        set({
          user: null,
          isAuthenticated: false,
          isLoading: false,
        });
      }
    } else {
      set({
        user: null,
        isAuthenticated: false,
        isLoading: false,
      });
    }
  },
}));
