const BASE = '/api'

export async function fetchStructure() {
  const res = await fetch(`${BASE}/structure`)
  if (!res.ok) throw new Error('Failed to load course structure')
  return res.json()
}

export async function fetchHealth() {
  const res = await fetch('/health')
  if (!res.ok) throw new Error('Backend unreachable')
  return res.json()
}

export async function generateQuestions(payload) {
  const res = await fetch(`${BASE}/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  const data = await res.json()
  if (!res.ok) throw new Error(data.detail || 'Generation failed')
  return data
}

export async function uploadSyllabus(courseId, file) {
  const form = new FormData()
  form.append('course_id', courseId)
  form.append('file', file)
  const res = await fetch(`${BASE}/syllabus/upload`, { method: 'POST', body: form })
  const data = await res.json()
  if (!res.ok) throw new Error(data.detail || 'Syllabus upload failed')
  return data
}

export async function fetchSyllabus(courseId) {
  const res = await fetch(`${BASE}/syllabus/${courseId}`)
  if (res.status === 404) return null
  if (!res.ok) throw new Error('Failed to fetch syllabus')
  return res.json()
}

export async function listSyllabi() {
  const res = await fetch(`${BASE}/syllabi`)
  if (!res.ok) throw new Error('Failed to list syllabi')
  return res.json()
}

export async function generateModule(payload) {
  const res = await fetch(`${BASE}/generate/module`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  const data = await res.json()
  if (!res.ok) throw new Error(data.detail || 'Module generation failed')
  return data
}

export async function submitFeedback(items) {
  const res = await fetch(`${BASE}/feedback`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(items),
  })
  const data = await res.json()
  if (!res.ok) throw new Error(data.detail || 'Feedback submission failed')
  return data
}

export async function optimizePrompts() {
  const res = await fetch(`${BASE}/optimize`, { method: 'POST' })
  const data = await res.json()
  if (!res.ok) throw new Error(data.detail || 'Optimization failed')
  return data
}

export async function sheetsStatus() {
  const res = await fetch(`${BASE}/sheets/status`)
  if (!res.ok) throw new Error('Failed to get Sheets status')
  return res.json()
}

export async function sheetsAuth() {
  const res = await fetch(`${BASE}/sheets/auth`, { method: 'POST' })
  const data = await res.json()
  if (!res.ok) throw new Error(data.detail || 'Auth failed')
  return data
}

export async function sheetsLog(questions) {
  const res = await fetch(`${BASE}/sheets/log`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ questions }),
  })
  const data = await res.json()
  if (!res.ok) throw new Error(data.detail || 'Log failed')
  return data
}

export async function sheetsDashboard() {
  const res = await fetch(`${BASE}/sheets/dashboard`)
  const data = await res.json()
  if (!res.ok) throw new Error(data.detail || 'Dashboard fetch failed')
  return data
}

export async function downloadExcel(questions, meta) {
  const res = await fetch(`${BASE}/download/excel`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ questions, meta }),
  })
  if (!res.ok) throw new Error('Excel download failed')
  const driveUrl = res.headers.get('X-Drive-URL') || ''
  const driveErr = res.headers.get('X-Drive-Error') || ''
  const blob = await res.blob()
  const cd = res.headers.get('Content-Disposition') || ''
  const match = cd.match(/filename=(.+)/)
  const filename = match ? match[1] : 'questions.xlsx'
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
  return { driveUrl, driveErr }
}
