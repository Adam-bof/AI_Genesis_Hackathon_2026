# Technical Documentation — Autonomous Code Quality & Performance Agent

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  User Interface (React + Monaco Editor)                     │
│  │                                                       │
│  └───────────────────────┬──────────────────────────────┘
│                            │  POST /api/v1/analyze
│                            ▼
│               ┌─────────────────────────────────────┐
│               │  FastAPI Backend (Python 3.11+)       │
│               │  │  CORS middleware, routes            │
│               │  └───────────────┬─────────────────┘
│               │                  │  analyze(code, lang)
│               │                  ▼
│               │          ┌───────────────────────┐
│               │          │  CodeAnalyzer Core     │
│               │          │  │  • Python parser    │
│               │          │  │  • C parser (fallback)│
│               │          │  │  • JS parser        │
│               │          │  • Metrics calculator │
│               │          │  • 4 analysis tools   │
│               │          └─────────────┬───────────┘
│               │                  │  AI analysis (Claude/GPT-4)
│               │                  ▼
│               │      ┌───────────────────────┐
│               │      │  AI Agent Core        │
│               │      │  │  • ReAct planning   │
│               │      │  • Tool definitions │
│               │      │  • Decision making  │
│               │      └─────────────┬───────────┘
│               │                  │  Fix suggestions
│               │                  ▼
│               │          ┌───────────────────────┐
│               │          │  Tool Results         │
│               │          │  • code_analyzer      │
│               │          │  • performance_profiler│
│               │          │  • security_scanner   │
│               │          │  • fix_suggester      │
│               │          └─────────────┬───────────┘
│               │                  │  Report generation
│               │                  ▼
│               │          ┌───────────────────────┐
│               │          │  API Response         │
│               │          │  (JSON: metrics,       │
│               │          │   issues, fixes)      │
│               │          └─────────────┬───────────┘
│               │                  │
│               └──────────────┼─────────────────────
                          │  GET /health, GET /
                                   ▼
                         ┌───────────────────────┐
                         │  Static Files / Docs  │
                         └───────────────────────┘
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. FastAPI Backend (`app/main.py`)

- **Entry point** with CORS configuration
- **5 endpoints**: `GET /`, `GET /health`, `POST /api/v1/analyze`, `POST /api/v1/security-scan`, `POST /api/v1/fix-suggestions`
- **Multi-language support**: Python, C, JavaScript
- **CORS**: Allow all origins for development

### 2. Code Analyzer (`app/core/analyzer.py`)

Orchestrates the full analysis pipeline:

- **Language detection**: Python, C, JavaScript
- **AST parsing**: Built-in `ast` module for Python, pattern-based for C, subset for JS
- **Metrics calculation**: Cyclomatic complexity, maintainability index, LOC
- **Tool execution**: 4 analysis tools (code_analyzer, performance_profiler, security_scanner, fix_suggester)
- **AI integration**: Claude/GPT-4 via AgentCore for intelligent analysis

### 3. Analysis Tools (`app/tools.py`)

| Tool | Purpose |
|------|---------|
| `code_analyzer_tool` | Extracts metrics and quality indicators |
| `performance_profiler_tool` | Detects O(n²) loops, unnecessary allocations |
| `security_scanner_tool` | Finds hardcoded credentials, eval/exec usage |
| `fix_suggester_tool` | Provides before/after code examples |

### 4. AI Agent Core (`app/agent/Core.py`)

- **ReAct planning**: Reason-Act-Observe cycle
- **Tool registry**: Dynamic tool discovery and management
- **Memory**: Short-term context for conversation flow
- **Decision making**: When to use which tool based on analysis type

### 5. Language Parsers

| Language | Parser | Features |
|----------|--------|----------|
| **Python** | `ast` module | Functions, classes extraction; complexity, MI, LOC |
| **C** | pycparser (fallback) | Pattern-based function counting, basic metrics |
| **JavaScript** | `ast` subset | Functions, variables extraction; basic metrics |

### 6. API Routes (`app/api/routes.py`)

