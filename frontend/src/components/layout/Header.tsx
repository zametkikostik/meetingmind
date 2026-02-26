import { Bell, Search } from 'lucide-react'
import { Input } from '@/components/ui/Input'
import { Button } from '@/components/ui/Button'
import { Avatar } from '@/components/ui/Avatar'
import { useAuth } from '@/hooks/useAuth'

export function Header() {
  const { user } = useAuth()
  
  return (
    <header className="bg-white border-b border-dark-200">
      <div className="px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Search */}
          <div className="flex-1 max-w-lg">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-dark-400" />
              <Input
                type="search"
                placeholder="Search meetings, topics, action items..."
                className="pl-10"
              />
            </div>
          </div>
          
          {/* Right side */}
          <div className="flex items-center space-x-4">
            <Button variant="ghost" size="sm">
              <Bell className="h-5 w-5" />
            </Button>
            
            <Avatar
              size="md"
              src={user?.avatar_url}
              alt={user?.full_name || user?.email}
              fallback={user?.email?.charAt(0).toUpperCase()}
            />
          </div>
        </div>
      </div>
    </header>
  )
}
