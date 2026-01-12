interface QuickActionsProps {
  onActionClick: (query: string) => void
}

export default function QuickActions({ onActionClick }: QuickActionsProps) {
  const quickActions = [
    { label: '🔍 Top CS Colleges', query: 'Show me top Computer Science colleges' },
    { label: '💰 Budget Friendly', query: 'Find affordable colleges under 2 lakhs' },
    { label: '🏆 Top NIRF Ranked', query: 'Show me top 50 NIRF ranked colleges' },
    { label: '🏛️ Government Colleges', query: 'Find government engineering colleges' },
    { label: '📍 Colleges in Karnataka', query: 'Show me engineering colleges in Karnataka' },
  ]

  return (
    <div className="bg-white border-t border-gray-200 px-4 py-3 overflow-x-auto">
      <div className="flex gap-2 min-w-max">
        {quickActions.map((action, index) => (
          <button
            key={index}
            onClick={() => onActionClick(action.query)}
            className="quick-action-btn whitespace-nowrap"
          >
            {action.label}
          </button>
        ))}
      </div>
    </div>
  )
}
