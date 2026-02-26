import { useState } from 'react'
import { format } from 'date-fns'
import { Calendar, Clock, Users, Plus, Search, Filter } from 'lucide-react'
import { useMeetings, useCreateMeeting } from '@/hooks/useMeetings'
import { Sidebar } from '@/components/layout/Sidebar'
import { Header } from '@/components/layout/Header'
import { Card, CardContent } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import { Input } from '@/components/ui/Input'
import toast from 'react-hot-toast'

export function MeetingsPage() {
  const { data: meetings = [], isLoading } = useMeetings()
  const createMeeting = useCreateMeeting()
  const [searchQuery, setSearchQuery] = useState('')
  const [showNewMeetingModal, setShowNewMeetingModal] = useState(false)
  const [newMeetingTitle, setNewMeetingTitle] = useState('')
  
  const filteredMeetings = meetings.filter(m =>
    m.title.toLowerCase().includes(searchQuery.toLowerCase())
  )
  
  const handleCreateMeeting = async () => {
    if (!newMeetingTitle.trim()) {
      toast.error('Please enter a meeting title')
      return
    }
    
    try {
      await createMeeting.mutateAsync({
        title: newMeetingTitle,
      })
      toast.success('Meeting created!')
      setShowNewMeetingModal(false)
      setNewMeetingTitle('')
    } catch (error) {
      toast.error('Failed to create meeting')
    }
  }
  
  return (
    <Sidebar>
      <Header />
      
      <div className="p-6">
        {/* Page Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold text-dark-800">Meetings</h1>
            <p className="text-dark-600 mt-1">Manage and review your meetings</p>
          </div>
          
          <Button onClick={() => setShowNewMeetingModal(true)}>
            <Plus className="h-5 w-5 mr-2" />
            New Meeting
          </Button>
        </div>
        
        {/* Filters */}
        <Card className="mb-6">
          <CardContent className="py-4">
            <div className="flex items-center space-x-4">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-dark-400" />
                <Input
                  placeholder="Search meetings..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10"
                />
              </div>
              <Button variant="outline">
                <Filter className="h-5 w-5 mr-2" />
                Filter
              </Button>
            </div>
          </CardContent>
        </Card>
        
        {/* Meetings List */}
        {isLoading ? (
          <Card>
            <CardContent className="py-12 text-center">
              <p className="text-dark-600">Loading meetings...</p>
            </CardContent>
          </Card>
        ) : filteredMeetings.length === 0 ? (
          <Card>
            <CardContent className="py-12 text-center">
              <Calendar className="h-12 w-12 text-dark-400 mx-auto mb-4" />
              <p className="text-dark-600 mb-4">
                {searchQuery ? 'No meetings found' : 'No meetings yet'}
              </p>
              {!searchQuery && (
                <Button onClick={() => setShowNewMeetingModal(true)}>
                  <Plus className="h-5 w-5 mr-2" />
                  Create Meeting
                </Button>
              )}
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-4">
            {filteredMeetings.map((meeting) => (
              <MeetingCard key={meeting.id} meeting={meeting} />
            ))}
          </div>
        )}
      </div>
      
      {/* New Meeting Modal */}
      {showNewMeetingModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <Card className="w-full max-w-md mx-4">
            <CardContent className="py-6">
              <h2 className="text-lg font-semibold mb-4">Create New Meeting</h2>
              <Input
                label="Meeting Title"
                value={newMeetingTitle}
                onChange={(e) => setNewMeetingTitle(e.target.value)}
                placeholder="Enter meeting title"
                autoFocus
              />
              <div className="flex justify-end space-x-3 mt-6">
                <Button
                  variant="outline"
                  onClick={() => setShowNewMeetingModal(false)}
                >
                  Cancel
                </Button>
                <Button onClick={handleCreateMeeting}>
                  Create Meeting
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </Sidebar>
  )
}

interface MeetingCardProps {
  meeting: any
}

function MeetingCard({ meeting }: MeetingCardProps) {
  const statusColors: Record<string, 'default' | 'success' | 'warning' | 'info' | 'danger'> = {
    scheduled: 'warning',
    in_progress: 'info',
    completed: 'success',
    failed: 'danger',
  }
  
  return (
    <Card className="hover:shadow-md transition-shadow cursor-pointer">
      <CardContent className="py-4">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center space-x-3 mb-2">
              <h3 className="font-semibold text-dark-800">{meeting.title}</h3>
              <Badge variant={statusColors[meeting.status as keyof typeof statusColors]}>
                {meeting.status}
              </Badge>
            </div>
            
            {meeting.description && (
              <p className="text-dark-600 text-sm mb-3">{meeting.description}</p>
            )}
            
            <div className="flex items-center space-x-4 text-sm text-dark-600">
              <span className="flex items-center">
                <Calendar className="h-4 w-4 mr-1" />
                {meeting.scheduled_at
                  ? format(new Date(meeting.scheduled_at), 'MMM d, yyyy HH:mm')
                  : 'No date'}
              </span>
              <span className="flex items-center">
                <Clock className="h-4 w-4 mr-1" />
                {meeting.duration_seconds
                  ? `${Math.round(meeting.duration_seconds / 60)} min`
                  : '—'}
              </span>
              <span className="flex items-center">
                <Users className="h-4 w-4 mr-1" />
                0 participants
              </span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
