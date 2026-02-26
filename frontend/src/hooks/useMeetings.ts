import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { meetingsApi } from '@/lib/api'
import type { Meeting } from '@/types'

export function useMeetings() {
  return useQuery<Meeting[]>({
    queryKey: ['meetings'],
    queryFn: async () => {
      const response = await meetingsApi.list()
      return response.data
    },
  })
}

export function useMeeting(id: string) {
  return useQuery<Meeting>({
    queryKey: ['meeting', id],
    queryFn: async () => {
      const response = await meetingsApi.get(id)
      return response.data
    },
    enabled: !!id,
  })
}

export function useCreateMeeting() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: meetingsApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['meetings'] })
    },
  })
}

export function useUpdateMeeting() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: { title?: string; description?: string | null; status?: string } }) =>
      meetingsApi.update(id, data as any),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['meetings'] })
    },
  })
}

export function useDeleteMeeting() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: meetingsApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['meetings'] })
    },
  })
}

export function useMeetingTranscripts(meetingId: string) {
  return useQuery({
    queryKey: ['transcripts', meetingId],
    queryFn: async () => {
      const response = await meetingsApi.getTranscripts(meetingId)
      return response.data
    },
    enabled: !!meetingId,
  })
}

export function useCreateActionItem() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: ({ meetingId, data }: { meetingId: string; data: { task: string; assignee_name?: string; priority?: string } }) =>
      meetingsApi.createActionItem(meetingId, data as any),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['meeting'] })
    },
  })
}
