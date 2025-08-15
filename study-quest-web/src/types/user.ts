export type UserRole = 'student' | 'parent' | 'teacher'

export interface User {
  id: string
  username: string
  role: UserRole
  nickname: string
  avatar: string
  level: number
  experience: number
  goldCoins: number
  createdAt: string
}

export interface LoginCredentials {
  username: string
  password: string
  role: UserRole
}

export interface LoginResponse {
  success: boolean
  user?: User
  error?: string
} 