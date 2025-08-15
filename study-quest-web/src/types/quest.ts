export interface Quest {
  id: string
  title: string
  description: string
  subject: string
  difficulty: 'easy' | 'medium' | 'hard'
  experienceReward: number
  goldReward: number
  deadline: string
  isCompleted: boolean
  progress: number
  type: 'daily' | 'weekly' | 'boss' | 'special'
}

export interface QuestCategory {
  id: string
  name: string
  subject: string
  icon: string
  color: string
  quests: Quest[]
}

export interface QuestProgress {
  questId: string
  completedAt?: string
  score?: number
  timeSpent: number
  attempts: number
}

export interface Subject {
  id: string
  name: string
  icon: string
  color: string
  description: string
  totalQuests: number
  completedQuests: number
} 