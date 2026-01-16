import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Loader2, AlertCircle, Check, X } from 'lucide-react'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle
} from '@/components/ui/Dialog'
import Button from '@/components/ui/Button'
import { DuplicateEntity } from '@/api/lightrag'

interface DuplicateDetectionDialogProps {
  open: boolean
  entityName: string
  duplicates: DuplicateEntity[]
  isLoading: boolean
  onOpenChange: (open: boolean) => void
  onMerge: (sourceEntity: string, targetEntity: string) => Promise<void>
  onKeep: () => void
}

/**
 * HITL Duplicate Detection Dialog
 * Shows potential duplicate entities and allows user to choose whether to merge or keep separate
 */
const DuplicateDetectionDialog = ({
  open,
  entityName,
  duplicates,
  isLoading,
  onOpenChange,
  onMerge,
  onKeep
}: DuplicateDetectionDialogProps) => {
  const { t } = useTranslation()
  const [mergingWith, setMergingWith] = useState<string | null>(null)

  const handleMerge = async (targetEntity: string) => {
    setMergingWith(targetEntity)
    try {
      await onMerge(entityName, targetEntity)
    } finally {
      setMergingWith(null)
    }
  }

  const getSimilarityBadge = (similarity: number): string => {
    if (similarity >= 0.9) return 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300'
    if (similarity >= 0.8) return 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300'
    return 'bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-300'
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-3xl max-h-[80vh] overflow-hidden flex flex-col">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <AlertCircle className="h-5 w-5" />
            {t('graphPanel.duplicateDetection.title')}
          </DialogTitle>
          <DialogDescription>
            {t('graphPanel.duplicateDetection.description', { entityName })}
          </DialogDescription>
        </DialogHeader>

        <div className="flex-1 overflow-y-auto py-4">
          {isLoading ? (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
            </div>
          ) : duplicates.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-8 text-center">
              <Check className="h-12 w-12 text-green-500 mb-2" />
              <p className="text-sm font-medium">
                {t('graphPanel.duplicateDetection.noDuplicates')}
              </p>
              <p className="text-xs text-muted-foreground mt-1">
                {t('graphPanel.duplicateDetection.noDuplicatesHint')}
              </p>
            </div>
          ) : (
            <div className="space-y-3">
              <div className="text-sm text-muted-foreground mb-3">
                {t('graphPanel.duplicateDetection.foundCount', { count: duplicates.length })}
              </div>

              {duplicates.map((duplicate, index) => (
                <div
                  key={index}
                  className="border border-border rounded-lg p-4 hover:bg-muted/50 transition-colors"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1 space-y-2">
                      <div className="flex items-center gap-2">
                        <h4 className="font-semibold text-sm">
                          {duplicate.entity_name}
                        </h4>
                        <span
                          className={`px-2 py-0.5 rounded text-xs font-medium ${getSimilarityBadge(duplicate.similarity)}`}
                        >
                          {Math.round(duplicate.similarity * 100)}% {t('graphPanel.duplicateDetection.similar')}
                        </span>
                        {duplicate.entity_type && (
                          <span className="px-2 py-0.5 rounded text-xs bg-muted text-muted-foreground">
                            {duplicate.entity_type}
                          </span>
                        )}
                      </div>

                      <p className="text-sm text-muted-foreground line-clamp-2">
                        {duplicate.description || t('graphPanel.duplicateDetection.noDescription')}
                      </p>
                    </div>

                    <div className="flex flex-col gap-2">
                      <Button
                        size="sm"
                        variant="default"
                        onClick={() => handleMerge(duplicate.entity_name)}
                        disabled={mergingWith !== null}
                        className="whitespace-nowrap"
                      >
                        {mergingWith === duplicate.entity_name ? (
                          <>
                            <Loader2 className="h-3 w-3 mr-1 animate-spin" />
                            {t('common.merging')}
                          </>
                        ) : (
                          <>
                            <Check className="h-3 w-3 mr-1" />
                            {t('graphPanel.duplicateDetection.autoMerge')}
                          </>
                        )}
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={onKeep}
                        disabled={mergingWith !== null}
                        className="whitespace-nowrap"
                      >
                        <X className="h-3 w-3 mr-1" />
                        {t('graphPanel.duplicateDetection.keepSeparate')}
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <DialogFooter className="flex-shrink-0">
          <Button
            type="button"
            variant="outline"
            onClick={() => onOpenChange(false)}
            disabled={mergingWith !== null}
          >
            {duplicates.length === 0 
              ? t('common.close')
              : t('graphPanel.duplicateDetection.reviewLater')
            }
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}

export default DuplicateDetectionDialog
