# UI Manual Test Plan
## "The Lenny Growth Assistant"

> **Deliverable 7 Requirement**: Manual test plan providing step-by-step verification procedures for evaluators testing the application through the web user interface.

---

### Test Environment Setup
1. Start the stack: `docker-compose up --build` (or run `./run_app.bat` for local Python & Vite servers).
2. Open browser: Navigate to `http://localhost:3000`.
3. Verify backend health: Navigate to `http://localhost:8000/api/v1/health` (should return `"status": "healthy"`).

---

### Test Scenarios

#### Scenario 1: Model Provider Switching & Fallback
- **Step 1**: Look at the top-right header model selector dropdown.
- **Step 2**: Toggle provider from `Ollama (Local LLM)` to `Anthropic Claude` or `Lenny Mock Provider`.
- **Expected Result**: 
  - The model badge updates immediately in the UI.
  - If Ollama is selected but offline, an amber indicator appears and the system automatically falls back to Mock engine without throwing 500 errors.

#### Scenario 2: Grounded Q&A & Citation Verification
- **Step 1**: Click the quick prompt chip: *"Explain Brian Chesky's Founder Mode vs Manager Mode"*.
- **Step 2**: Observe the response generated.
- **Step 3**: Expand the citation accordion under the response message.
- **Expected Result**:
  - The response cites `[Brian Chesky, Ep. 101]`.
  - Citations display Episode Title, Guest Name, Timestamp (`04:15`), Key Quote, and a clickable link to Lenny's Podcast.

#### Scenario 3: Negative Test (Out-of-Scope Query)
- **Step 1**: Type an unsupported question, e.g., *"How do I bake sourdough bread?"*
- **Expected Result**:
  - The assistant acknowledges lack of transcript coverage: *"Based on the available transcripts, this specific topic is not covered in detail."*

#### Scenario 4: Ship 30 for 30 Content Skill
- **Step 1**: In the skill selector bar, click **"✍️ Ship 30 Essay"**.
- **Step 2**: Enter prompt: *"Write an essay on Shreyas Doshi's LNO framework"*.
- **Expected Result**:
  - Assistant produces a structured ~1,250-word essay.
  - Essay includes:
    1. Single-sentence counter-intuitive hook.
    2. 3 logical narrative pillars with punchy headings.
    3. Skimmable formatting with bullet points and bold emphasis.
    4. Explicit citations to Shreyas Doshi (Ep. 102).
    5. Actionable "Growth Playbook Checklist" at the end.

#### Scenario 5: Artifact Generation & Side-by-Side Viewer
- **Step 1**: In the skill selector bar, click **"🎨 Artifact"**.
- **Step 2**: Enter prompt: *"Create an interactive HTML growth framework matrix dashboard"*.
- **Expected Result**:
  - The layout dynamically shifts to a 50/50 split view.
  - The **Artifact Viewer** panel appears on the right with a green **"Sandboxed"** badge.
  - **Preview Tab**: Renders clean interactive HTML inside `<iframe sandbox="allow-scripts">` sanitized via DOMPurify.
  - **Code Tab**: Shows raw syntax-highlighted source code.
  - **Action Buttons**: "Copy" and "Download" buttons successfully export the file.

#### Scenario 6: Session Creation & Context Persistence
- **Step 1**: In the left sidebar, click **"+ New Chat"**.
- **Expected Result**: A clean conversation window opens with an empty state.
- **Step 2**: Send a message to start the chat.
- **Step 3**: Switch between past sessions in the sidebar.
- **Expected Result**: Full conversation history, citations, and attached artifacts restore accurately.
