import { Link, useLocation } from 'react-router-dom';
import { 
  Home, 
  Search, 
  Bell, 
  MessageCircle, 
  User, 
  Bookmark,
  TrendingUp,
  Users,
  Hash
} from 'lucide-react';
import { useAuthStore } from '../../stores/authStore';
import { Button } from '../ui/button';
import { cn } from '../../utils/cn';

const navigationItems = [
  {
    name: 'Home',
    href: '/',
    icon: Home,
  },
  {
    name: 'Explore',
    href: '/explore',
    icon: Search,
  },
  {
    name: 'Notifications',
    href: '/notifications',
    icon: Bell,
  },
  {
    name: 'Messages',
    href: '/messages',
    icon: MessageCircle,
  },
  {
    name: 'Bookmarks',
    href: '/bookmarks',
    icon: Bookmark,
  },
  {
    name: 'Profile',
    href: '/profile',
    icon: User,
  },
];

const trendingItems = [
  { name: 'Technology', count: '125K posts' },
  { name: 'Photography', count: '89K posts' },
  { name: 'Travel', count: '67K posts' },
  { name: 'Food', count: '45K posts' },
  { name: 'Music', count: '34K posts' },
];

const suggestedUsers = [
  { username: 'johndoe', displayName: 'John Doe', avatar: null },
  { username: 'janesmth', displayName: 'Jane Smith', avatar: null },
  { username: 'mikejones', displayName: 'Mike Jones', avatar: null },
];

export const Sidebar = () => {
  const location = useLocation();
  const { user } = useAuthStore();

  return (
    <aside className="hidden lg:flex lg:w-80 lg:flex-col lg:fixed lg:inset-y-0 lg:pt-16">
      <div className="flex flex-col flex-1 min-h-0 border-r bg-background">
        <div className="flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
          <div className="flex items-center flex-shrink-0 px-4">
            <nav className="flex-1 space-y-1">
              {navigationItems.map((item) => {
                const href = item.href === '/profile' ? `/profile/${user?.username}` : item.href;
                const isActive = location.pathname === href || 
                  (item.href === '/' && location.pathname === '/');
                
                return (
                  <Link
                    key={item.name}
                    to={href}
                    className={cn(
                      'group flex items-center px-2 py-3 text-sm font-medium rounded-md transition-colors',
                      isActive
                        ? 'bg-primary text-primary-foreground'
                        : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
                    )}
                  >
                    <item.icon
                      className={cn(
                        'mr-3 flex-shrink-0 h-5 w-5',
                        isActive ? 'text-primary-foreground' : 'text-muted-foreground'
                      )}
                    />
                    {item.name}
                  </Link>
                );
              })}
            </nav>
          </div>

          {/* Trending Section */}
          <div className="mt-8 px-4">
            <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider mb-3">
              Trending
            </h3>
            <div className="space-y-2">
              {trendingItems.map((item) => (
                <Link
                  key={item.name}
                  to={`/explore?hashtag=${item.name.toLowerCase()}`}
                  className="flex items-center justify-between p-2 rounded-md hover:bg-accent transition-colors"
                >
                  <div className="flex items-center">
                    <Hash className="h-4 w-4 text-muted-foreground mr-2" />
                    <span className="text-sm font-medium">{item.name}</span>
                  </div>
                  <span className="text-xs text-muted-foreground">{item.count}</span>
                </Link>
              ))}
            </div>
          </div>

          {/* Suggested Users */}
          <div className="mt-8 px-4">
            <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider mb-3">
              Suggested for you
            </h3>
            <div className="space-y-3">
              {suggestedUsers.map((suggestedUser) => (
                <div key={suggestedUser.username} className="flex items-center justify-between">
                  <Link
                    to={`/profile/${suggestedUser.username}`}
                    className="flex items-center space-x-3 hover:bg-accent p-2 rounded-md transition-colors flex-1"
                  >
                    <div className="h-8 w-8 rounded-full bg-muted flex items-center justify-center">
                      <User className="h-4 w-4 text-muted-foreground" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium truncate">
                        {suggestedUser.displayName}
                      </p>
                      <p className="text-xs text-muted-foreground truncate">
                        @{suggestedUser.username}
                      </p>
                    </div>
                  </Link>
                  <Button size="sm" variant="outline" className="ml-2">
                    Follow
                  </Button>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
};
