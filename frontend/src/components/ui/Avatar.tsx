import { HTMLAttributes, forwardRef } from 'react'
import { cn } from '@/lib/utils'

export interface AvatarProps extends HTMLAttributes<HTMLDivElement> {
  src?: string | null
  alt?: string
  size?: 'sm' | 'md' | 'lg'
  fallback?: string
}

export const Avatar = forwardRef<HTMLDivElement, AvatarProps>(
  ({ className, src, alt, size = 'md', fallback, ...props }, ref) => {
    const sizes = {
      sm: 'h-8 w-8 text-xs',
      md: 'h-10 w-10 text-sm',
      lg: 'h-12 w-12 text-base',
    }
    
    return (
      <div
        className={cn(
          'relative inline-flex items-center justify-center overflow-hidden rounded-full bg-dark-200',
          sizes[size],
          className
        )}
        ref={ref}
        {...props}
      >
        {src ? (
          <img
            className="h-full w-full object-cover"
            src={src}
            alt={alt}
          />
        ) : (
          <span className="font-medium text-dark-600">
            {fallback || '?'}
          </span>
        )}
      </div>
    )
  }
)

Avatar.displayName = 'Avatar'
