import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogFooter
} from '@/components/ui/Dialog'
import Button from '@/components/ui/Button'
import { AlertTriangle } from 'lucide-react'

export interface DocumentConflictDialogProps {
  open: boolean
  fileName: string
  conflictDocId: string
  onReplace: () => Promise<void>
  onCancel: () => void
}

export default function DocumentConflictDialog({
  open,
  fileName,
  conflictDocId,
  onReplace,
  onCancel
}: DocumentConflictDialogProps) {
  const { t } = useTranslation()
  const [isProcessing, setIsProcessing] = useState(false)

  const handleReplace = async () => {
    setIsProcessing(true)
    try {
      await onReplace()
    } finally {
      setIsProcessing(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={(isOpen) => {
      if (!isOpen && !isProcessing) {
        onCancel()
      }
    }}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <div className="flex items-center gap-2">
            <AlertTriangle className="h-5 w-5 text-amber-600" />
            <DialogTitle>{t('documentPanel.conflict.title', 'Document Conflict')}</DialogTitle>
          </div>
          <DialogDescription>
            {t('documentPanel.conflict.description', 'This file already exists in the system')}
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4 py-4">
          <div className="rounded-md bg-amber-50 dark:bg-amber-950 p-3">
            <p className="text-sm font-medium text-amber-900 dark:text-amber-200">
              {t('documentPanel.conflict.fileExists', 'File already exists')}: <span className="font-mono">{fileName}</span>
            </p>
          </div>

          <div className="space-y-2 text-sm text-muted-foreground">
            <p>{t('documentPanel.conflict.conflictMessage', 'A document with the same filename exists with ID')}:</p>
            <p className="font-mono text-xs bg-muted p-2 rounded break-all">{conflictDocId}</p>
          </div>

          <div className="bg-blue-50 dark:bg-blue-950 rounded-md p-3">
            <p className="text-sm text-blue-900 dark:text-blue-200">
              {t('documentPanel.conflict.replaceExplanation', 'If you replace it, the old document and all its associated data (entities, relationships, indexed content) will be permanently deleted and replaced with this new version.')}
            </p>
          </div>
        </div>

        <DialogFooter className="flex gap-2 justify-end">
          <Button
            variant="outline"
            onClick={onCancel}
            disabled={isProcessing}
          >
            {t('documentPanel.conflict.keepOld', 'Keep Old')}
          </Button>
          <Button
            variant="destructive"
            onClick={handleReplace}
            disabled={isProcessing}
          >
            {isProcessing ? (
              <>
                <span className="inline-block animate-spin mr-2">⏳</span>
                {t('documentPanel.conflict.replacing', 'Replacing...')}
              </>
            ) : (
              t('documentPanel.conflict.replaceNew', 'Replace with New')
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
