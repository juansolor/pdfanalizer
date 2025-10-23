import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

const API_BASE_URL = 'http://localhost:8000'

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [pdfList, setPdfList] = useState([])
  const [currentPdf, setCurrentPdf] = useState('')
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [loading, setLoading] = useState(false)
  const [apiStatus, setApiStatus] = useState('checking')
  const [queryStats, setQueryStats] = useState(null)
  const [analysisResult, setAnalysisResult] = useState(null)
  const [showAnalysis, setShowAnalysis] = useState(false)
  const [locations, setLocations] = useState([])
  const [pagesFound, setPagesFound] = useState([])

  useEffect(() => {
    checkApiStatus()
    loadPdfList()
  }, [])

  const checkApiStatus = async () => {
    try {
      console.log('Intentando conectar con:', API_BASE_URL)
      const response = await axios.get(`${API_BASE_URL}/`, {
        timeout: 5000
      })
      console.log('Respuesta del backend:', response.data)
      setApiStatus('connected')
    } catch (error) {
      console.error('Error connecting to API:', error.message)
      if (error.code === 'ERR_NETWORK') {
        console.error('Error de red - El backend no está accesible')
      }
      if (error.response) {
        console.error('Respuesta de error:', error.response.status, error.response.data)
      }
      setApiStatus('disconnected')
    }
  }

  const loadPdfList = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/list-pdfs`)
      setPdfList(response.data.pdfs)
    } catch (error) {
      console.error('Error loading PDF list:', error)
    }
  }

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0])
  }

  const handleUpload = async () => {
    if (!selectedFile) {
      alert('Por favor selecciona un archivo PDF')
      return
    }

    const formData = new FormData()
    formData.append('file', selectedFile)

    try {
      setLoading(true)
      const response = await axios.post(`${API_BASE_URL}/upload-pdf`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      
      alert('Archivo subido correctamente')
      setSelectedFile(null)
      loadPdfList()
      document.getElementById('file-input').value = ''
    } catch (error) {
      console.error('Error uploading file:', error)
      alert(`Error al subir archivo: ${error.response?.data?.detail || error.message}`)
    } finally {
      setLoading(false)
    }
  }

  const handleQuery = async () => {
    if (!question || !currentPdf) {
      alert('Por favor selecciona un PDF y escribe una pregunta')
      return
    }

    try {
      setLoading(true)
      setAnswer('')
      setQueryStats(null)
      setLocations([])
      setPagesFound([])
      
      const response = await axios.post(`${API_BASE_URL}/query`, {
        question: question,
        filename: currentPdf
      })
      
      setAnswer(response.data.answer)
      setLocations(response.data.locations || [])
      setPagesFound(response.data.pages_found || [])
      setQueryStats({
        matches: response.data.total_matches || 0,
        keywords: response.data.keywords || []
      })
    } catch (error) {
      console.error('Error querying PDF:', error)
      const errorMsg = error.response?.data?.detail || error.message
      setAnswer(`❌ Error: ${errorMsg}`)
      alert(`Error al procesar consulta: ${errorMsg}`)
    } finally {
      setLoading(false)
    }
  }

  const openPdfAtPage = (page) => {
    const pdfUrl = `${API_BASE_URL}/view-pdf/${currentPdf}#page=${page}`
    window.open(pdfUrl, '_blank')
  }

  const handleAnalysis = async (analysisType) => {
    if (!currentPdf) {
      alert('Por favor selecciona un PDF primero')
      return
    }

    try {
      setLoading(true)
      setAnalysisResult(null)
      
      let response
      if (analysisType === 'all') {
        response = await axios.post(`${API_BASE_URL}/batch-analyze/${currentPdf}`)
      } else {
        response = await axios.post(`${API_BASE_URL}/analyze/${currentPdf}?analysis_type=${analysisType}`)
      }
      
      setAnalysisResult(response.data)
      setShowAnalysis(true)
    } catch (error) {
      console.error('Error analyzing PDF:', error)
      alert(`Error al analizar: ${error.response?.data?.detail || error.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>📄 PDF Query System</h1>
        <p>Sube PDFs y haz preguntas sobre su contenido con IA</p>
        <div className={`status-indicator ${apiStatus}`}>
          <span className="status-dot"></span>
          Backend: {apiStatus === 'connected' ? 'Conectado' : 
                   apiStatus === 'disconnected' ? 'Desconectado' : 'Verificando...'}
        </div>
      </header>

      <main className="app-main">
        {/* Sección de subida de archivos */}
        <section className="upload-section card">
          <h2>📤 Subir PDF</h2>
          <div className="upload-container">
            <input 
              id="file-input"
              type="file" 
              accept=".pdf" 
              onChange={handleFileChange}
              disabled={loading}
              className="file-input"
            />
            <button 
              onClick={handleUpload} 
              disabled={!selectedFile || loading}
              className="btn btn-primary"
            >
              {loading ? '⏳ Subiendo...' : '📤 Subir PDF'}
            </button>
          </div>
        </section>

        {/* Sección de consultas */}
        <section className="query-section card">
          <h2>🤖 Consultar PDF</h2>
          
          <div className="pdf-selector">
            <label htmlFor="pdf-select">Seleccionar PDF:</label>
            <select 
              id="pdf-select"
              value={currentPdf} 
              onChange={(e) => setCurrentPdf(e.target.value)}
              disabled={loading}
              className="select-input"
            >
              <option value="">-- Selecciona un PDF --</option>
              {pdfList.map((pdf, index) => (
                <option key={index} value={pdf}>{pdf}</option>
              ))}
            </select>
          </div>

          <div className="question-container">
            <label htmlFor="question-input">Tu pregunta:</label>
            <textarea
              id="question-input"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Escribe tu pregunta sobre el PDF..."
              disabled={loading}
              rows="3"
              className="textarea-input"
            />
            <button 
              onClick={handleQuery}
              disabled={!question || !currentPdf || loading}
              className="btn btn-secondary"
            >
              {loading ? '⏳ Procesando...' : '🔍 Hacer Pregunta'}
            </button>
          </div>

          {answer && (
            <div className="answer-container">
              <h3>💡 Respuesta:</h3>
              <div className="answer-text">
                {answer.split('\n').map((line, index) => (
                  <p key={index} className={line.startsWith('📌') || line.startsWith('📍') ? 'highlight-line' : ''}>
                    {line}
                  </p>
                ))}
              </div>
              
              {/* Mostrar ubicaciones en el PDF */}
              {locations && locations.length > 0 && (
                <div className="locations-container">
                  <h4>📍 Ubicaciones en el PDF:</h4>
                  <div className="locations-grid">
                    {locations.map((loc, index) => (
                      <div key={index} className="location-card">
                        <div className="location-header">
                          <span className="page-badge">Página {loc.page}</span>
                          <button 
                            onClick={() => openPdfAtPage(loc.page)}
                            className="btn-open-pdf"
                            title="Abrir PDF en esta página"
                          >
                            🔗 Abrir
                          </button>
                        </div>
                        <p className="location-preview">{loc.preview}</p>
                        <div className="keywords-found">
                          <small>Palabras encontradas: {loc.keywords.join(', ')}</small>
                        </div>
                      </div>
                    ))}
                  </div>
                  
                  {pagesFound && pagesFound.length > 0 && (
                    <div className="pages-summary">
                      <strong>📄 Páginas con coincidencias:</strong>
                      <div className="page-chips">
                        {pagesFound.map(page => (
                          <button 
                            key={page}
                            onClick={() => openPdfAtPage(page)}
                            className="page-chip"
                          >
                            Pág. {page}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
              
              {queryStats && (
                <div className="query-stats">
                  <p><strong>📊 Estadísticas:</strong></p>
                  <p>✓ Coincidencias encontradas: {queryStats.matches}</p>
                  {queryStats.keywords && queryStats.keywords.length > 0 && (
                    <p>🔍 Palabras clave buscadas: {queryStats.keywords.join(', ')}</p>
                  )}
                </div>
              )}
            </div>
          )}

          {/* Botones de análisis avanzado */}
          <div className="analysis-buttons">
            <h3>🔬 Análisis Avanzado</h3>
            <div className="button-grid">
              <button 
                onClick={() => handleAnalysis('summary')}
                disabled={!currentPdf || loading}
                className="btn btn-analysis"
              >
                📋 Resumen
              </button>
              <button 
                onClick={() => handleAnalysis('word_frequency')}
                disabled={!currentPdf || loading}
                className="btn btn-analysis"
              >
                📊 Palabras Frecuentes
              </button>
              <button 
                onClick={() => handleAnalysis('statistics')}
                disabled={!currentPdf || loading}
                className="btn btn-analysis"
              >
                📈 Estadísticas
              </button>
              <button 
                onClick={() => handleAnalysis('all')}
                disabled={!currentPdf || loading}
                className="btn btn-analysis btn-all"
              >
                🚀 Análisis Completo
              </button>
            </div>
          </div>

          {/* Resultados del análisis */}
          {showAnalysis && analysisResult && (
            <div className="analysis-container">
              <div className="analysis-header">
                <h3>📊 Resultados del Análisis</h3>
                <button 
                  onClick={() => setShowAnalysis(false)}
                  className="close-btn"
                >
                  ✕
                </button>
              </div>

              {/* Resumen */}
              {analysisResult.summary && (
                <div className="analysis-section">
                  <h4>📋 Resumen</h4>
                  <pre className="analysis-content">{analysisResult.summary}</pre>
                </div>
              )}

              {/* Palabras frecuentes */}
              {analysisResult.word_frequency && (
                <div className="analysis-section">
                  <h4>📊 Palabras Más Frecuentes</h4>
                  <div className="word-frequency-grid">
                    {analysisResult.word_frequency.map((item, index) => (
                      <div key={index} className="word-item">
                        <span className="word-rank">#{index + 1}</span>
                        <span className="word-text">{item.word}</span>
                        <span className="word-count">{item.count} veces</span>
                      </div>
                    ))}
                  </div>
                  {analysisResult.total_unique_words && (
                    <p className="unique-words">
                      Total de palabras únicas: {analysisResult.total_unique_words}
                    </p>
                  )}
                </div>
              )}

              {/* Estadísticas */}
              {analysisResult.statistics && (
                <div className="analysis-section">
                  <h4>📈 Estadísticas del Documento</h4>
                  <div className="stats-grid">
                    <div className="stat-item">
                      <span className="stat-label">Palabras totales</span>
                      <span className="stat-value">{analysisResult.statistics.total_words?.toLocaleString()}</span>
                    </div>
                    <div className="stat-item">
                      <span className="stat-label">Caracteres</span>
                      <span className="stat-value">{analysisResult.statistics.total_characters?.toLocaleString()}</span>
                    </div>
                    <div className="stat-item">
                      <span className="stat-label">Líneas</span>
                      <span className="stat-value">{analysisResult.statistics.total_lines?.toLocaleString()}</span>
                    </div>
                    {analysisResult.statistics.unique_words && (
                      <div className="stat-item">
                        <span className="stat-label">Palabras únicas</span>
                        <span className="stat-value">{analysisResult.statistics.unique_words?.toLocaleString()}</span>
                      </div>
                    )}
                    {analysisResult.statistics.average_word_length && (
                      <div className="stat-item">
                        <span className="stat-label">Promedio longitud</span>
                        <span className="stat-value">{analysisResult.statistics.average_word_length} chars</span>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          )}
        </section>

        {/* Lista de PDFs */}
        <section className="pdf-list card">
          <h3>📚 PDFs Disponibles ({pdfList.length})</h3>
          <div className="pdf-grid">
            {pdfList.length > 0 ? (
              pdfList.map((pdf, index) => (
                <div key={index} className="pdf-item">
                  <span className="pdf-icon">📄</span>
                  <span className="pdf-name">{pdf}</span>
                </div>
              ))
            ) : (
              <p className="no-pdfs">No hay PDFs subidos aún</p>
            )}
          </div>
        </section>
      </main>
    </div>
  )
}

export default App
