import { ReactNode } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { cn } from '@/lib/utils'
import {
  LayoutDashboard,
  Calendar,
  FolderOpen,
  Settings,
  LogOut,
  Brain,
  FileText,
  Book,
} from 'lucide-react'
import { useAuth } from '@/hooks/useAuth'
import { Avatar } from '@/components/ui/Avatar'
import { Button } from '@/components/ui/Button'

interface SidebarProps {
  children?: ReactNode
}

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Meetings', href: '/meetings', icon: Calendar },
  { name: 'Notes', href: '/notes', icon: Book },
  { name: 'Calendar', href: '/calendar', icon: FileText },
  { name: 'Knowledge', href: '/knowledge', icon: FolderOpen },
  { name: 'Settings', href: '/settings', icon: Settings },
]

export function Sidebar({ children }: SidebarProps) {
  const location = useLocation()
  const { user, logout } = useAuth()
  
  return (
    <div className="min-h-screen bg-dark-50 flex">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-dark-200 flex flex-col">
        {/* Logo */}
        <div className="h-16 flex items-center px-6 border-b border-dark-200">
          <Brain className="h-8 w-8 text-primary-600" />
          <span className="ml-3 text-lg font-bold text-dark-800">MeetingMind</span>
        </div>
        
        {/* Navigation */}
        <nav className="flex-1 px-4 py-6 space-y-1">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href
            return (
              <Link
                key={item.name}
                to={item.href}
                className={cn(
                  'flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors',
                  isActive
                    ? 'bg-primary-50 text-primary-700'
                    : 'text-dark-600 hover:bg-dark-100'
                )}
              >
                <item.icon className={cn('h-5 w-5 mr-3', isActive ? 'text-primary-600' : 'text-dark-400')} />
                {item.name}
              </Link>
            )
          })}
        </nav>
        
        {/* User */}
        <div className="p-4 border-t border-dark-200">
          <div className="flex items-center">
            <Avatar
              size="md"
              alt={user?.full_name || user?.email}
              fallback={user?.email?.charAt(0).toUpperCase()}
            />
            <div className="ml-3 flex-1 min-w-0">
              <p className="text-sm font-medium text-dark-800 truncate">
                {user?.full_name || 'User'}
              </p>
              <p className="text-xs text-dark-500 truncate">{user?.email}</p>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={logout}
              className="ml-2"
            >
              <LogOut className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </aside>
      
      {/* Main content */}
      <main className="flex-1 overflow-auto">
        {children}
      </main>
    </div>
  )
}
