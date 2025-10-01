import React, { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, Leaf, AlertCircle, CheckCircle, Loader2 } from 'lucide-react'
import ImageUpload from '../components/ImageUpload'
import PredictionResult from '../components/PredictionResult'
import { predictDisease } from '../services/api'

interface PredictionData {
  disease_name: string
  confidence_score: number
  treatment_suggestion: string
}

export default function Home() {
  const [prediction, setPrediction] = useState<PredictionData | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [uploadedImage, setUploadedImage] = useState<string | null>(null)

  const handleImageUpload = useCallback(async (file: File) => {
    setLoading(true)
    setError(null)
    setPrediction(null)

    try {
      // Create preview URL
      const imageUrl = URL.createObjectURL(file)
      setUploadedImage(imageUrl)

      // Make prediction
      const result = await predictDisease(file)
      setPrediction(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred during prediction')
    } finally {
      setLoading(false)
    }
  }, [])

  const handleReset = () => {
    setPrediction(null)
    setError(null)
    setUploadedImage(null)
    if (uploadedImage) {
      URL.revokeObjectURL(uploadedImage)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center space-x-3">
            <div className="bg-primary-100 p-2 rounded-lg">
              <Leaf className="h-8 w-8 text-primary-600" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Crop Disease Detection</h1>
              <p className="text-gray-600">AI-powered plant health analysis</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Comprehensive Crop Disease Detection
          </h2>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto mb-6">
            Upload an image of your crop and get instant disease detection with treatment recommendations. 
            Our AI supports <strong>85+ disease classes</strong> across cereals, vegetables, fruits, legumes, and root crops.
          </p>
          
          {/* Crop Categories */}
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 max-w-4xl mx-auto">
            <div className="bg-green-50 rounded-lg p-3 border border-green-200">
              <h3 className="font-semibold text-green-800 text-sm">Cereals</h3>
              <p className="text-xs text-green-600">Wheat, Rice, Corn, Barley</p>
            </div>
            <div className="bg-blue-50 rounded-lg p-3 border border-blue-200">
              <h3 className="font-semibold text-blue-800 text-sm">Vegetables</h3>
              <p className="text-xs text-blue-600">Tomato, Potato, Pepper, Cucumber</p>
            </div>
            <div className="bg-orange-50 rounded-lg p-3 border border-orange-200">
              <h3 className="font-semibold text-orange-800 text-sm">Fruits</h3>
              <p className="text-xs text-orange-600">Apple, Citrus, Grape, Strawberry</p>
            </div>
            <div className="bg-purple-50 rounded-lg p-3 border border-purple-200">
              <h3 className="font-semibold text-purple-800 text-sm">Legumes</h3>
              <p className="text-xs text-purple-600">Soybean, Bean</p>
            </div>
            <div className="bg-yellow-50 rounded-lg p-3 border border-yellow-200">
              <h3 className="font-semibold text-yellow-800 text-sm">Root Crops</h3>
              <p className="text-xs text-yellow-600">Sweet Potato, Cassava</p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Upload Section */}
          <div className="space-y-6">
            <div className="card">
              <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                <Upload className="h-5 w-5 mr-2 text-primary-600" />
                Upload Crop Image
              </h3>
              
              <ImageUpload
                onImageUpload={handleImageUpload}
                loading={loading}
                uploadedImage={uploadedImage}
              />
            </div>

            {/* Instructions */}
            <div className="card bg-blue-50 border-blue-200">
              <h4 className="font-semibold text-blue-900 mb-2">Tips for Best Results:</h4>
              <ul className="text-sm text-blue-800 space-y-1">
                <li>• Use clear, well-lit photos of individual leaves</li>
                <li>• Ensure the leaf fills most of the frame</li>
                <li>• Avoid blurry or heavily shadowed images</li>
                <li>• Supported formats: JPG, PNG, WebP</li>
              </ul>
            </div>
          </div>

          {/* Results Section */}
          <div className="space-y-6">
            {loading && (
              <div className="card text-center">
                <Loader2 className="h-12 w-12 text-primary-600 animate-spin mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  Analyzing Your Image
                </h3>
                <p className="text-gray-600">
                  Our AI model is processing your crop image...
                </p>
              </div>
            )}

            {error && (
              <div className="card bg-red-50 border-red-200">
                <div className="flex items-start">
                  <AlertCircle className="h-5 w-5 text-red-600 mt-0.5 mr-3 flex-shrink-0" />
                  <div>
                    <h3 className="font-semibold text-red-900 mb-1">Error</h3>
                    <p className="text-red-800">{error}</p>
                    <button
                      onClick={handleReset}
                      className="mt-3 text-sm text-red-600 hover:text-red-800 underline"
                    >
                      Try again
                    </button>
                  </div>
                </div>
              </div>
            )}

            {prediction && (
              <PredictionResult
                prediction={prediction}
                onReset={handleReset}
              />
            )}

            {!loading && !error && !prediction && (
              <div className="card text-center text-gray-500">
                <Leaf className="h-12 w-12 text-gray-300 mx-auto mb-4" />
                <p>Upload an image to get started with disease detection</p>
              </div>
            )}
          </div>
        </div>

        {/* Features Section */}
        <div className="mt-16 grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="text-center">
            <div className="bg-primary-100 p-3 rounded-full w-12 h-12 mx-auto mb-4 flex items-center justify-center">
              <CheckCircle className="h-6 w-6 text-primary-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">85+ Diseases</h3>
            <p className="text-gray-600 text-sm">
              Comprehensive coverage across all major crop types
            </p>
          </div>
          
          <div className="text-center">
            <div className="bg-success-100 p-3 rounded-full w-12 h-12 mx-auto mb-4 flex items-center justify-center">
              <Leaf className="h-6 w-6 text-success-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Instant Results</h3>
            <p className="text-gray-600 text-sm">
              Get disease diagnosis and treatment suggestions in seconds
            </p>
          </div>
          
          <div className="text-center">
            <div className="bg-warning-100 p-3 rounded-full w-12 h-12 mx-auto mb-4 flex items-center justify-center">
              <AlertCircle className="h-6 w-6 text-warning-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Expert Advice</h3>
            <p className="text-gray-600 text-sm">
              Comprehensive treatment recommendations for each disease
            </p>
          </div>
          
          <div className="text-center">
            <div className="bg-purple-100 p-3 rounded-full w-12 h-12 mx-auto mb-4 flex items-center justify-center">
              <Upload className="h-6 w-6 text-purple-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Easy Upload</h3>
            <p className="text-gray-600 text-sm">
              Simple drag-and-drop interface for quick analysis
            </p>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-600">
            <p>&copy; 2024 Crop Disease Detection. Built with AI for farmers worldwide.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
