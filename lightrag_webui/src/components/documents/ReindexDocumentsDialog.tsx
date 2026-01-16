import { useState, useCallback, useEffect } from 'react'
import Button from '@/components/ui/Button'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter
} from '@/components/ui/Dialog'
import { toast } from 'sonner'
import { errorMessage } from '@/lib/utils'
import { reindexDocuments } from '@/api/lightrag'

import { RefreshCwIcon, InfoIcon } from 'lucide-react'
import { useTranslation } from 'react-i18next'

interface ReindexDocumentsDialogProps {
  selectedDocIds: string[]
  onDocumentsReindexed?: () => Promise<void>
}

export default function ReindexDocumentsDialog({ selectedDocIds, onDocumentsReindexed }: ReindexDocumentsDialogProps) {
  const { t } = useTranslation()
  const [open, setOpen] = useState(false)
  const [isReindexing, setIsReindexing] = useState(false)

  // Reset state when dialog closes
  useEffect(() => {
    if (!open) {
      setIsReindexing(false)
    }
  }, [open])

  const handleReindex = useCallback(async () => {
    if (selectedDocIds.length === 0) return

    setIsReindexing(true)
    try {
      const result = await reindexDocuments(selectedDocIds)

      if (result.status === 'reindexing_started') {
        toast.success(t('documentPanel.reindexDocuments.success', { count: selectedDocIds.length }))
      } else if (result.status === 'busy') {
        toast.error(t('documentPanel.reindexDocuments.busy'))
        setIsReindexing(false)
        return
      } else {
        toast.error(t('documentPanel.reindexDocuments.failed', { message: result.message }))
        setIsReindexing(false)
        return
      }

      // Refresh document list if provided
      if (onDocumentsReindexed) {
        onDocumentsReindexed().catch(console.error)
      }

      // Close dialog after successful operation
      setOpen(false)
    } catch (err) {
      toast.error(t('documentPanel.reindexDocuments.error', { error: errorMessage(err) }))
    } finally {
      setIsReindexing(false)
    }
  }, [selectedDocIds, setOpen, t, onDocumentsReindexed])

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button
          variant="outline"
          side="bottom"
          tooltip={t('documentPanel.reindexDocuments.tooltip', { count: selectedDocIds.length })}
          size="sm"
        >
          <RefreshCwIcon/> {t('documentPanel.reindexDocuments.button')}
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-xl" onCloseAutoFocus={(e) => e.preventDefault()}>
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2 text-blue-500 dark:text-blue-400 font-bold">
            <InfoIcon className="h-5 w-5" />
            {t('documentPanel.reindexDocuments.title')}
          </DialogTitle>
          <DialogDescription className="pt-2">
            {t('documentPanel.reindexDocuments.description', { count: selectedDocIds.length })}
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4">
          <div className="text-sm">
            {t('documentPanel.reindexDocuments.whatHappens')}
          </div>

          <ul className="list-disc list-inside text-sm space-y-2 text-gray-600 dark:text-gray-400">
            <li>{t('documentPanel.reindexDocuments.benefit1')}</li>
            <li>{t('documentPanel.reindexDocuments.benefit2')}</li>
            <li>{t('documentPanel.reindexDocuments.benefit3')}</li>
          </ul>

          <div className="text-sm text-yellow-600 dark:text-yellow-500">
            {t('documentPanel.reindexDocuments.note')}
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={() => setOpen(false)} disabled={isReindexing}>
            {t('common.cancel')}
          </Button>
          <Button
            variant="default"
            onClick={handleReindex}
            disabled={isReindexing}
          >
            {isReindexing ? t('documentPanel.reindexDocuments.reindexing') : t('documentPanel.reindexDocuments.confirmButton')}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
