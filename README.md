# SignBridge

---

## 1. Project Folder Structure

```plaintext
signbridge/
│
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── api/              # API route definitions
│   │   ├── core/             # Core settings, config, security
│   │   ├── db/               # Supabase integration, models, queries
│   │   ├── ml/               # ML model wrappers (MediaPipe, Whisper, etc.)
│   │   ├── services/         # Business logic, orchestration
│   │   ├── utils/            # Helper functions
│   │   └── main.py           # FastAPI entrypoint
│   ├── tests/                # Backend tests
│   ├── requirements.txt      # Python dependencies
│   └── Dockerfile            # Backend Dockerfile
│
├── frontend/                 # React frontend
│   ├── public/
│   ├── src/
│   │   ├── assets/           # Images, videos, etc.
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/            # Page-level components
│   │   ├── services/         # API calls, Supabase client
│   │   ├── hooks/            # Custom React hooks
│   │   ├── utils/            # Frontend helpers
│   │   ├── avatar/           # 3D avatar rendering (e.g., Three.js)
│   │   └── App.tsx
│   ├── package.json
│   └── Dockerfile            # Frontend Dockerfile (optional)
│
├── ml-models/                # ML models, scripts, weights
│   ├── mediapipe/
│   ├── whisper/
│   ├── elevenlabs/
│   └── README.md
│
├── .github/                  # GitHub Actions workflows
│   └── workflows/
│       ├── backend.yml       # Backend CI/CD
│       ├── frontend.yml      # Frontend CI/CD
│       └── deploy.yml        # Deployment pipeline
│
├── docs/                     # Documentation
│   └── architecture.md
│
├── README.md
└── docker-compose.yml        # For local dev orchestration
```

---

## 2. Model Integration Patterns

- **MediaPipe (Sign Detection):**
  - Run in a Python process (backend or separate service).
  - Expose a WebSocket or REST endpoint for real-time video frame inference.
  - Use WebRTC or WebSockets for low-latency streaming from frontend to backend.

- **Whisper (Speech-to-Text):**
  - Run as a backend service (Python).
  - Accept audio blobs from frontend, return transcribed text.

- **ElevenLabs (Text-to-Speech):**
  - Use their API from backend (Python) or directly from frontend if CORS allows.
  - Cache audio files in Supabase storage for chat history.

- **3D Avatar (Sign Rendering):**
  - Use Three.js or Babylon.js in React frontend.
  - Backend sends sign language sequence (e.g., JSON of gestures), frontend animates avatar accordingly.

---

## 3. CI/CD Guidance

- **GitHub Actions:**
  - Separate workflows for backend and frontend (test, lint, build).
  - Deploy backend to Render or similar (Docker-based).
  - Deploy frontend to Vercel (React optimized).
  - Use environment secrets for API keys, DB URLs, etc.

- **Example Workflow Triggers:**
  - On push to `main` or PRs.
  - On tag for production deploy.

---

## 4. Database (Supabase)

- Use Supabase for:
  - User authentication (email, OAuth, etc.)
  - Storing chat history (text, sign sequence, audio URLs)
  - File storage (audio, video snippets if needed)
- Access Supabase from both backend (for secure ops) and frontend (for real-time features).

---

## 5. Local Development

- Use `docker-compose.yml` to spin up backend, frontend, and any local dependencies.
- Use `.env` files for local secrets/config.

---


