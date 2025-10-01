import React, { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, X, Image as ImageIcon } from 'lucide-react'

interface ImageUploadProps {
  onImageUpload: (file: File) => void
  loading: boolean
  uploadedImage: string | null
}

const ImageUpload: React.FC<ImageUploadProps> = ({ onImageUpload, loading, uploadedImage }) => {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      onImageUpload(acceptedFiles[0])
    }
  }, [onImageUpload])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.webp']
    },
    multiple: false,
    disabled: loading
  })

  const handleRemoveImage = () => {
    if (uploadedImage) {
      URL.revokeObjectURL(uploadedImage)
    }
  }

  return (
    <div className="space-y-4">
      {!uploadedImage ? (
        <div
          {...getRootProps()}
          className={`
            border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
            ${isDragActive 
              ? 'border-primary-400 bg-primary-50' 
              : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
            }
            ${loading ? 'opacity-50 cursor-not-allowed' : ''}
          `}
        >
          <input {...getInputProps()} />
          <div className="space-y-4">
            <div className="mx-auto w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center">
              <Upload className="h-8 w-8 text-gray-400" />
            </div>
            
            <div>
              <p className="text-lg font-medium text-gray-900">
                {isDragActive ? 'Drop the image here' : 'Upload crop image'}
              </p>
              <p className="text-sm text-gray-500 mt-1">
                Drag and drop or click to select
              </p>
            </div>
            
            <div className="text-xs text-gray-400">
              Supports JPG, PNG, WebP up to 10MB
            </div>
          </div>
        </div>
      ) : (
        <div className="relative">
          <div className="relative rounded-lg overflow-hidden bg-gray-100">
            <img
              src={uploadedImage}
              alt="Uploaded crop"
              className="w-full h-64 object-cover"
            />
            <button
              onClick={handleRemoveImage}
              className="absolute top-2 right-2 bg-white rounded-full p-1 shadow-md hover:bg-gray-50 transition-colors"
              disabled={loading}
            >
              <X className="h-4 w-4 text-gray-600" />
            </button>
          </div>
          
          <div className="mt-2 text-center">
            <p className="text-sm text-gray-600">
              Image uploaded successfully
            </p>
          </div>
        </div>
      )}
      
      {loading && (
        <div className="text-center py-4">
          <div className="inline-flex items-center space-x-2 text-primary-600">
            <div className="animate-spin rounded-full h-4 w-4 border-2 border-primary-600 border-t-transparent"></div>
            <span className="text-sm">Processing image...</span>
          </div>
        </div>
      )}
    </div>
  )
}

export default ImageUpload
