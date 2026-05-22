import { useState, useRef } from 'react'
import { uploadSyllabus } from '../api/client.js'

export default function SyllabusPanel({ courses, onClose, onUploaded }) {
  const [courseId,   setCourseId]   = useState('')
  const [uploading,  setUploading]  = useState(false)
  const [uploadMsg,  setUploadMsg]  = useState('')
  const [uploadError,setUploadError]= useState('')
  const [structure,  setStructure]  = useState(null)
  const fileRef = useRef(null)

  async function handleUpload(e) {
    const file = e.target.files?.[0]
    if (!file || !courseId) return
    setUploading(true); setUploadMsg(''); setUploadError(''); setStructure(null)
    try {
      const data = await uploadSyllabus(courseId, file)
      setStructure(data.structure)
      setUploadMsg('Syllabus parsed successfully.')
      if (onUploaded) onUploaded(courseId, data.structure)
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
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl mx-4 overflow-hidden flex flex-col max-h-[90vh]">

        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-100 flex items-center justify-between shrink-0">
          <div>
            <h2 className="text-sm font-bold text-gray-800">Upload Syllabus</h2>
            <p className="text-xs text-gray-400 mt-0.5">Extract CO definitions and unit structure from a PDF, DOCX, or TXT file</p>
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

          {/* Upload form */}
          <div className="border border-gray-200 rounded-xl p-4 space-y-3">
            <p className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">Upload syllabus document</p>

            {/* Course selector */}
            <div>
              <label className="text-[10px] font-bold text-gray-400 uppercase tracking-wider block mb-1">Course</label>
              <select
                value={courseId}
                onChange={e => setCourseId(e.target.value)}
                className="w-full text-sm border border-gray-200 rounded-lg px-3 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-blue-400"
              >
                <option value="">Select course…</option>
                {(courses || []).map(c => (
                  <option key={c.id} value={c.id}>{c.display}</option>
                ))}
              </select>
            </div>

            {/* File picker */}
            <div>
              <label className="text-[10px] font-bold text-gray-400 uppercase tracking-wider block mb-1">Syllabus file (PDF / DOCX / TXT)</label>
              <input
                ref={fileRef}
                type="file"
                accept=".pdf,.docx,.doc,.txt"
                onChange={handleUpload}
                disabled={!courseId || uploading}
                className="w-full text-xs text-gray-600 file:mr-3 file:text-xs file:font-semibold file:bg-blue-50 file:text-blue-700 file:border file:border-blue-200 file:rounded-lg file:px-3 file:py-1.5 file:cursor-pointer hover:file:bg-blue-100 disabled:opacity-50 cursor-pointer"
              />
            </div>

            {uploading && (
              <div className="flex items-center gap-2 text-xs text-blue-600">
                <span className="w-3 h-3 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
                Parsing syllabus with AI…
              </div>
            )}
            {uploadMsg && (
              <p className="text-xs text-emerald-700 bg-emerald-50 border border-emerald-100 rounded-lg px-3 py-2">{uploadMsg}</p>
            )}
            {uploadError && (
              <p className="text-xs text-red-600 bg-red-50 border border-red-100 rounded-lg px-3 py-2">{uploadError}</p>
            )}
          </div>

          {/* Parsed structure preview */}
          {structure && (
            <div className="space-y-4">
              {/* Course name */}
              <div>
                <p className="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1">Course name</p>
                <p className="text-sm text-gray-800 font-semibold">{structure.course_name}</p>
              </div>

              {/* CO definitions */}
              {structure.co_definitions && Object.keys(structure.co_definitions).length > 0 && (
                <div>
                  <p className="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-2">Course outcomes</p>
                  <div className="rounded-xl border border-gray-100 overflow-hidden divide-y divide-gray-50">
                    {Object.entries(structure.co_definitions).map(([co, desc]) => (
                      <div key={co} className="flex gap-3 px-4 py-2.5">
                        <span className="text-xs font-bold text-blue-700 shrink-0 w-8">{co}</span>
                        <span className="text-xs text-gray-600 leading-relaxed">{desc}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Units */}
              {structure.units && structure.units.length > 0 && (
                <div>
                  <p className="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-2">Units &amp; topics</p>
                  <div className="space-y-3">
                    {structure.units.map((unit, ui) => (
                      <div key={ui} className="rounded-xl border border-gray-100 overflow-hidden">
                        <div className="px-4 py-2.5 bg-slate-50 flex items-center justify-between">
                          <div>
                            <span className="text-xs font-bold text-gray-700">Unit {unit.unit_number}: {unit.unit_name}</span>
                          </div>
                          <span className="text-[10px] font-bold text-blue-600 bg-blue-50 border border-blue-200 rounded px-2 py-0.5">{unit.co}</span>
                        </div>
                        {unit.topics && unit.topics.length > 0 && (
                          <div className="divide-y divide-gray-50">
                            {unit.topics.map((topic, ti) => (
                              <div key={ti} className="px-4 py-2.5">
                                <p className="text-xs font-semibold text-gray-700 mb-1">{topic.topic_name}</p>
                                {topic.description && (
                                  <p className="text-[10px] text-gray-400 mb-1.5 leading-relaxed">{topic.description}</p>
                                )}
                                <div className="flex flex-wrap gap-1">
                                  {(topic.recommended_question_types || []).map(qt => (
                                    <span key={qt} className="text-[9px] font-semibold bg-violet-50 text-violet-700 border border-violet-200 rounded px-1.5 py-0.5">{qt}</span>
                                  ))}
                                  {topic.marks && (
                                    <span className="text-[9px] font-semibold bg-amber-50 text-amber-700 border border-amber-200 rounded px-1.5 py-0.5">{topic.marks}M</span>
                                  )}
                                </div>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {structure.notes && (
                <div>
                  <p className="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1">Notes</p>
                  <p className="text-xs text-gray-500 leading-relaxed">{structure.notes}</p>
                </div>
              )}
            </div>
          )}
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
