# Product Requirements Document (PRD)
## "The Lenny Growth Assistant"

---

## 1. Executive Summary & Discovery Brief

### 1.1 Target User & Persona
- **Primary User**: Product Managers, Growth Engineers, Product Marketing Leads, and Founders.
- **User Job-to-be-Done (JTBD)**: "When I am designing growth loops, structuring product strategy, or writing leadership memos, I want to access grounded insights from elite operators (Brian Chesky, Shreyas Doshi, Elena Verna) so that I can make high-confidence decisions without manually searching hundreds of podcast transcript hours."
- **Core Pain Removed**: Eliminates unstructured prompt engineering, time spent scrubbing audio/transcript archives, hallucinated advice, and tedious manual formatting for stakeholder presentations.

### 1.2 Success Metrics
1. **Grounded Accuracy Rate**: >90% of citations resolve to valid episode timestamps with zero false attribution.
2. **Artifact Engagement & Adoption**: >40% of sessions generate and view a rendered HTML/CSS or Markdown artifact.
3. **Execution Latency**: Local Ollama RAG response delivery under 4 seconds; cloud fallback under 2 seconds.

### 1.3 Key Assumptions
- Evaluators require a zero-setup local fallback if Ollama or external API keys are unavailable.
- Transcript datasets are structured by episode, speaker turns, topics, and timestamps.
- Rendered HTML artifacts must be safely sandboxed inside an `<iframe>` to prevent XSS.

### 1.4 Scope Choices
- **Included**:
  - Grounded RAG conversational engine with explicit episode/timestamp citation footnoting.
  - Dedicated **Ship 30 for 30 Content Skill** generating ~1,250-word structured viral essays.
  - Interactive **Side-by-Side Artifact Viewer** with raw code vs. sandboxed visual rendering.
  - Flexible LLM provider switcher (Local Ollama, Anthropic Claude, OpenAI, Mock Engine).
  - PostgreSQL database with Async SQLAlchemy & local SQLite fallback.
- **Intentionally Excluded**:
  - User authentication/SSO (out of scope for local evaluation simplicity).
  - Live YouTube transcript web scraper (pre-indexed dataset used for speed and offline stability).

### 1.5 Risks & Trade-Off Analysis
| Risk | Severity | Mitigation Strategy |
| :--- | :--- | :--- |
| **Hallucination** | High | System prompts enforce strict context grounding. Unsupported queries explicitly output a fallback statement. |
| **Local Ollama Unavailable** | Medium | Graceful automatic fallback to the built-in Lenny Mock Provider without crashing. |
| **XSS in Rendered Artifacts** | High | Sanitization via `DOMPurify` combined with HTML `iframe` `sandbox="allow-scripts"`. |

---

## 2. Functional Acceptance Criteria

1. **Session Context Persistence**:
   - Creating a new chat initializes a clean context window.
   - Returning to a session restores full message history, citations, and artifacts.
2. **Grounded Citation Chips**:
   - Clicking a footnote displays the episode title, guest name, timestamp, and direct link.
3. **Ship 30 for 30 Skill**:
   - Outputs ~1,250 words formatted with hook, 3 pillars, skimmable bullet points, bold key insights, and actionable takeaway.
4. **Artifact Viewer**:
   - Automatically opens on HTML/CSS generation with toggleable Preview vs. Code tabs.