| Endpoint | Method | Parameters | Response |
|----------|--------|------------|----------|
| `/` | GET | None | `{"message": "..."}` |
| `/health` | GET | None | `{"status": "healthy", "service": "..."}` |
| `/api/v1/analyze` | POST | `file` (UploadFile) | Full analysis: metrics, issues, performance, security, fixes |
| `/api/v1/security-scan` | POST | `file` (UploadFile) | Vulnerabilities only |
| `/api/v1/fix-suggestions` | POST | `file` (UploadFile) | Fix suggestions with code examples |

### 7. Metrics Calculator (`app/metrics/metrics.py`)

- **Cyclomatic complexity**: radon (preferred) or manual AST-based fallback
- **Maintainability index**: radon (preferred) or manual calculation
- **Lines of code**: Manual counting (blank, code, comment lines)
- **Supported**: Python, C, JavaScript (with language-specific adaptations)

### 8. Frontend (React + Monaco Editor)

- **Component structure**: `src/App.jsx`, `src/components/`, `src/services/api.js`
- **Code display**: Monaco Editor for syntax-highlighted code editing
- **Results display**: Metrics cards, issue lists, fix suggestion panels
- **Export functionality**: Markdown and PDF export formats
- **Styling**: Tailwind CSS for responsive design

### 9. Deployment Configuration

#### Railway

```bash
# Railway.toml (root)
[build]
  command = "cd code_quality_agent/backend && pip install -r requirements.txt && cd ../frontend && npm install && npm run build"

[deploy]
  startCommand = "cd code_quality_agent/backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT"
  port = 8000
```

#### Render

```yaml
# render.yaml (root)
services:
  - type: web
    name: code-quality-agent
    env: python
    buildCommand: |
      cd code_quality_agent/backend && pip install -r requirements.txt
      cd ../frontend && npm install && npm run build
    startCommand: |
      cd code_quality_agent/backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

### 10. Project Phases (per Hackathon Plan)

| Phase | Dates | Hours | Deliverables |
|-------|-------|-------|--------------|
| 1. Clarification & Research | Jul 28 – Aug 10 | 15 | spec, research, wireframes |
| 2. Technical Design | Aug 11 – Aug 25 | 20 | API spec, agent prompt, architecture |
| 3. Initial Build | Aug 26 – Sep 15 | 40 | FastAPI + parser + basic agent |
| 4. Tool Development | Sep 16 – Oct 5 | 35 | 4 tools working with agent |
| 5. Frontend + Polish | Oct 6 – Oct 25 | 30 | React UI, Monaco, export, deploy |
| 6. Intensive Build | Oct 26 – Nov 2 | 56 | Final testing, fixes, demo, submission |

## 🛠️ Development Commands

```bash
# Start backend
cd code_quality_agent/backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Start frontend
cd code_quality_agent/frontend
npm run dev

# Run tests
cd code_quality_agent/backend
python -m pytest tests/ -v

# Install dependencies
cd code_quality_agent/backend
pip install -r requirements.txt
cd code_quality_agent/frontend
npm install

# Build frontend
cd code_quality_agent/frontend
npm run build
```

## 📦 Dependencies

### Backend (requirements.txt)

```
fastapi=="0.141.1"
uvicorn=="0.47.0"
python-dotenv=="1.0.1"
radon=="6.0.1"  # optional, with fallback
anthropic=="0.28.0"  # optional
openai=="1.35.0"  # optional
python-multipart  # for file uploads
```

### Frontend (package.json)

```
react: "^18.2.0"
react-dom: "^18.2.0"
react-scripts: "5.0.1"
react-monaco-editor: "^2.1.0"
recharts: "^2.10.4"
axios: "^1.7.2"
tailwindcss: "^3.4.1"
```

## 🎯 Success Criteria (per Hackathon Plan)

- [x] Application working perfectly
- [x] Advanced AI reasoning visible
- [x] Multi-language analysis (Python/C/JS)
- [x] Impressive demo with before/after code examples
- [x] Professional documentation
- [ ] API response < 3 seconds
- [ ] No memory leaks
- [ ] Video demo 3 min, 1080p+
- [ ] GitHub repo public
- [ ] Submission statement 200 words

## 📋 Next Steps

1. Final testing with edge cases
2. Video demo recording (3 minutes)
3. Submission statement (200 words)
4. Deployment verification (Railway/Render)
5. README and technical documentation completion
6. GitHub repository setup with organized commit history