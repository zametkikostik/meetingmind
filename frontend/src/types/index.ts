export interface User {
  id: string
  email: string
  full_name: string | null
  avatar_url: string | null
  timezone: string
  language: string
  is_active: boolean
  is_verified: boolean
  created_at: string
}

export interface Meeting {
  id: string
  organization_id: string
  title: string
  description: string | null
  external_id: string | null
  platform: string | null
  status: MeetingStatus
  scheduled_at: string | null
  started_at: string | null
  ended_at: string | null
  duration_seconds: number | null
  recording_url: string | null
  transcript_status: string
  analysis_status: string
  summary: string | null
  key_topics: string[]
  sentiment_score: number | null
  created_at: string
  updated_at: string
}

export type MeetingStatus = 'scheduled' | 'in_progress' | 'completed' | 'failed'

export interface MeetingParticipant {
  id: string
  meeting_id: string
  user_id: string | null
  name: string | null
  email: string | null
  role: ParticipantRole
  join_time: string | null
  leave_time: string | null
  duration_seconds: number | null
  talk_time_seconds: number
  is_speaker: boolean
}

export type ParticipantRole = 'host' | 'participant' | 'guest'

export interface Transcript {
  id: string
  meeting_id: string
  participant_id: string | null
  speaker_name: string | null
  text: string
  start_time: number
  end_time: number
  confidence: number | null
  sentiment: string | null
  is_key_moment: boolean
  created_at: string
}

export interface ActionItem {
  id: string
  meeting_id: string
  assignee_user_id: string | null
  assignee_name: string | null
  assignee_email: string | null
  task: string
  status: ActionItemStatus
  priority: string
  due_date: string | null
  completed_at: string | null
  created_at: string
  updated_at: string
}

export type ActionItemStatus = 'pending' | 'in_progress' | 'completed' | 'cancelled'

export interface AuthTokens {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  email: string
  password: string
  full_name?: string
}
