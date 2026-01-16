import { useEffect, useState, useCallback } from 'react'
import { useSettingsStore } from '@/stores/settings'
import { listThreads, createThread, deleteThread, updateThread, getThread } from '@/api/lightrag'
import { PlusIcon, MessageSquareIcon, Trash2Icon, Edit2Icon, CheckIcon, XIcon } from 'lucide-react'
import { toast } from 'sonner'
import Button from '@/components/ui/Button'
import Input from '@/components/ui/Input'
import { cn } from '@/lib/utils'
import { useTranslation } from 'react-i18next'
import type { ThreadListItem } from '@/api/lightrag'

interface ThreadSidebarProps {
  onThreadSelect: (threadId: string | null) => void
  onNewThread: () => void
}

export function ThreadSidebar({ onThreadSelect, onNewThread }: ThreadSidebarProps) {
  const { t } = useTranslation()
  const [threads, setThreads] = useState<ThreadListItem[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [editingThreadId, setEditingThreadId] = useState<string | null>(null)
  const [editingTitle, setEditingTitle] = useState('')
  const currentThreadId = useSettingsStore.use.currentThreadId()
  const setCurrentThreadId = useSettingsStore.use.setCurrentThreadId()
  const setThreadsList = useSettingsStore.use.setThreadsList()

  const loadThreads = useCallback(async () => {
    try {
      setIsLoading(true)
      const threadsList = await listThreads()
      setThreads(threadsList)
      setThreadsList(threadsList)
    } catch (error) {
      console.error('Error loading threads:', error)
      toast.error('Failed to load threads')
    } finally {
      setIsLoading(false)
    }
  }, [setThreadsList])

  useEffect(() => {
    loadThreads()
  }, [loadThreads])

  const handleNewThread = async () => {
    try {
      const newThread = await createThread({ title: 'New Conversation' })
      setCurrentThreadId(newThread.id)
      await loadThreads()
      onNewThread()
      toast.success('New thread created')
    } catch (error) {
      console.error('Error creating thread:', error)
      toast.error('Failed to create thread')
    }
  }

  const handleSelectThread = async (threadId: string) => {
    try {
      // Load the full thread data
      const thread = await getThread(threadId)
      setCurrentThreadId(threadId)
      onThreadSelect(threadId)
    } catch (error) {
      console.error('Error loading thread:', error)
      toast.error('Failed to load thread')
    }
  }

  const handleDeleteThread = async (threadId: string, e: React.MouseEvent) => {
    e.stopPropagation()
    if (!confirm('Are you sure you want to delete this thread?')) {
      return
    }

    try {
      await deleteThread(threadId)
      if (currentThreadId === threadId) {
        setCurrentThreadId(null)
        onThreadSelect(null)
      }
      await loadThreads()
      toast.success('Thread deleted')
    } catch (error) {
      console.error('Error deleting thread:', error)
      toast.error('Failed to delete thread')
    }
  }

  const handleStartEdit = (thread: ThreadListItem, e: React.MouseEvent) => {
    e.stopPropagation()
    setEditingThreadId(thread.id)
    setEditingTitle(thread.title)
  }

  const handleSaveEdit = async (threadId: string, e: React.MouseEvent) => {
    e.stopPropagation()
    if (!editingTitle.trim()) {
      toast.error('Title cannot be empty')
      return
    }

    try {
      await updateThread(threadId, { title: editingTitle.trim() })
      setEditingThreadId(null)
      await loadThreads()
      toast.success('Thread title updated')
    } catch (error) {
      console.error('Error updating thread:', error)
      toast.error('Failed to update thread')
    }
  }

  const handleCancelEdit = (e: React.MouseEvent) => {
    e.stopPropagation()
    setEditingThreadId(null)
    setEditingTitle('')
  }

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr)
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffMins = Math.floor(diffMs / 60000)
    const diffHours = Math.floor(diffMs / 3600000)
    const diffDays = Math.floor(diffMs / 86400000)

    if (diffMins < 1) return 'Just now'
    if (diffMins < 60) return `${diffMins}m ago`
    if (diffHours < 24) return `${diffHours}h ago`
    if (diffDays < 7) return `${diffDays}d ago`

    return date.toLocaleDateString()
  }

  return (
    <div className="flex flex-col h-full bg-background border-r border-border">
      <div className="p-4 border-b border-border">
        <Button
          onClick={handleNewThread}
          className="w-full"
          variant="default"
        >
          <PlusIcon className="w-4 h-4 mr-2" />
          New Thread
        </Button>
      </div>

      <div className="flex-1 overflow-y-auto">
        {isLoading ? (
          <div className="p-4 text-center text-muted-foreground">
            Loading threads...
          </div>
        ) : threads.length === 0 ? (
          <div className="p-4 text-center text-muted-foreground">
            <MessageSquareIcon className="w-12 h-12 mx-auto mb-2 opacity-50" />
            <p>No threads yet</p>
            <p className="text-sm">Create a new thread to start</p>
          </div>
        ) : (
          <div className="divide-y divide-border">
            {threads.map((thread) => (
              <div
                key={thread.id}
                onClick={() => handleSelectThread(thread.id)}
                className={cn(
                  'p-3 cursor-pointer hover:bg-muted/50 transition-colors group',
                  currentThreadId === thread.id && 'bg-muted'
                )}
              >
                {editingThreadId === thread.id ? (
                  <div className="flex items-center gap-2" onClick={(e) => e.stopPropagation()}>
                    <Input
                      value={editingTitle}
                      onChange={(e) => setEditingTitle(e.target.value)}
                      className="flex-1 h-8 text-sm"
                      autoFocus
                      onKeyDown={(e) => {
                        if (e.key === 'Enter') {
                          handleSaveEdit(thread.id, e as any)
                        } else if (e.key === 'Escape') {
                          handleCancelEdit(e as any)
                        }
                      }}
                    />
                    <button
                      onClick={(e) => handleSaveEdit(thread.id, e)}
                      className="p-1 hover:bg-background rounded"
                    >
                      <CheckIcon className="w-4 h-4 text-green-600" />
                    </button>
                    <button
                      onClick={handleCancelEdit}
                      className="p-1 hover:bg-background rounded"
                    >
                      <XIcon className="w-4 h-4 text-red-600" />
                    </button>
                  </div>
                ) : (
                  <>
                    <div className="flex items-start justify-between mb-1">
                      <h3 className="font-medium text-sm truncate flex-1">
                        {thread.title}
                      </h3>
                      <div className="flex gap-1 ml-2">
                        <button
                          onClick={(e) => handleStartEdit(thread, e)}
                          className="p-1 hover:bg-background rounded opacity-0 group-hover:opacity-100 transition-opacity"
                        >
                          <Edit2Icon className="w-3 h-3" />
                        </button>
                        <button
                          onClick={(e) => handleDeleteThread(thread.id, e)}
                          className="p-1 hover:bg-background rounded opacity-0 group-hover:opacity-100 transition-opacity"
                        >
                          <Trash2Icon className="w-3 h-3 text-red-600" />
                        </button>
                      </div>
                    </div>
                    <div className="text-xs text-muted-foreground mb-1">
                      {thread.message_count} messages · {formatDate(thread.updated_at)}
                    </div>
                    {thread.preview && (
                      <p className="text-xs text-muted-foreground truncate">
                        {thread.preview}
                      </p>
                    )}
                  </>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
