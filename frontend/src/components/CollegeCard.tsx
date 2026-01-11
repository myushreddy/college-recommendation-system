import type { College } from '@/types'

interface CollegeCardProps {
  college: College
}

export default function CollegeCard({ college }: CollegeCardProps) {
  return (
    <div className="college-card animate-slide-up">
      <div className="flex justify-between items-start mb-2">
        <h3 className="font-bold text-gray-900 text-lg leading-tight">
          {college.college_name}
        </h3>
        {college.nirf_rank && (
          <span className="bg-yellow-100 text-yellow-800 text-xs font-semibold px-2 py-1 rounded-full">
            NIRF #{college.nirf_rank}
          </span>
        )}
      </div>

      <div className="space-y-2 text-sm text-gray-600">
        <div className="flex items-center">
          <span className="mr-2">📍</span>
          <span>{college.city}, {college.state}</span>
        </div>

        {college.tier && (
          <div className="flex items-center">
            <span className="mr-2">🏆</span>
            <span className="font-medium text-primary-600">{college.tier}</span>
          </div>
        )}

        {college.ownership && (
          <div className="flex items-center">
            <span className="mr-2">🏛️</span>
            <span>{college.ownership}</span>
          </div>
        )}

        {college.average_fees !== null && college.average_fees !== undefined && (
          <div className="flex items-center">
            <span className="mr-2">💰</span>
            <span>₹{(college.average_fees / 100000).toFixed(2)}L / year</span>
          </div>
        )}

        {college.overall_score && (
          <div className="flex items-center">
            <span className="mr-2">⭐</span>
            <span>Score: {college.overall_score.toFixed(1)}/100</span>
          </div>
        )}
      </div>

      <div className="mt-3 pt-3 border-t border-gray-200 flex flex-wrap gap-2">
        {college.has_hostel && (
          <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full">
            🏠 Hostel
          </span>
        )}
        {college.has_library && (
          <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full">
            📚 Library
          </span>
        )}
        {college.has_gym && (
          <span className="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded-full">
            💪 Gym
          </span>
        )}
      </div>

      <button className="mt-4 w-full py-2 text-sm font-medium text-primary-600 hover:text-primary-700 hover:bg-primary-50 rounded-lg transition-colors duration-200 border border-primary-200">
        View Details →
      </button>
    </div>
  )
}
