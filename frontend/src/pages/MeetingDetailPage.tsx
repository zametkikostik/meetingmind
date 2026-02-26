import { useParams } from 'react-router-dom'
import { format } from 'date-fns'
import {
  Clock,
  Users,
  FileText,
  CheckSquare,
  Brain,
  TrendingUp,
  Play,
} from 'lucide-react'
import { useMeeting, useMeetingTranscripts } from '@/hooks/useMeetings'
import { Sidebar } from '@/components/layout/Sidebar'
import { Header } from '@/components/layout/Header'
import { Card, CardContent, CardHeader } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import { Spinner } from '@/components/ui/Spinner'

export function MeetingDetailPage() {
  const { id } = useParams<{ id: string }>()
  const { data: meeting, isLoading } = useMeeting(id!)
  const { data: transcripts = [] } = useMeetingTranscripts(id!)
  
  if (isLoading || !meeting) {
    return (
      <Sidebar>
        <div className="min-h-screen flex items-center justify-center">
          <Spinner size="lg" />
        </div>
      </Sidebar>
    )
  }
  
  const statusColors: Record<string, 'default' | 'success' | 'warning' | 'info' | 'danger'> = {
    scheduled: 'warning',
    in_progress: 'info',
    completed: 'success',
    failed: 'danger',
  }
  
  return (
    <Sidebar>
      <Header />
      
      <div className="p-6">
        {/* Header */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-2xl font-bold text-dark-800">{meeting.title}</h1>
              <p className="text-dark-600 mt-1">{meeting.description || 'No description'}</p>
            </div>
            <Badge variant={statusColors[meeting.status as keyof typeof statusColors]}>
              {meeting.status}
            </Badge>
          </div>
          
          <div className="flex items-center space-x-6 text-sm text-dark-600">
            <span className="flex items-center">
              <Clock className="h-4 w-4 mr-1" />
              {meeting.duration_seconds
                ? `${Math.round(meeting.duration_seconds / 60)} minutes`
                : 'No duration'}
            </span>
            <span className="flex items-center">
              <Calendar className="h-4 w-4 mr-1" />
              {meeting.scheduled_at
                ? format(new Date(meeting.scheduled_at), 'MMM d, yyyy HH:mm')
                : 'No date'}
            </span>
            <span className="flex items-center">
              <Users className="h-4 w-4 mr-1" />
              0 participants
            </span>
          </div>
        </div>
        
        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Summary & Transcript */}
          <div className="lg:col-span-2 space-y-6">
            {/* Summary */}
            {meeting.summary && (
              <Card>
                <CardHeader className="flex flex-row items-center space-x-2">
                  <Brain className="h-5 w-5 text-primary-600" />
                  <h2 className="font-semibold">AI Summary</h2>
                </CardHeader>
                <CardContent>
                  <p className="text-dark-700">{meeting.summary}</p>
                </CardContent>
              </Card>
            )}
            
            {/* Topics */}
            {meeting.key_topics && meeting.key_topics.length > 0 && (
              <Card>
                <CardHeader className="flex flex-row items-center space-x-2">
                  <TrendingUp className="h-5 w-5 text-primary-600" />
                  <h2 className="font-semibold">Key Topics</h2>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-2">
                    {meeting.key_topics.map((topic: string, index: number) => (
                      <Badge key={index} variant="info">
                        {topic}
                      </Badge>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
            
            {/* Transcript */}
            <Card>
              <CardHeader className="flex flex-row items-center space-x-2">
                <FileText className="h-5 w-5 text-primary-600" />
                <h2 className="font-semibold">Transcript</h2>
              </CardHeader>
              <CardContent>
                {transcripts.length === 0 ? (
                  <p className="text-dark-600 text-center py-8">
                    No transcript available yet
                  </p>
                ) : (
                  <div className="space-y-4 max-h-96 overflow-y-auto">
                    {transcripts.map((t: any) => (
                      <div key={t.id} className="flex space-x-3">
                        <span className="text-xs text-dark-500 w-16 flex-shrink-0">
                          {formatTime(t.start_time)}
                        </span>
                        <div>
                          <span className="font-medium text-dark-800 mr-2">
                            {t.speaker_name || 'Unknown'}
                          </span>
                          <span className="text-dark-700">{t.text}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
          
          {/* Sidebar */}
          <div className="space-y-6">
            {/* Action Items */}
            <Card>
              <CardHeader className="flex flex-row items-center space-x-2">
                <CheckSquare className="h-5 w-5 text-primary-600" />
                <h2 className="font-semibold">Action Items</h2>
              </CardHeader>
              <CardContent>
                <p className="text-dark-600 text-sm">
                  Action items will appear here after analysis
                </p>
              </CardContent>
            </Card>
            
            {/* Sentiment */}
            {meeting.sentiment_score && (
              <Card>
                <CardHeader className="flex flex-row items-center space-x-2">
                  <TrendingUp className="h-5 w-5 text-primary-600" />
                  <h2 className="font-semibold">Sentiment</h2>
                </CardHeader>
                <CardContent>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-dark-800">
                      {Math.round(meeting.sentiment_score * 100)}%
                    </div>
                    <p className="text-sm text-dark-600 mt-1">
                      {meeting.sentiment_score > 0.7 ? 'Positive' :
                       meeting.sentiment_score > 0.4 ? 'Neutral' : 'Negative'}
                    </p>
                  </div>
                </CardContent>
              </Card>
            )}
            
            {/* Actions */}
            <Card>
              <CardHeader>
                <h2 className="font-semibold">Actions</h2>
              </CardHeader>
              <CardContent className="space-y-2">
                <Button variant="outline" className="w-full justify-start">
                  <Play className="h-4 w-4 mr-2" />
                  Play Recording
                </Button>
                <Button variant="outline" className="w-full justify-start">
                  <FileText className="h-4 w-4 mr-2" />
                  Export Transcript
                </Button>
                <Button variant="outline" className="w-full justify-start">
                  <CheckSquare className="h-4 w-4 mr-2" />
                  Add Action Item
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </Sidebar>
  )
}

function formatTime(seconds: number): string {
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

// Placeholder for Calendar icon
function Calendar(props: any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <rect width="18" height="18" x="3" y="4" rx="2" ry="2" />
      <line x1="16" x2="16" y1="2" y2="6" />
      <line x1="8" x2="8" y1="2" y2="6" />
      <line x1="3" x2="21" y1="10" y2="10" />
    </svg>
  )
}
