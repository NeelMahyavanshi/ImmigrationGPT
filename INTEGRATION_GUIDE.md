# Frontend-Backend Integration Guide

## Overview

The Reflex frontend (in `/hello`) is now connected to the AI agent backend (in `/app`) through the bridge layer (in `/bridge`).

## Architecture

```
Frontend (Reflex) → Bridge Layer → Backend Agents (Agno)
     ↓                   ↓               ↓
  ChatState      router_bridge.py    chitchat_agent
                                     eligibility_agent
                                     document_agent
                                     sop_agent
```

## What Changed

### 1. Frontend State (`hello/hello/states/state.py`)
- Removed mock data functions
- Added imports for bridge functions
- Updated `_call_agent()` to use real backend agents via `asyncio.to_thread()`
- Modified `_handle_response()` to accept the new response format (reply, files, payload)
- User messages now get session IDs for conversation memory

### 2. Response Flow
**Before:** Mock data returned from hardcoded functions
**After:** Real AI agents process queries and return structured responses

## Environment Setup

### Required Environment Variables

Update your `.env` file with:

```env
# Database connection (Required for agent memory)
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
AGNO_MEMORY_TABLE=agno_memories

# API Keys (Required for agents to work)
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
```

### Database Setup

The agents use PostgreSQL for conversation memory. You'll need to:

1. Get your Supabase database password from the Supabase dashboard
2. Create the memory table (if not exists):

```sql
CREATE TABLE IF NOT EXISTS agno_memories (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    session_id TEXT,
    message TEXT,
    role TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## How It Works

### 1. User Input Flow
1. User types a message in the chat
2. `ChatState.send()` receives the input
3. Based on keywords, it routes to: `chat`, `eligibility`, `documents`, or `sop`
4. `_call_agent()` calls the bridge function with user text and session ID
5. Bridge calls the appropriate agent and returns (reply, files, payload)
6. Response is displayed with optional panels (eligibility cards, document lists, etc.)

### 2. Agent Routing
- **Eligibility keywords:** "eligible", "crs", "teer", "noc"
- **Documents keywords:** "form", "imm", "checklist", "documents"
- **SOP keywords:** "sop", "statement of purpose", "loe"
- **Default:** Routes to chitchat agent (which may escalate)

### 3. Escalation
If chitchat agent determines the query should go to a specialist:
- Returns `{"escalate_to": "eligibility_agent"}` in payload
- Frontend automatically calls the specialist agent
- User gets comprehensive answer without multiple interactions

## File Structure

```
project/
├── hello/                      # Reflex frontend
│   └── hello/
│       ├── states/
│       │   └── state.py       # ✅ UPDATED - Now calls real agents
│       └── components/
│           ├── chat.py        # Chat UI (unchanged)
│           ├── panels.py      # Result panels (unchanged)
│           └── ...
├── app/                       # Backend agents
│   └── agents/
│       ├── chitchat_agent.py  # Router/general chat
│       ├── eligibility_agent.py
│       ├── document_agent.py
│       └── sop_agent.py
├── bridge/                    # Integration layer
│   └── router_bridge.py      # Bridge functions
└── public/                    # Generated files (PDFs, etc.)
```

## Testing the Integration

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   - Update `.env` with real credentials
   - Ensure database is accessible

3. **Run the application:**
   ```bash
   cd hello
   reflex run
   ```

4. **Test queries:**
   - "Am I eligible for Express Entry with 3 years experience?"
   - "What documents do I need for a study permit?"
   - "Help me write an SOP"

## Troubleshooting

### Agent Not Responding
- Check API keys in `.env`
- Verify DATABASE_URL is correct
- Check logs for error messages

### Import Errors
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Check Python path in bridge imports

### Database Connection Failed
- Verify Supabase database password
- Check network connectivity to Supabase
- Ensure memory table exists

## Next Steps

Consider adding:
1. Loading indicators while agents process
2. Error handling UI for failed agent calls
3. Retry logic for network failures
4. Analytics/logging for agent performance
5. User feedback mechanism
