import { useState, useRef } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Image, Video, Smile, X, Loader2 } from 'lucide-react';
import { useAuthStore } from '../../stores/authStore';
import { Avatar, AvatarFallback, AvatarImage } from '../ui/avatar';
import { Button } from '../ui/button';
import { Card, CardContent } from '../ui/card';
import { toast } from 'react-hot-toast';
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

const createPostSchema = z.object({
  content: z.string().min(1, 'Post cannot be empty').max(280, 'Post cannot exceed 280 characters'),
});

type CreatePostFormData = z.infer<typeof createPostSchema>;

interface CreatePostCardProps {
  onPostCreated?: (post: Post) => void;
}

export const CreatePostCard = ({ onPostCreated }: CreatePostCardProps) => {
  const [selectedImages, setSelectedImages] = useState<File[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { user } = useAuthStore();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const {
    register,
    handleSubmit,
    watch,
    reset,
    formState: { errors },
  } = useForm<CreatePostFormData>({
    resolver: zodResolver(createPostSchema),
    defaultValues: {
      content: '',
    },
  });

  const content = watch('content');
  const characterCount = content?.length || 0;
  const isNearLimit = characterCount > 250;
  const isAtLimit = characterCount >= 280;

  const handleImageSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files || []);
    const imageFiles = files.filter(file => file.type.startsWith('image/'));
    
    if (imageFiles.length + selectedImages.length > 4) {
      toast.error('You can only upload up to 4 images');
      return;
    }

    setSelectedImages(prev => [...prev, ...imageFiles]);
  };

  const removeImage = (index: number) => {
    setSelectedImages(prev => prev.filter((_, i) => i !== index));
  };

  const onSubmit = async (data: CreatePostFormData) => {
    if (!user) return;
    
    setIsSubmitting(true);
    
    try {
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Create new post object
      const newPost: Post = {
        id: Date.now().toString(),
        content: data.content,
        images: selectedImages.map(file => URL.createObjectURL(file)),
        videos: [],
        author: user,
        likesCount: 0,
        commentsCount: 0,
        sharesCount: 0,
        isLiked: false,
        isBookmarked: false,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        hashtags: data.content.match(/#\w+/g)?.map(tag => tag.slice(1)) || [],
        mentions: data.content.match(/@\w+/g)?.map(mention => mention.slice(1)) || [],
      };
      
      // Call the callback to add the post to the feed
      onPostCreated?.(newPost);
      
      toast.success('Post created successfully!');
      reset();
      setSelectedImages([]);
    } catch (error) {
      toast.error('Failed to create post');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Card>
      <CardContent className="p-6">
        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="flex space-x-4">
            {/* User Avatar */}
            <Avatar className="h-10 w-10 flex-shrink-0">
              <AvatarImage src={user?.avatar} alt={user?.displayName} />
              <AvatarFallback>
                {user?.displayName?.charAt(0).toUpperCase() || 'U'}
              </AvatarFallback>
            </Avatar>

            {/* Post Content */}
            <div className="flex-1 space-y-4">
              {/* Text Area */}
              <div className="relative">
                <textarea
                  {...register('content')}
                  placeholder="What's happening?"
                  className="w-full min-h-[120px] p-3 text-lg resize-none border rounded-md bg-background focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent"
                  disabled={isSubmitting}
                />
                
                {/* Character Count */}
                <div className="absolute bottom-2 right-2 text-xs text-muted-foreground">
                  <span className={isNearLimit ? (isAtLimit ? 'text-destructive' : 'text-orange-500') : ''}>
                    {characterCount}/280
                  </span>
                </div>
              </div>

              {/* Error Message */}
              {errors.content && (
                <p className="text-sm text-destructive">{errors.content.message}</p>
              )}

              {/* Selected Images Preview */}
              {selectedImages.length > 0 && (
                <div className="grid grid-cols-2 gap-2 mt-4">
                  {selectedImages.map((file, index) => (
                    <div key={index} className="relative group">
                      <img
                        src={URL.createObjectURL(file)}
                        alt={`Selected ${index + 1}`}
                        className="w-full h-32 object-cover rounded-md"
                      />
                      <button
                        type="button"
                        onClick={() => removeImage(index)}
                        className="absolute top-2 right-2 p-1 bg-black/50 rounded-full text-white opacity-0 group-hover:opacity-100 transition-opacity"
                      >
                        <X className="h-4 w-4" />
                      </button>
                    </div>
                  ))}
                </div>
              )}

              {/* Actions */}
              <div className="flex items-center justify-between pt-4 border-t">
                <div className="flex items-center space-x-2">
                  {/* Image Upload */}
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    onClick={() => fileInputRef.current?.click()}
                    disabled={isSubmitting || selectedImages.length >= 4}
                    className="text-primary hover:bg-primary/10"
                  >
                    <Image className="h-4 w-4" />
                  </Button>

                  {/* Video Upload (placeholder) */}
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    disabled
                    className="text-muted-foreground"
                  >
                    <Video className="h-4 w-4" />
                  </Button>

                  {/* Emoji (placeholder) */}
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    disabled
                    className="text-muted-foreground"
                  >
                    <Smile className="h-4 w-4" />
                  </Button>
                </div>

                {/* Submit Button */}
                <Button
                  type="submit"
                  disabled={isSubmitting || !content?.trim() || isAtLimit}
                  className="px-6"
                >
                  {isSubmitting ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Posting...
                    </>
                  ) : (
                    'Post'
                  )}
                </Button>
              </div>
            </div>
          </div>

          {/* Hidden File Input */}
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            multiple
            onChange={handleImageSelect}
            className="hidden"
          />
        </form>
      </CardContent>
    </Card>
  );
};
