import { useState } from 'react'
import { format, startOfWeek, endOfWeek, eachDayOfInterval, isToday, isSameDay } from 'date-fns'
import { Calendar as CalendarIcon, ChevronLeft, ChevronRight, Clock, Video } from 'lucide-react'
import { Sidebar } from '@/components/layout/Sidebar'
import { Header } from '@/components/layout/Header'
import { Card, CardContent } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'

interface CalendarEvent {
  id: string
  title: string
  start_time: string
  end_time: string
  meeting_link?: string
  is_meetingmind_meeting: boolean
}

export function CalendarPage() {
  const [currentWeekStart, setCurrentWeekStart] = useState(startOfWeek(new Date()))
  const [events] = useState<CalendarEvent[]>([]) // TODO: Load from API
  
  const weekDays = eachDayOfInterval({
    start: currentWeekStart,
    end: endOfWeek(currentWeekStart)
  })
  
  const nextWeek = () => {
    setCurrentWeekStart(new Date(currentWeekStart.setDate(currentWeekStart.getDate() + 7)))
  }
  
  const prevWeek = () => {
    setCurrentWeekStart(new Date(currentWeekStart.setDate(currentWeekStart.getDate() - 7)))
  }
  
  const getEventsForDay = (date: Date) => {
    return events.filter(event => isSameDay(new Date(event.start_time), date))
  }
  
  return (
    <Sidebar>
      <Header />
      
      <div className="p-6">
        {/* Page Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold text-dark-800">Calendar</h1>
            <p className="text-dark-600 mt-1">Schedule and sync your meetings</p>
          </div>
          
          <Button>
            <CalendarIcon className="h-5 w-5 mr-2" />
            Sync Calendar
          </Button>
        </div>
        
        {/* Week Navigation */}
        <Card className="mb-6">
          <CardContent className="py-4">
            <div className="flex items-center justify-between">
              <Button variant="outline" onClick={prevWeek}>
                <ChevronLeft className="h-5 w-5" />
              </Button>
              
              <h2 className="text-lg font-semibold">
                {format(currentWeekStart, 'MMMM yyyy')}
              </h2>
              
              <Button variant="outline" onClick={nextWeek}>
                <ChevronRight className="h-5 w-5" />
              </Button>
            </div>
          </CardContent>
        </Card>
        
        {/* Week View */}
        <div className="grid grid-cols-7 gap-4">
          {weekDays.map((day) => {
            const dayEvents = getEventsForDay(day)
            
            return (
              <div key={day.toISOString()} className="min-h-[200px]">
                {/* Day Header */}
                <div className={`text-center py-2 rounded-t-lg mb-2 ${
                  isToday(day) ? 'bg-primary-100 text-primary-700' : 'bg-dark-100'
                }`}>
                  <p className="text-xs font-medium uppercase">
                    {format(day, 'EEE')}
                  </p>
                  <p className={`text-lg font-bold ${isToday(day) ? 'text-primary-600' : ''}`}>
                    {format(day, 'd')}
                  </p>
                </div>
                
                {/* Events */}
                <div className="space-y-2">
                  {dayEvents.map(event => (
                    <EventCard key={event.id} event={event} />
                  ))}
                  
                  {dayEvents.length === 0 && (
                    <div className="text-center py-4 text-dark-400 text-sm">
                      No events
                    </div>
                  )}
                </div>
              </div>
            )
          })}
        </div>
        
        {/* Integration Cards */}
        <div className="mt-8">
          <h2 className="text-lg font-semibold text-dark-800 mb-4">Connected Calendars</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <IntegrationCard
              name="Google Calendar"
              connected={false}
              icon="📅"
            />
            <IntegrationCard
              name="Outlook Calendar"
              connected={false}
              icon="📆"
            />
            <IntegrationCard
              name="Apple Calendar"
              connected={false}
              icon="🗓️"
            />
          </div>
        </div>
      </div>
    </Sidebar>
  )
}

interface EventCardProps {
  event: CalendarEvent
}

function EventCard({ event }: EventCardProps) {
  const startTime = new Date(event.start_time)
  
  return (
    <div className={`p-2 rounded-lg text-xs cursor-pointer transition-colors ${
      event.is_meetingmind_meeting
        ? 'bg-primary-100 border border-primary-300'
        : 'bg-dark-50 border border-dark-200'
    }`}>
      <p className="font-medium text-dark-800 truncate">{event.title}</p>
      <div className="flex items-center mt-1 space-x-2 text-dark-600">
        <span className="flex items-center">
          <Clock className="h-3 w-3 mr-1" />
          {format(startTime, 'HH:mm')}
        </span>
        {event.meeting_link && (
          <span className="flex items-center">
            <Video className="h-3 w-3 mr-1" />
            Video
          </span>
        )}
      </div>
      {event.is_meetingmind_meeting && (
        <Badge variant="success" size="sm" className="mt-1">
          MeetingMind
        </Badge>
      )}
    </div>
  )
}

interface IntegrationCardProps {
  name: string
  connected: boolean
  icon: string
}

function IntegrationCard({ name, connected, icon }: IntegrationCardProps) {
  return (
    <Card>
      <CardContent className="py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <span className="text-2xl">{icon}</span>
            <div>
              <p className="font-medium text-dark-800">{name}</p>
              <p className="text-xs text-dark-600">
                {connected ? 'Connected' : 'Not connected'}
              </p>
            </div>
          </div>
          <Button variant={connected ? 'outline' : 'primary'} size="sm">
            {connected ? 'Disconnect' : 'Connect'}
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
