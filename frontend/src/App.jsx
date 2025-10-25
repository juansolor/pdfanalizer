import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

// Configuración dinámica de API
// Detecta automáticamente si estás accediendo desde otra máquina en la red
const getApiBaseUrl = () => {
  const hostname = window.location.hostname
  
  // Si accedes desde localhost, usa localhost
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return 'http://localhost:8000'
  }
  
  // Si accedes desde una IP de red local, usa esa IP para el backend
  return `http://${hostname}:8000`
}

const API_BASE_URL = getApiBaseUrl()

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
  
  // Estados para búsqueda múltiple
  const [searchAll, setSearchAll] = useState(false)
  const [selectedPdfs, setSelectedPdfs] = useState([])
  const [multiResults, setMultiResults] = useState(null)
  const [isMultiSearch, setIsMultiSearch] = useState(false)

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
    if (!question) {
      alert('Por favor escribe una pregunta')
      return
    }

    // Búsqueda múltiple
    if (searchAll || selectedPdfs.length > 0) {
      try {
        setLoading(true)
        setAnswer('')
        setQueryStats(null)
        setMultiResults(null)
        setIsMultiSearch(true)
        
        const response = await axios.post(`${API_BASE_URL}/query-multiple`, {
          question: question,
          filenames: searchAll ? [] : selectedPdfs,
          search_all: searchAll
        })
        
        setAnswer(response.data.answer)
        setMultiResults(response.data.results || [])
        setQueryStats({
          matches: response.data.total_matches || 0,
          keywords: response.data.keywords || [],
          documents_found: response.data.documents_found || 0,
          comparison: response.data.comparison || {}
        })
      } catch (error) {
        console.error('Error querying multiple PDFs:', error)
        const errorMsg = error.response?.data?.detail || error.message
        setAnswer(`❌ Error: ${errorMsg}`)
        alert(`Error al procesar consulta múltiple: ${errorMsg}`)
      } finally {
        setLoading(false)
      }
      return
    }

    // Búsqueda individual
    if (!currentPdf) {
      alert('Por favor selecciona un PDF')
      return
    }

    try {
      setLoading(true)
      setAnswer('')
      setQueryStats(null)
      setLocations([])
      setPagesFound([])
      setIsMultiSearch(false)
      
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

  const togglePdfSelection = (pdfName) => {
    setSelectedPdfs(prev => {
      if (prev.includes(pdfName)) {
        return prev.filter(name => name !== pdfName)
      } else {
        return [...prev, pdfName]
      }
    })
  }

  const openMultiPdfAtPage = (filename, page) => {
    const pdfUrl = `${API_BASE_URL}/view-pdf/${filename}#page=${page}`
    window.open(pdfUrl, '_blank')
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
          
          {/* Opción de búsqueda múltiple */}
          <div className="multi-search-toggle">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={searchAll}
                onChange={(e) => {
                  setSearchAll(e.target.checked)
                  if (e.target.checked) {
                    setSelectedPdfs([])
                  }
                }}
                disabled={loading}
              />
              <span>🔍 Buscar en todos los PDFs</span>
            </label>
          </div>

          {!searchAll && (
            <>
              <div className="pdf-selector">
                <label htmlFor="pdf-select">Seleccionar PDF individual:</label>
                <select 
                  id="pdf-select"
                  value={currentPdf} 
                  onChange={(e) => setCurrentPdf(e.target.value)}
                  disabled={loading || selectedPdfs.length > 0}
                  className="select-input"
                >
                  <option value="">-- Selecciona un PDF --</option>
                  {pdfList.map((pdf, index) => (
                    <option key={index} value={pdf}>{pdf}</option>
                  ))}
                </select>
              </div>

              {pdfList.length > 1 && (
                <div className="multi-select-section">
                  <label>O selecciona múltiples PDFs para comparar:</label>
                  <div className="pdf-checkboxes">
                    {pdfList.map((pdf, index) => (
                      <label key={index} className="pdf-checkbox-item">
                        <input
                          type="checkbox"
                          checked={selectedPdfs.includes(pdf)}
                          onChange={() => togglePdfSelection(pdf)}
                          disabled={loading || currentPdf !== ''}
                        />
                        <span>{pdf}</span>
                      </label>
                    ))}
                  </div>
                  {selectedPdfs.length > 0 && (
                    <div className="selected-count">
                      ✓ {selectedPdfs.length} PDF(s) seleccionado(s)
                    </div>
                  )}
                </div>
              )}
            </>
          )}

          <div className="question-container">
            <label htmlFor="question-input">Tu pregunta:</label>
            <textarea
              id="question-input"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder={searchAll ? "Escribe tu pregunta para buscar en todos los PDFs..." : "Escribe tu pregunta sobre el PDF..."}
              disabled={loading}
              rows="3"
              className="textarea-input"
            />
            <button 
              onClick={handleQuery}
              disabled={!question || (!currentPdf && !searchAll && selectedPdfs.length === 0) || loading}
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
                  <p key={index} className={line.startsWith('📌') || line.startsWith('📍') || line.startsWith('📄') ? 'highlight-line' : ''}>
                    {line}
                  </p>
                ))}
              </div>
              
              {/* Resultados de búsqueda múltiple */}
              {isMultiSearch && multiResults && multiResults.length > 0 && (
                <div className="multi-results-container">
                  <h4>📚 Resultados por Documento:</h4>
                  {multiResults.map((docResult, idx) => (
                    <div key={idx} className="multi-doc-card">
                      <div className="multi-doc-header">
                        <h5>📄 {docResult.filename}</h5>
                        <div className="multi-doc-stats">
                          <span className="stat-badge matches">{docResult.matches} coincidencias</span>
                          <span className="stat-badge pages">{docResult.pages_found.length} páginas</span>
                        </div>
                      </div>
                      
                      <div className="multi-doc-pages">
                        <strong>Páginas con resultados:</strong>
                        <div className="page-chips">
                          {docResult.pages_found.slice(0, 10).map(page => (
                            <button 
                              key={page}
                              onClick={() => openMultiPdfAtPage(docResult.filename, page)}
                              className="page-chip"
                              title={`Abrir ${docResult.filename} en página ${page}`}
                            >
                              📄 Pág. {page}
                            </button>
                          ))}
                          {docResult.pages_found.length > 10 && (
                            <span className="more-pages">
                              +{docResult.pages_found.length - 10} más
                            </span>
                          )}
                        </div>
                      </div>
                      
                      {docResult.locations && docResult.locations.length > 0 && (
                        <div className="multi-doc-locations">
                          {docResult.locations.map((loc, locIdx) => (
                            <div key={locIdx} className="mini-location-card">
                              <div className="mini-location-header">
                                <span className="mini-page-badge">Pág. {loc.page}</span>
                                <button 
                                  onClick={() => openMultiPdfAtPage(docResult.filename, loc.page)}
                                  className="btn-mini-open"
                                >
                                  🔗
                                </button>
                              </div>
                              <p className="mini-preview">{loc.preview}</p>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                  
                  {/* Comparación estadística */}
                  {queryStats && queryStats.comparison && (
                    <div className="comparison-summary">
                      <h5>📊 Resumen Comparativo:</h5>
                      <div className="comparison-stats">
                        <div className="comparison-item">
                          <span className="comparison-label">Más relevante:</span>
                          <span className="comparison-value">{queryStats.comparison.most_relevant}</span>
                        </div>
                        <div className="comparison-item">
                          <span className="comparison-label">Con resultados:</span>
                          <span className="comparison-value">{queryStats.comparison.documents_with_results} documentos</span>
                        </div>
                        <div className="comparison-item">
                          <span className="comparison-label">Sin resultados:</span>
                          <span className="comparison-value">{queryStats.comparison.documents_without_results} documentos</span>
                        </div>
                        <div className="comparison-item">
                          <span className="comparison-label">Promedio:</span>
                          <span className="comparison-value">{queryStats.comparison.average_matches_per_doc} coincidencias/doc</span>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}
              
              {/* Ubicaciones en un solo PDF */}
              {!isMultiSearch && locations && locations.length > 0 && (
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
                  {queryStats.documents_found !== undefined && (
                    <p>📄 Documentos con resultados: {queryStats.documents_found}</p>
                  )}
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
