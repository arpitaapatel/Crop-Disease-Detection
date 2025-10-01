import React from 'react'
import { CheckCircle, AlertTriangle, RotateCcw, ExternalLink } from 'lucide-react'

interface PredictionData {
  disease_name: string
  confidence_score: number
  treatment_suggestion: string
}

interface PredictionResultProps {
  prediction: PredictionData
  onReset: () => void
}

const PredictionResult: React.FC<PredictionResultProps> = ({ prediction, onReset }) => {
  const { disease_name, confidence_score, treatment_suggestion } = prediction
  
  const isHealthy = disease_name.toLowerCase().includes('healthy')
  const confidenceColor = confidence_score >= 80 ? 'text-success-600' : 
                         confidence_score >= 60 ? 'text-warning-600' : 'text-danger-600'
  
  const confidenceBg = confidence_score >= 80 ? 'bg-success-100' : 
                      confidence_score >= 60 ? 'bg-warning-100' : 'bg-danger-100'

  return (
    <div className="space-y-6">
      {/* Main Result Card */}
      <div className="card">
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center space-x-3">
            <div className={`p-2 rounded-lg ${isHealthy ? 'bg-success-100' : 'bg-danger-100'}`}>
              {isHealthy ? (
                <CheckCircle className="h-6 w-6 text-success-600" />
              ) : (
                <AlertTriangle className="h-6 w-6 text-danger-600" />
              )}
            </div>
            <div>
              <h3 className="text-xl font-semibold text-gray-900">
                {isHealthy ? 'Plant is Healthy!' : 'Disease Detected'}
              </h3>
              <p className="text-gray-600">
                {isHealthy ? 'No signs of disease found' : 'Potential disease identified'}
              </p>
            </div>
          </div>
          
          <button
            onClick={onReset}
            className="btn-secondary flex items-center space-x-2"
          >
            <RotateCcw className="h-4 w-4" />
            <span>New Analysis</span>
          </button>
        </div>

        {/* Disease Name */}
        <div className="mb-4">
          <h4 className="text-lg font-medium text-gray-900 mb-2">Disease Name:</h4>
          <div className="bg-gray-50 rounded-lg p-3">
            <p className="font-medium text-gray-800">{disease_name}</p>
          </div>
        </div>

        {/* Confidence Score */}
        <div className="mb-6">
          <h4 className="text-lg font-medium text-gray-900 mb-2">Confidence Score:</h4>
          <div className="flex items-center space-x-4">
            <div className={`px-4 py-2 rounded-lg ${confidenceBg}`}>
              <span className={`font-semibold ${confidenceColor}`}>
                {confidence_score}%
              </span>
            </div>
            <div className="flex-1 bg-gray-200 rounded-full h-2">
              <div 
                className={`h-2 rounded-full transition-all duration-500 ${
                  confidence_score >= 80 ? 'bg-success-500' : 
                  confidence_score >= 60 ? 'bg-warning-500' : 'bg-danger-500'
                }`}
                style={{ width: `${confidence_score}%` }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Treatment Suggestion */}
      <div className="card">
        <h4 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
          <ExternalLink className="h-5 w-5 mr-2 text-primary-600" />
          Treatment Recommendation
        </h4>
        
        <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
          <div className="prose prose-sm max-w-none">
            <p className="text-gray-800 whitespace-pre-line leading-relaxed">
              {treatment_suggestion}
            </p>
          </div>
        </div>
        
        <div className="mt-4 p-3 bg-yellow-50 rounded-lg border border-yellow-200">
          <p className="text-sm text-yellow-800">
            <strong>Disclaimer:</strong> This is an AI-powered diagnosis tool. 
            For critical decisions, please consult with agricultural experts or plant pathologists.
          </p>
        </div>
      </div>

      {/* Additional Actions */}
      <div className="card bg-gray-50">
        <h4 className="text-lg font-medium text-gray-900 mb-3">Next Steps:</h4>
        <ul className="space-y-2 text-sm text-gray-700">
          <li className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-primary-500 rounded-full"></div>
            <span>Take action based on the treatment recommendations</span>
          </li>
          <li className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-primary-500 rounded-full"></div>
            <span>Monitor your plants regularly for changes</span>
          </li>
          <li className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-primary-500 rounded-full"></div>
            <span>Consider consulting local agricultural extension services</span>
          </li>
          <li className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-primary-500 rounded-full"></div>
            <span>Upload more images for additional analysis</span>
          </li>
        </ul>
      </div>
    </div>
  )
}

export default PredictionResult
