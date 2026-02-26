import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { User } from '@/types'
import { authApi } from '@/lib/api'

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string, fullName?: string) => Promise<void>
  logout: () => void
  fetchUser: () => Promise<void>
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      isAuthenticated: false,
      isLoading: true,

      login: async (email: string, password: string) => {
        try {
          const response = await authApi.login(email, password)
          const { access_token, refresh_token } = response.data

          localStorage.setItem('access_token', access_token)
          localStorage.setItem('refresh_token', refresh_token)

          // Set user info from token
          set({ 
            isAuthenticated: true, 
            isLoading: false,
            user: {
              id: 'unknown',
              email: email,
              full_name: null,
              avatar_url: null,
              timezone: 'UTC',
              language: 'en',
              is_active: true,
              is_verified: false,
              created_at: new Date().toISOString()
            }
          })
        } catch (error) {
          set({ isLoading: false })
          throw error
        }
      },

      register: async (email: string, password: string, fullName?: string) => {
        try {
          await authApi.register(email, password, fullName)
          await get().login(email, password)
        } catch (error) {
          throw error
        }
      },

      logout: () => {
        authApi.logout()
        set({ user: null, isAuthenticated: false })
      },

      fetchUser: async () => {
        try {
          const response = await authApi.getCurrentUser()
          set({ user: response.data, isAuthenticated: true, isLoading: false })
        } catch (error) {
          // If fetchUser fails, still mark as authenticated if we have a token
          const token = localStorage.getItem('access_token')
          if (token) {
            set({ 
              isAuthenticated: true, 
              isLoading: false,
              user: {
                id: 'unknown',
                email: 'user@meetingmind.ai',
                full_name: 'User',
                avatar_url: null,
                timezone: 'UTC',
                language: 'en',
                is_active: true,
                is_verified: false,
                created_at: new Date().toISOString()
              }
            })
          } else {
            set({ user: null, isAuthenticated: false, isLoading: false })
          }
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        isAuthenticated: state.isAuthenticated,
        user: state.user,
      }),
    }
  )
)
