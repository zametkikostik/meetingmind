import { Link } from 'react-router-dom'
import { format } from 'date-fns'
import {
  Calendar,
  Clock,
  Users,
  FileText,
  Plus,
  Play,
  CheckCircle,
} from 'lucide-react'
import { useMeetings } from '@/hooks/useMeetings'
import { Sidebar } from '@/components/layout/Sidebar'
import { Header } from '@/components/layout/Header'
import { Card, CardContent, CardHeader } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'

export function DashboardPage() {
  const { data: meetings = [], isLoading } = useMeetings()
  
  const stats = {
    total: meetings.length,
    completed: meetings.filter(m => m.status === 'completed').length,
    scheduled: meetings.filter(m => m.status === 'scheduled').length,
    totalDuration: meetings.reduce((acc, m) => acc + (m.duration_seconds || 0), 0),
  }
  
  const recentMeetings = meetings.slice(0, 5)
  
  return (
    <Sidebar>
      <Header />
      
      <div className="p-6">
        {/* Page Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold text-dark-800">Dashboard</h1>
            <p className="text-dark-600 mt-1">Overview of your meetings and insights</p>
          </div>
          
          <Link to="/meetings/new">
            <Button>
              <Plus className="h-5 w-5 mr-2" />
              New Meeting
            </Button>
          </Link>
        </div>
        
        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <StatCard
            icon={FileText}
            label="Total Meetings"
            value={stats.total}
            color="primary"
          />
          <StatCard
            icon={CheckCircle}
            label="Completed"
            value={stats.completed}
            color="success"
          />
          <StatCard
            icon={Calendar}
            label="Scheduled"
            value={stats.scheduled}
            color="warning"
          />
          <StatCard
            icon={Clock}
            label="Total Hours"
            value={(stats.totalDuration / 3600).toFixed(1)}
            color="info"
          />
        </div>
        
        {/* Recent Meetings */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <h2 className="text-lg font-semibold text-dark-800">Recent Meetings</h2>
            <Link to="/meetings">
              <Button variant="ghost" size="sm">View All</Button>
            </Link>
          </CardHeader>
          
          <CardContent>
            {isLoading ? (
              <p className="text-center text-dark-600 py-8">Loading...</p>
            ) : recentMeetings.length === 0 ? (
              <div className="text-center py-12">
                <Calendar className="h-12 w-12 text-dark-400 mx-auto mb-4" />
                <p className="text-dark-600 mb-4">No meetings yet</p>
                <Link to="/meetings/new">
                  <Button>Schedule Your First Meeting</Button>
                </Link>
              </div>
            ) : (
              <div className="space-y-4">
                {recentMeetings.map((meeting) => (
                  <MeetingRow key={meeting.id} meeting={meeting} />
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </Sidebar>
  )
}

interface StatCardProps {
  icon: any
  label: string
  value: string | number
  color: string
}

function StatCard({ icon: Icon, label, value, color }: StatCardProps) {
  const colors = {
    primary: 'bg-primary-100 text-primary-600',
    success: 'bg-green-100 text-green-600',
    warning: 'bg-yellow-100 text-yellow-600',
    info: 'bg-blue-100 text-blue-600',
  }
  
  return (
    <Card>
      <CardContent className="flex items-center">
        <div className={`p-3 rounded-lg ${colors[color as keyof typeof colors]}`}>
          <Icon className="h-6 w-6" />
        </div>
        <div className="ml-4">
          <p className="text-sm text-dark-600">{label}</p>
          <p className="text-2xl font-bold text-dark-800">{value}</p>
        </div>
      </CardContent>
    </Card>
  )
}

interface MeetingRowProps {
  meeting: any
}

function MeetingRow({ meeting }: MeetingRowProps) {
  const statusColors: Record<string, 'default' | 'success' | 'warning' | 'info' | 'danger'> = {
    scheduled: 'warning',
    in_progress: 'info',
    completed: 'success',
    failed: 'danger',
  }
  
  return (
    <Link
      to={`/meetings/${meeting.id}`}
      className="block hover:bg-dark-50 -mx-6 px-6 py-4 transition-colors border-b border-dark-100 last:border-0"
    >
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <h3 className="font-medium text-dark-800">{meeting.title}</h3>
          <div className="flex items-center mt-1 space-x-4 text-sm text-dark-600">
            <span className="flex items-center">
              <Calendar className="h-4 w-4 mr-1" />
              {meeting.scheduled_at ? format(new Date(meeting.scheduled_at), 'MMM d, yyyy') : 'No date'}
            </span>
            <span className="flex items-center">
              <Clock className="h-4 w-4 mr-1" />
              {meeting.duration_seconds ? `${Math.round(meeting.duration_seconds / 60)} min` : '—'}
            </span>
            <span className="flex items-center">
              <Users className="h-4 w-4 mr-1" />
              0 participants
            </span>
          </div>
        </div>
        
        <div className="flex items-center space-x-4">
          <Badge variant={statusColors[meeting.status as keyof typeof statusColors]}>
            {meeting.status}
          </Badge>
          <Button variant="ghost" size="sm">
            <Play className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </Link>
  )
}
