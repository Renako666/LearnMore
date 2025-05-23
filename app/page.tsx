"use client"

import { useEffect } from 'react'

export default function HomePage() {
  useEffect(() => {
    // Load Chart.js
    const chartScript = document.createElement('script')
    chartScript.src = 'https://cdn.jsdelivr.net/npm/chart.js'
    chartScript.async = true
    document.head.appendChild(chartScript)

  
    chartScript.onload = () => {
      console.log('Charts initialized');
    
    }

    return () => {
      document.head.removeChild(chartScript)
    }
  }, [])

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Welcome to Learning Platform</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Add course cards or other content here */}
      </div>
    </div>
  )
}
