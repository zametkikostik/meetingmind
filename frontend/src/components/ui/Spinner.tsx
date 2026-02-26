import { HTMLAttributes, forwardRef } from 'react'
import { cn } from '@/lib/utils'

export interface SpinnerProps extends HTMLAttributes<HTMLDivElement> {
  size?: 'sm' | 'md' | 'lg'
}

export const Spinner = forwardRef<HTMLDivElement, SpinnerProps>(
  ({ className, size = 'md', ...props }, ref) => {
    const sizes = {
      sm: 'h-4 w-4',
      md: 'h-8 w-8',
      lg: 'h-12 w-12',
    }
    
    return (
      <div
        className={cn(
          'animate-spin rounded-full border-2 border-current border-t-transparent',
          'text-primary-600',
          sizes[size],
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)

Spinner.displayName = 'Spinner'
