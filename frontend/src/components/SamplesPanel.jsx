import { useState, useEffect, useRef } from 'react'

const ALL_TYPES = [
  'Fill in the Blanks',
  'Cloze',
  'Error Correction',
  'Sentence Arrangement',
  'Jumbled Sentences',
  'Jumbled Words',
  'Sentence Conversion',
  'Sentence Correction / MCQ',
]

export default function SamplesPanel({ onClose }) {
  const [counts,       setCounts]       = useState({})
  const [loadingInfo,  setLoadingInfo]  = useState(true)
  const [selectedType, setSelectedType] = useState('')
  const [uploading,    setUploading]    = useState(false)
  const [uploadMsg,    setUploadMsg]    = useState('')
  const [uploadError,  setUploadError]  = useState('')
  const fileRef = useRef(null)

  async function fetchCounts() {
    setLoadingInfo(true)
    try {
      const res = await fetch('/api/samples')
      if (res.ok) setCounts(await res.json())
    } catch { /* silent */ }
    finally { setLoadingInfo(false) }
  }

  useEffect(() => { fetchCounts() }, [])

  async function handleUpload(e) {
    const file = e.target.files?.[0]
    if (!file || !selectedType) return
    setUploading(true); setUploadMsg(''); setUploadError('')
    const form = new FormData()
    form.append('question_type', selectedType)
    form.append('file', file)
    try {
      const res = await fetch('/api/samples/upload', { method: 'POST', body: form })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Upload failed')
      setUploadMsg(`Added ${data.added} sample${data.added !== 1 ? 's' : ''} (${data.total} total for ${selectedType})`)
      await fetchCounts()
    } catch (err) {
      setUploadError(err.message)
    } finally {
      setUploading(false)
      if (fileRef.current) fileRef.current.value = ''
    }
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm"
      onClick={e => { if (e.target === e.currentTarget) onClose() }}
    >
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-lg mx-4 overflow-hidden flex flex-col max-h-[90vh]">

        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-100 flex items-center justify-between shrink-0">
          <div>
            <h2 className="text-sm font-bold text-gray-800">Sample Questions</h2>
            <p className="text-xs text-gray-400 mt-0.5">Few-shot examples used during generation</p>
          </div>
          <button
            onClick={onClose}
            className="w-7 h-7 flex items-center justify-center text-gray-400 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Body */}
        <div className="overflow-y-auto flex-1 px-6 py-4 space-y-5">

          {/* Current sample counts */}
          <div>
            <p className="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-2">Sample counts per question type</p>
            {loadingInfo ? (
              <p className="text-xs text-gray-400">Loading…</p>
            ) : (
              <div className="rounded-xl border border-gray-100 overflow-hidden divide-y divide-gray-50">
                {ALL_TYPES.map(type => {
                  const n = counts[type] ?? 0
                  return (
                    <div key={type} className="flex items-center justify-between px-4 py-2.5">
                      <span className="text-xs text-gray-700">{type}</span>
                      <span className={`text-xs font-semibold tabular-nums ${n > 0 ? 'text-emerald-600' : 'text-gray-300'}`}>
                        {n} sample{n !== 1 ? 's' : ''}
                      </span>
                    </div>
                  )
                })}
              </div>
            )}
          </div>

          {/* Upload section */}
          <div className="border border-gray-200 rounded-xl p-4 space-y-3">
            <p className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">Upload CSV samples</p>
            <p className="text-xs text-gray-500 leading-relaxed">
              CSV columns: <code className="bg-gray-100 rounded px-1">Question</code>,{' '}
              <code className="bg-gray-100 rounded px-1">Solution</code>,{' '}
              <code className="bg-gray-100 rounded px-1">Explanation</code>,{' '}
              <code className="bg-gray-100 rounded px-1">Difficulty</code>,{' '}
              <code className="bg-gray-100 rounded px-1">Bloom's Level</code>,{' '}
              <code className="bg-gray-100 rounded px-1">CO</code>
            </p>

            {/* Type selector */}
            <div>
              <label className="text-[10px] font-bold text-gray-400 uppercase tracking-wider block mb-1">Question type</label>
              <select
                value={selectedType}
                onChange={e => setSelectedType(e.target.value)}
                className="w-full text-sm border border-gray-200 rounded-lg px-3 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-blue-400"
              >
                <option value="">Select question type…</option>
                {ALL_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
              </select>
            </div>

            {/* File picker */}
            <div>
              <label className="text-[10px] font-bold text-gray-400 uppercase tracking-wider block mb-1">CSV file</label>
              <input
                ref={fileRef}
                type="file"
                accept=".csv"
                onChange={handleUpload}
                disabled={!selectedType || uploading}
                className="w-full text-xs text-gray-600 file:mr-3 file:text-xs file:font-semibold file:bg-blue-50 file:text-blue-700 file:border file:border-blue-200 file:rounded-lg file:px-3 file:py-1.5 file:cursor-pointer hover:file:bg-blue-100 disabled:opacity-50 cursor-pointer"
              />
            </div>

            {uploading && (
              <div className="flex items-center gap-2 text-xs text-blue-600">
                <span className="w-3 h-3 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
                Uploading…
              </div>
            )}
            {uploadMsg && (
              <p className="text-xs text-emerald-700 bg-emerald-50 border border-emerald-100 rounded-lg px-3 py-2">{uploadMsg}</p>
            )}
            {uploadError && (
              <p className="text-xs text-red-600 bg-red-50 border border-red-100 rounded-lg px-3 py-2">{uploadError}</p>
            )}
          </div>

        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-gray-100 shrink-0">
          <button
            onClick={onClose}
            className="w-full text-xs font-semibold text-gray-500 hover:text-gray-700 border border-gray-200 hover:border-gray-300 py-2 rounded-lg transition-colors"
          >Close</button>
        </div>
      </div>
    </div>
  )
}
