import { useState, useMemo } from 'react'

export default function Sidebar({ courses, selection, onSelect }) {
  const [openCourse, setOpenCourse] = useState('')
  const [openModule, setOpenModule] = useState('')
  const [query, setQuery] = useState('')

  function toggleCourse(id) {
    setOpenCourse(p => p === id ? '' : id)
    setOpenModule('')
  }

  function toggleModule(id) {
    setOpenModule(p => p === id ? '' : id)
  }

  // Flat list of all topics for search results
  const allTopics = useMemo(() => {
    const results = []
    courses.forEach(c => {
      c.modules.forEach(m => {
        m.topics.forEach(t => {
          results.push({ course: c, module: m, topic: t })
        })
      })
    })
    return results
  }, [courses])

  const q = query.trim().toLowerCase()
  const searchResults = q
    ? allTopics.filter(
        ({ course, module, topic }) =>
          topic.display.toLowerCase().includes(q) ||
          module.display.toLowerCase().includes(q) ||
          course.display.toLowerCase().includes(q)
      )
    : []

  if (!courses.length) {
    return <p className="text-xs text-gray-400 px-4 py-3">No courses found.</p>
  }

  return (
    <div className="flex flex-col h-full">
      {/* Search input */}
      <div className="px-3 py-2 border-b border-gray-100">
        <div className="flex items-center gap-2 bg-gray-50 border border-gray-200 rounded-lg px-2.5 py-1.5">
          <svg className="w-3 h-3 text-gray-300 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            type="text"
            placeholder="Search topics..."
            value={query}
            onChange={e => setQuery(e.target.value)}
            className="flex-1 text-xs bg-transparent text-gray-700 placeholder:text-gray-300 focus:outline-none min-w-0"
          />
          {query && (
            <button
              onClick={() => setQuery('')}
              className="text-gray-300 hover:text-gray-500 leading-none text-base shrink-0"
            >×</button>
          )}
        </div>
      </div>

      <nav className="flex-1 overflow-y-auto">
        {/* ── Search results ── */}
        {q ? (
          <div className="py-1">
            {searchResults.length === 0 ? (
              <p className="text-xs text-gray-400 px-4 py-4 text-center">No topics match "{query}"</p>
            ) : (
              <>
                <p className="text-[10px] font-semibold text-gray-400 uppercase tracking-wider px-3 py-1.5">
                  {searchResults.length} result{searchResults.length !== 1 ? 's' : ''}
                </p>
                {searchResults.map(({ course, module, topic }) => {
                  const active =
                    selection?.course === course.id &&
                    selection?.module === module.id &&
                    selection?.topic === topic.id
                  return (
                    <button
                      key={`${course.id}/${module.id}/${topic.id}`}
                      onClick={() => onSelect(course.id, module.id, topic.id)}
                      className={`w-full text-left px-3 py-2.5 transition-colors border-b border-gray-50 last:border-0
                        ${active ? 'bg-blue-600 text-white' : 'hover:bg-gray-50 text-gray-700'}`}
                    >
                      <div className="flex items-center gap-2">
                        <span className={`text-[9px] shrink-0 ${
                          topic.has_material
                            ? active ? 'text-green-300' : 'text-green-500'
                            : active ? 'text-white/40' : 'text-gray-300'
                        }`}>
                          {topic.has_material ? '●' : '○'}
                        </span>
                        <div className="min-w-0">
                          <p className="text-xs font-medium truncate">{topic.display}</p>
                          <p className={`text-[10px] truncate mt-px ${active ? 'text-blue-200' : 'text-gray-400'}`}>
                            {course.display} › {module.display}
                          </p>
                        </div>
                      </div>
                    </button>
                  )
                })}
              </>
            )}
          </div>
        ) : (
          /* ── Full tree ── */
          <div className="py-1">
            {courses.map(course => (
              <div key={course.id}>
                <button
                  onClick={() => toggleCourse(course.id)}
                  className={`w-full flex items-center gap-1.5 px-3 py-2 text-xs font-semibold text-left transition-colors
                    ${openCourse === course.id ? 'text-blue-800 bg-blue-50' : 'text-gray-600 hover:bg-gray-50'}`}
                >
                  <span className={`text-[9px] transition-transform duration-150 ${openCourse === course.id ? 'rotate-90' : ''}`}>▶</span>
                  <span className="truncate">{course.display}</span>
                </button>

                {openCourse === course.id && course.modules.map(mod => (
                  <div key={mod.id}>
                    <button
                      onClick={() => toggleModule(mod.id)}
                      className={`w-full flex items-center gap-1.5 pl-6 pr-3 py-1.5 text-xs text-left transition-colors
                        ${openModule === mod.id ? 'text-blue-700 font-medium' : 'text-gray-500 hover:bg-gray-50'}`}
                    >
                      <span className={`text-[8px] transition-transform duration-150 ${openModule === mod.id ? 'rotate-90' : ''}`}>▶</span>
                      <span className="truncate">{mod.display}</span>
                    </button>

                    {openModule === mod.id && mod.topics.map(topic => {
                      const active =
                        selection?.course === course.id &&
                        selection?.module === mod.id &&
                        selection?.topic === topic.id
                      return (
                        <button
                          key={topic.id}
                          onClick={() => onSelect(course.id, mod.id, topic.id)}
                          className={`w-full flex items-center gap-2 pl-10 pr-3 py-1.5 text-xs text-left transition-colors
                            ${active ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'}`}
                        >
                          <span className={`text-[9px] shrink-0 ${
                            topic.has_material
                              ? active ? 'text-green-300' : 'text-green-500'
                              : active ? 'text-white/40' : 'text-gray-300'
                          }`}>
                            {topic.has_material ? '●' : '○'}
                          </span>
                          <span className="truncate">{topic.display}</span>
                        </button>
                      )
                    })}
                  </div>
                ))}
              </div>
            ))}
          </div>
        )}
      </nav>
    </div>
  )
}
