import { useState } from 'react';
import { Link } from 'react-router-dom';
import { formatDistanceToNow } from 'date-fns';
import { 
  Heart, 
  MessageCircle, 
  Share, 
  Bookmark, 
  MoreHorizontal,
  Verified
} from 'lucide-react';
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
import { Avatar, AvatarFallback, AvatarImage } from '../ui/avatar';
import { Button } from '../ui/button';
import { Card, CardContent } from '../ui/card';
import * as DropdownMenu from '@radix-ui/react-dropdown-menu';
import { cn } from '../../utils/cn';

interface PostCardProps {
  post: Post;
}

export const PostCard = ({ post }: PostCardProps) => {
  const [isLiked, setIsLiked] = useState(post.isLiked);
  const [isBookmarked, setIsBookmarked] = useState(post.isBookmarked);
  const [likesCount, setLikesCount] = useState(post.likesCount);

  const handleLike = () => {
    setIsLiked(!isLiked);
    setLikesCount(prev => isLiked ? prev - 1 : prev + 1);
    // TODO: API call to like/unlike post
  };

  const handleBookmark = () => {
    setIsBookmarked(!isBookmarked);
    // TODO: API call to bookmark/unbookmark post
  };

  const handleShare = () => {
    // TODO: Implement share functionality
    navigator.clipboard.writeText(`${window.location.origin}/post/${post.id}`);
  };

  const formatContent = (content: string) => {
    // Simple hashtag and mention formatting
    return content
      .split(' ')
      .map((word, index) => {
        if (word.startsWith('#')) {
          return (
            <Link
              key={index}
              to={`/explore?hashtag=${word.slice(1)}`}
              className="text-primary hover:underline"
            >
              {word}
            </Link>
          );
        }
        if (word.startsWith('@')) {
          return (
            <Link
              key={index}
              to={`/profile/${word.slice(1)}`}
              className="text-primary hover:underline"
            >
              {word}
            </Link>
          );
        }
        return word;
      })
      .reduce((acc, word, index) => {
        if (index === 0) return [word];
        return [...acc, ' ', word];
      }, [] as React.ReactNode[]);
  };

  return (
    <Card className="w-full">
      <CardContent className="p-6">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center space-x-3">
            <Link to={`/profile/${post.author.username}`}>
              <Avatar className="h-10 w-10">
                <AvatarImage src={post.author.avatar} alt={post.author.displayName} />
                <AvatarFallback>
                  {post.author.displayName.charAt(0).toUpperCase()}
                </AvatarFallback>
              </Avatar>
            </Link>
            <div>
              <div className="flex items-center space-x-1">
                <Link
                  to={`/profile/${post.author.username}`}
                  className="font-semibold hover:underline"
                >
                  {post.author.displayName}
                </Link>
                {post.author.verified && (
                  <Verified className="h-4 w-4 text-primary fill-current" />
                )}
              </div>
              <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                <span>@{post.author.username}</span>
                <span>·</span>
                <Link
                  to={`/post/${post.id}`}
                  className="hover:underline"
                >
                  {formatDistanceToNow(new Date(post.createdAt), { addSuffix: true })}
                </Link>
              </div>
            </div>
          </div>

          {/* More Options */}
          <DropdownMenu.Root>
            <DropdownMenu.Trigger asChild>
              <Button variant="ghost" size="icon" className="h-8 w-8">
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </DropdownMenu.Trigger>
            <DropdownMenu.Portal>
              <DropdownMenu.Content
                className="min-w-[160px] bg-popover text-popover-foreground rounded-md border shadow-md p-1 z-50"
                align="end"
              >
                <DropdownMenu.Item className="flex items-center px-3 py-2 text-sm rounded-sm hover:bg-accent hover:text-accent-foreground cursor-pointer outline-none">
                  Copy link
                </DropdownMenu.Item>
                <DropdownMenu.Item className="flex items-center px-3 py-2 text-sm rounded-sm hover:bg-accent hover:text-accent-foreground cursor-pointer outline-none">
                  Report post
                </DropdownMenu.Item>
              </DropdownMenu.Content>
            </DropdownMenu.Portal>
          </DropdownMenu.Root>
        </div>

        {/* Content */}
        <div className="mb-4">
          <p className="text-foreground whitespace-pre-wrap leading-relaxed">
            {formatContent(post.content)}
          </p>
        </div>

        {/* Images */}
        {post.images && post.images.length > 0 && (
          <div className="mb-4">
            <div className={cn(
              "grid gap-2 rounded-lg overflow-hidden",
              post.images.length === 1 ? "grid-cols-1" : "grid-cols-2"
            )}>
              {post.images.map((image, index) => (
                <img
                  key={index}
                  src={image}
                  alt={`Post image ${index + 1}`}
                  className="w-full h-auto object-cover max-h-96"
                />
              ))}
            </div>
          </div>
        )}

        {/* Actions */}
        <div className="flex items-center justify-between pt-2 border-t">
          <div className="flex items-center space-x-6">
            {/* Like */}
            <div className="flex items-center space-x-2">
              <Button
                variant="ghost"
                size="sm"
                onClick={handleLike}
                className={cn(
                  "h-8 px-2",
                  isLiked ? "text-red-500 hover:text-red-600" : "text-muted-foreground"
                )}
              >
                <Heart className={cn("h-4 w-4 mr-1", isLiked && "fill-current")} />
                {likesCount}
              </Button>
            </div>

            {/* Comment */}
            <div className="flex items-center space-x-2">
              <Button
                variant="ghost"
                size="sm"
                asChild
                className="h-8 px-2 text-muted-foreground"
              >
                <Link to={`/post/${post.id}`}>
                  <MessageCircle className="h-4 w-4 mr-1" />
                  {post.commentsCount}
                </Link>
              </Button>
            </div>

            {/* Share */}
            <div className="flex items-center space-x-2">
              <Button
                variant="ghost"
                size="sm"
                onClick={handleShare}
                className="h-8 px-2 text-muted-foreground"
              >
                <Share className="h-4 w-4 mr-1" />
                {post.sharesCount}
              </Button>
            </div>
          </div>

          {/* Bookmark */}
          <Button
            variant="ghost"
            size="sm"
            onClick={handleBookmark}
            className={cn(
              "h-8 px-2",
              isBookmarked ? "text-primary" : "text-muted-foreground"
            )}
          >
            <Bookmark className={cn("h-4 w-4", isBookmarked && "fill-current")} />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};
