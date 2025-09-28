import { useState, useEffect } from 'react';
import { PostCard } from '../components/posts/PostCard';
import { CreatePostCard } from '../components/posts/CreatePostCard';
import { Button } from '../components/ui/button';
import { Loader2, RefreshCw } from 'lucide-react';
// Define Post type inline to avoid import issues
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

interface Post {
  id: string;
  content: string;
  images?: string[];
  videos?: string[];
  author: User;
  likesCount: number;
  commentsCount: number;
  sharesCount: number;
  isLiked: boolean;
  isBookmarked: boolean;
  createdAt: string;
  updatedAt: string;
  hashtags: string[];
  mentions: string[];
}

// Mock data for development
const mockPosts: Post[] = [
  {
    id: '1',
    content: 'Just built an amazing React app with TypeScript! The developer experience is incredible. #react #typescript #webdev',
    images: [],
    videos: [],
    author: {
      id: '1',
      username: 'johndoe',
      email: 'john@example.com',
      displayName: 'John Doe',
      avatar: null,
      bio: 'Full-stack developer passionate about React and TypeScript',
      verified: true,
      followersCount: 1250,
      followingCount: 340,
      postsCount: 89,
      createdAt: '2024-01-15T10:00:00Z',
      updatedAt: '2024-01-15T10:00:00Z',
    },
    likesCount: 42,
    commentsCount: 8,
    sharesCount: 3,
    isLiked: false,
    isBookmarked: false,
    createdAt: '2024-01-20T14:30:00Z',
    updatedAt: '2024-01-20T14:30:00Z',
    hashtags: ['react', 'typescript', 'webdev'],
    mentions: [],
  },
  {
    id: '2',
    content: 'Beautiful sunset from my balcony today! Nature never fails to amaze me.',
    images: ['https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=500&h=300&fit=crop'],
    videos: [],
    author: {
      id: '2',
      username: 'janesmth',
      email: 'jane@example.com',
      displayName: 'Jane Smith',
      avatar: null,
      bio: 'Photography enthusiast and nature lover',
      verified: false,
      followersCount: 890,
      followingCount: 420,
      postsCount: 156,
      createdAt: '2024-01-10T08:00:00Z',
      updatedAt: '2024-01-10T08:00:00Z',
    },
    likesCount: 127,
    commentsCount: 15,
    sharesCount: 8,
    isLiked: true,
    isBookmarked: true,
    createdAt: '2024-01-20T18:45:00Z',
    updatedAt: '2024-01-20T18:45:00Z',
    hashtags: [],
    mentions: [],
  },
];

export const HomePage = () => {
  const [posts, setPosts] = useState<Post[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);

  // Generate more mock posts
  const generateMockPosts = (pageNum: number, pageSize: number = 10) => {
    return Array.from({ length: pageSize }, (_, i) => ({
      ...mockPosts[i % mockPosts.length],
      id: `${pageNum}-${i}`,
      content: `${mockPosts[i % mockPosts.length].content} (Post #${(pageNum - 1) * pageSize + i + 1})`,
    }));
  };

  // Initial load
  useEffect(() => {
    const loadInitialPosts = async () => {
      setIsLoading(true);
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      const initialPosts = generateMockPosts(1);
      setPosts(initialPosts);
      setIsLoading(false);
    };
    
    loadInitialPosts();
  }, []);

  const handleRefresh = async () => {
    setRefreshing(true);
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    const refreshedPosts = generateMockPosts(1);
    setPosts(refreshedPosts);
    setPage(1);
    setHasMore(true);
    setRefreshing(false);
  };

  const loadMore = async () => {
    if (loadingMore || !hasMore) return;
    
    setLoadingMore(true);
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    const nextPage = page + 1;
    const newPosts = generateMockPosts(nextPage);
    setPosts(prev => [...prev, ...newPosts]);
    setPage(nextPage);
    
    // Simulate end of data after 5 pages
    if (nextPage >= 5) {
      setHasMore(false);
    }
    
    setLoadingMore(false);
  };

  const addNewPost = (newPost: Post) => {
    setPosts(prev => [newPost, ...prev]);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-6 lg:ml-80">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Home</h1>
        <Button
          variant="ghost"
          size="icon"
          onClick={handleRefresh}
          disabled={refreshing}
          className="h-9 w-9"
        >
          <RefreshCw className={`h-4 w-4 ${refreshing ? 'animate-spin' : ''}`} />
        </Button>
      </div>

      {/* Create Post Card */}
      <div className="mb-6">
        <CreatePostCard onPostCreated={addNewPost} />
      </div>

      {/* Posts Feed */}
      <div className="space-y-6">
        {posts.map((post) => (
          <PostCard key={post.id} post={post} />
        ))}
      </div>

      {/* Load More Button */}
      {hasMore && (
        <div className="flex justify-center mt-8">
          <Button
            onClick={loadMore}
            disabled={loadingMore}
            variant="outline"
          >
            {loadingMore ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Loading...
              </>
            ) : (
              'Load More'
            )}
          </Button>
        </div>
      )}

      {/* End of Feed Message */}
      {!hasMore && posts.length > 0 && (
        <div className="text-center mt-8 py-8 border-t">
          <p className="text-muted-foreground">You've reached the end of your feed</p>
          <Button
            onClick={handleRefresh}
            variant="ghost"
            className="mt-2"
            disabled={refreshing}
          >
            {refreshing ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Refreshing...
              </>
            ) : (
              'Refresh Feed'
            )}
          </Button>
        </div>
      )}
    </div>
  );
};
