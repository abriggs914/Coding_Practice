import { useState, useEffect, useRef } from "react";

const SYSTEM_PROMPT = `You are a TELUS International Maps Quality Analyst exam question generator and evaluator. You generate realistic map search result evaluation scenarios and evaluate user answers against the correct logic from the guidelines.

You know the following rating scales:
- RELEVANCE: Navigational, Excellent, Good, Acceptable, Bad (with sub-reasons: Distance/Prominence Issue, User Intent Issue)
- NAME: Correct, Incorrect (sub-types: Incorrect Category, Incorrect Street Number, Incorrect Street Name, Incorrect Unit/Apt), N/A
- ADDRESS: Correct, Incorrect (sub-types: Street Number, Street Name, Unit/Apt, Does Not Exist), N/A
- PIN: Perfect, Approximate, Next Door, Wrong, Can't Verify

Key guideline rules you apply:
1. Section 2.3.2 Implicit Location: If user is INSIDE fresh viewport (FVP) → use user location. If user is OUTSIDE FVP → results expected in/near viewport. If viewport is STALE → use user location only.
2. Section 2.3.1 Explicit Location: "near me"/"nearby" → use user location, not viewport.
3. Chain business + general location modifier (e.g., "Walmart Tomball TX") → ignore user/viewport, results expected within location modifier.
4. Navigational = unique exact match (single result qualifies). Excellent = fits primary intent, no demotion needed. Good = -1 demotion. Acceptable = -2 demotion. Bad = does not meet intent.
5. Section 10.3 Non-existing address: if result = same as query address → Excellent (not Navigational). Name = N/A, Address = Incorrect (does not exist), Pin = Can't Verify.
6. Section 10.1 Specific address: if result is street only (no number) → Acceptable.
7. Section 10.7.8 Clear Categories: for category queries (e.g., "mall"), a result that is a business *inside* a mall (like Nordstrom Rack) = Bad User Intent.
8. Section 5.14 Unexpected Results / Locality queries: only internationally prominent POIs and transit POIs qualify for secondary intent. Everything else = Bad.
9. Section 5.16.1 Transit Queries: exact match station = Navigational. Other stations in same locality = Excellent. Stations just outside locality = Good or Acceptable based on distance.
10. Section 5.18 Service-Level Mismatch: query for Brand A, result is Brand B (similar service) = Bad.
11. Section 5.7/5.8 Few Possible Results: leniency on distance when few results exist.
12. Section 4.2.2 Closed business: still rate Relevance as if operational. Skip Name/Address/Pin if "closed" checkbox selected.
13. Section 6.1 Name N/A: all address-type results (full address, street, locality) = Name N/A.
14. Section 6.3.2 Incorrect Category: wrong category = Name Incorrect.
15. Section 9.4 Single Rooftop: pin on correct rooftop = Perfect. On same parcel/property = Approximate. Neighboring same-block property = Next Door. Wrong block or across street = Wrong.
16. Section 9.3.2 Shared Spaces: businesses in parking lot associated with main POI → whole parcel = Perfect.
17. Section 7.1.x Address accuracy: must match official website. Missing/wrong street number, name, direction, unit = Incorrect with specific sub-type.
18. Section 8.3.2.1 Minimum Address Component for transit: only correct locality required, not full street address.
19. Section 10.6.3 Chain Business with Location Modifier: results inside modifier = no distance demotion. Outside = demotion based on distance.
20. Section 5.1.8 Lack of Connection: query for "Walmart", result is "Walmart Pharmacy" = Bad.

When generating a question, output ONLY valid JSON in this exact format:
{
  "scenario": {
    "query": "the search query the user typed",
    "queryType": "Chain Business | Category Query | Specific Address | Non-Specific Address | Non-Existing Address | Locality Query | Transit Query | Chain + Location Modifier",
    "viewportStatus": "Fresh - User Inside | Fresh - User Outside | Stale | N/A (explicit location)",
    "resultName": "the name of the map result returned",
    "resultAddress": "the address shown for this result",
    "additionalContext": "any extra info needed: closed status, distance info, competing locations, website discrepancy, etc."
  },
  "correctAnswer": {
    "relevance": "e.g. Excellent",
    "relevanceReason": "e.g. Distance/Prominence Issue",
    "name": "e.g. Correct",
    "nameReason": "e.g. or empty string",
    "address": "e.g. Incorrect",
    "addressReason": "e.g. Street Number",
    "pin": "e.g. Perfect",
    "pinReason": "e.g. or empty string"
  },
  "explanation": {
    "relevance": "Full explanation of why this relevance rating is correct, citing the guideline section",
    "name": "Full explanation of name rating",
    "address": "Full explanation of address rating",
    "pin": "Full explanation of pin rating"
  }
}

Generate varied scenarios across all query types. Make them realistic and educational. Vary difficulty. Sometimes include tricky edge cases like closed businesses, non-existing addresses, category queries with wrong results, locality queries with transit secondary intent, etc.`;

const QUESTION_PROMPT = `Generate a new realistic TELUS Maps exam practice question. Vary the scenario type - don't repeat the same type consecutively. Output only the JSON object, no markdown, no explanation outside the JSON.`;

const EVAL_PROMPT = (scenario, correctAnswer, userAnswer) => `
A student answered the following TELUS Maps exam question. Evaluate their answer and provide detailed feedback.

SCENARIO:
Query: "${scenario.query}"
Query Type: ${scenario.queryType}
Viewport Status: ${scenario.viewportStatus}
Result Name: ${scenario.resultName}
Result Address: ${scenario.resultAddress}
Additional Context: ${scenario.additionalContext}

CORRECT ANSWER:
Relevance: ${correctAnswer.relevance}${correctAnswer.relevanceReason ? ' - ' + correctAnswer.relevanceReason : ''}
Name: ${correctAnswer.name}${correctAnswer.nameReason ? ' - ' + correctAnswer.nameReason : ''}
Address: ${correctAnswer.address}${correctAnswer.addressReason ? ' - ' + correctAnswer.addressReason : ''}
Pin: ${correctAnswer.pin}${correctAnswer.pinReason ? ' - ' + correctAnswer.pinReason : ''}

STUDENT ANSWER:
Relevance: ${userAnswer.relevance}${userAnswer.relevanceReason ? ' - ' + userAnswer.relevanceReason : ''}
Name: ${userAnswer.name}${userAnswer.nameReason ? ' - ' + userAnswer.nameReason : ''}
Address: ${userAnswer.address}${userAnswer.addressReason ? ' - ' + userAnswer.addressReason : ''}
Pin: ${userAnswer.pin}${userAnswer.pinReason ? ' - ' + userAnswer.pinReason : ''}

Score each field: correct (1 point) or incorrect (0 points). Output ONLY valid JSON:
{
  "scores": {
    "relevance": 1,
    "name": 1,
    "address": 0,
    "pin": 1
  },
  "feedback": {
    "relevance": "explanation of whether correct and why",
    "name": "explanation",
    "address": "explanation",
    "pin": "explanation"
  },
  "totalScore": 3,
  "overallFeedback": "brief encouraging summary"
}`;

const RELEVANCE_OPTIONS = ["Navigational", "Excellent", "Good", "Acceptable", "Bad"];
const RELEVANCE_REASONS = ["", "Distance/Prominence Issue", "User Intent Issue"];
const NAME_OPTIONS = ["Correct", "Incorrect", "N/A"];
const NAME_REASONS = ["", "Incorrect Category", "Incorrect Street Number", "Incorrect Street Name", "Incorrect Unit/Apt"];
const ADDRESS_OPTIONS = ["Correct", "Incorrect", "N/A"];
const ADDRESS_REASONS = ["", "Street Number", "Street Name", "Unit/Apt", "Does Not Exist"];
const PIN_OPTIONS = ["Perfect", "Approximate", "Next Door", "Wrong", "Can't Verify"];

async function callClaude(systemPrompt, userPrompt) {
  const response = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model: "claude-sonnet-4-20250514",
      max_tokens: 1000,
      system: systemPrompt,
      messages: [{ role: "user", content: userPrompt }],
    }),
  });
  const data = await response.json();
  return data.content?.[0]?.text || "";
}

function parseJSON(text) {
  try {
    const clean = text.replace(/```json|```/g, "").trim();
    return JSON.parse(clean);
  } catch {
    return null;
  }
}

function SelectField({ label, value, onChange, options, color }) {
  return (
    <div style={{ marginBottom: 8 }}>
      <label style={{ display: "block", fontSize: 11, fontWeight: 700, letterSpacing: "0.08em", textTransform: "uppercase", color: "#8b9bb4", marginBottom: 4 }}>{label}</label>
      <select
        value={value}
        onChange={e => onChange(e.target.value)}
        style={{
          width: "100%",
          padding: "8px 10px",
          borderRadius: 6,
          border: `1.5px solid ${color || "#2a3650"}`,
          background: "#111827",
          color: value ? "#e2e8f0" : "#4b5563",
          fontSize: 13,
          fontFamily: "inherit",
          outline: "none",
          cursor: "pointer",
        }}
      >
        {options.map(o => <option key={o} value={o}>{o || "— select —"}</option>)}
      </select>
    </div>
  );
}

function ScoreBadge({ score, total }) {
  const pct = total ? score / total : 0;
  const color = pct === 1 ? "#22c55e" : pct >= 0.5 ? "#f59e0b" : "#ef4444";
  return (
    <span style={{ display: "inline-block", padding: "2px 10px", borderRadius: 20, background: color + "22", color, fontWeight: 700, fontSize: 13, border: `1px solid ${color}44` }}>
      {score}/{total}
    </span>
  );
}

function FeedbackRow({ label, correct, feedback, userAnswer, correctAnswer }) {
  const ok = correct === 1;
  return (
    <div style={{ padding: "10px 14px", borderRadius: 8, background: ok ? "#14532d22" : "#7f1d1d22", border: `1px solid ${ok ? "#22c55e33" : "#ef444433"}`, marginBottom: 8 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 4 }}>
        <span style={{ fontSize: 15 }}>{ok ? "✓" : "✗"}</span>
        <span style={{ fontWeight: 700, fontSize: 12, textTransform: "uppercase", letterSpacing: "0.07em", color: ok ? "#22c55e" : "#ef4444" }}>{label}</span>
        {!ok && <span style={{ fontSize: 12, color: "#94a3b8" }}>Your: <b style={{ color: "#f87171" }}>{userAnswer}</b> → Correct: <b style={{ color: "#86efac" }}>{correctAnswer}</b></span>}
      </div>
      <p style={{ margin: 0, fontSize: 13, color: "#cbd5e1", lineHeight: 1.5 }}>{feedback}</p>
    </div>
  );
}

export default function App() {
  const [question, setQuestion] = useState(null);
  const [loading, setLoading] = useState(false);
  const [answer, setAnswer] = useState({ relevance: "", relevanceReason: "", name: "", nameReason: "", address: "", addressReason: "", pin: "", pinReason: "" });
  const [result, setResult] = useState(null);
  const [evaluating, setEvaluating] = useState(false);
  const [stats, setStats] = useState({ total: 0, points: 0, maxPoints: 0 });
  const [history, setHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);

  async function loadQuestion() {
    setLoading(true);
    setQuestion(null);
    setResult(null);
    setAnswer({ relevance: "", relevanceReason: "", name: "", nameReason: "", address: "", addressReason: "", pin: "", pinReason: "" });
    const raw = await callClaude(SYSTEM_PROMPT, QUESTION_PROMPT);
    const parsed = parseJSON(raw);
    setQuestion(parsed);
    setLoading(false);
  }

  async function submitAnswer() {
    if (!answer.relevance || !answer.name || !answer.address || !answer.pin) {
      alert("Please fill in all four rating fields before submitting.");
      return;
    }
    setEvaluating(true);
    const raw = await callClaude(SYSTEM_PROMPT, EVAL_PROMPT(question.scenario, question.correctAnswer, answer));
    const parsed = parseJSON(raw);
    setResult(parsed);
    if (parsed) {
      setStats(s => ({ total: s.total + 1, points: s.points + parsed.totalScore, maxPoints: s.maxPoints + 4 }));
      setHistory(h => [{ question, answer, result: parsed }, ...h.slice(0, 9)]);
    }
    setEvaluating(false);
  }

  useEffect(() => { loadQuestion(); }, []);

  const queryTypeColors = {
    "Chain Business": "#6366f1",
    "Category Query": "#ec4899",
    "Specific Address": "#06b6d4",
    "Non-Specific Address": "#14b8a6",
    "Non-Existing Address": "#8b5cf6",
    "Locality Query": "#f59e0b",
    "Transit Query": "#22c55e",
    "Chain + Location Modifier": "#f97316",
  };

  return (
    <div style={{ minHeight: "100vh", background: "#0a0f1e", color: "#e2e8f0", fontFamily: "'DM Mono', 'Fira Code', 'Courier New', monospace", padding: "0 0 60px" }}>
      {/* Header */}
      <div style={{ background: "linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%)", borderBottom: "1px solid #1e293b", padding: "20px 24px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <div style={{ width: 8, height: 8, borderRadius: "50%", background: "#6366f1", boxShadow: "0 0 8px #6366f1" }} />
            <span style={{ fontSize: 11, fontWeight: 700, letterSpacing: "0.15em", textTransform: "uppercase", color: "#6366f1" }}>TELUS Maps Analyst</span>
          </div>
          <h1 style={{ margin: "4px 0 0", fontSize: 20, fontWeight: 700, color: "#f1f5f9", letterSpacing: "-0.02em" }}>Exam Practice Tool</h1>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          {stats.total > 0 && (
            <div style={{ textAlign: "right" }}>
              <div style={{ fontSize: 11, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.08em" }}>Session Score</div>
              <div style={{ fontSize: 18, fontWeight: 700, color: stats.points / stats.maxPoints >= 0.8 ? "#22c55e" : stats.points / stats.maxPoints >= 0.6 ? "#f59e0b" : "#ef4444" }}>
                {stats.points}/{stats.maxPoints} <span style={{ fontSize: 12, color: "#64748b" }}>({stats.total} q)</span>
              </div>
            </div>
          )}
          <button onClick={() => setShowHistory(!showHistory)} style={{ padding: "6px 12px", borderRadius: 6, border: "1px solid #2a3650", background: "transparent", color: "#94a3b8", fontSize: 12, cursor: "pointer" }}>
            {showHistory ? "Hide" : "History"} ▾
          </button>
        </div>
      </div>

      <div style={{ maxWidth: 780, margin: "0 auto", padding: "24px 16px" }}>
        {/* History panel */}
        {showHistory && history.length > 0 && (
          <div style={{ marginBottom: 20, padding: 16, borderRadius: 10, background: "#111827", border: "1px solid #1e293b" }}>
            <div style={{ fontSize: 11, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.1em", color: "#64748b", marginBottom: 12 }}>Recent Questions</div>
            {history.map((h, i) => (
              <div key={i} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "6px 0", borderBottom: i < history.length - 1 ? "1px solid #1e293b" : "none" }}>
                <span style={{ fontSize: 13, color: "#94a3b8", flex: 1, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>"{h.question.scenario.query}"</span>
                <ScoreBadge score={h.result.totalScore} total={4} />
              </div>
            ))}
          </div>
        )}

        {/* Question card */}
        {loading && (
          <div style={{ textAlign: "center", padding: 60 }}>
            <div style={{ display: "inline-block", width: 36, height: 36, border: "3px solid #1e293b", borderTop: "3px solid #6366f1", borderRadius: "50%", animation: "spin 0.8s linear infinite" }} />
            <p style={{ color: "#64748b", marginTop: 12, fontSize: 13 }}>Generating scenario...</p>
            <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
          </div>
        )}

        {question && !loading && (
          <>
            {/* Scenario */}
            <div style={{ borderRadius: 12, background: "#111827", border: "1px solid #1e293b", marginBottom: 16, overflow: "hidden" }}>
              <div style={{ padding: "14px 18px", background: "#0f172a", borderBottom: "1px solid #1e293b", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                <span style={{ fontSize: 11, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.12em", color: "#64748b" }}>Scenario</span>
                <span style={{
                  fontSize: 11, fontWeight: 700, padding: "3px 10px", borderRadius: 20,
                  background: (queryTypeColors[question.scenario.queryType] || "#6366f1") + "22",
                  color: queryTypeColors[question.scenario.queryType] || "#6366f1",
                  border: `1px solid ${(queryTypeColors[question.scenario.queryType] || "#6366f1")}44`
                }}>
                  {question.scenario.queryType}
                </span>
              </div>
              <div style={{ padding: 18 }}>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginBottom: 12 }}>
                  <div style={{ padding: "10px 14px", borderRadius: 8, background: "#0f172a", border: "1px solid #1e293b" }}>
                    <div style={{ fontSize: 10, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.1em", color: "#475569", marginBottom: 4 }}>Query</div>
                    <div style={{ fontSize: 15, color: "#f1f5f9", fontWeight: 600 }}>"{question.scenario.query}"</div>
                  </div>
                  <div style={{ padding: "10px 14px", borderRadius: 8, background: "#0f172a", border: "1px solid #1e293b" }}>
                    <div style={{ fontSize: 10, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.1em", color: "#475569", marginBottom: 4 }}>Viewport Status</div>
                    <div style={{ fontSize: 13, color: "#94a3b8" }}>{question.scenario.viewportStatus}</div>
                  </div>
                </div>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginBottom: 12 }}>
                  <div style={{ padding: "10px 14px", borderRadius: 8, background: "#0f172a", border: "1px solid #1e293b" }}>
                    <div style={{ fontSize: 10, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.1em", color: "#475569", marginBottom: 4 }}>Result Name</div>
                    <div style={{ fontSize: 13, color: "#e2e8f0" }}>{question.scenario.resultName}</div>
                  </div>
                  <div style={{ padding: "10px 14px", borderRadius: 8, background: "#0f172a", border: "1px solid #1e293b" }}>
                    <div style={{ fontSize: 10, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.1em", color: "#475569", marginBottom: 4 }}>Result Address</div>
                    <div style={{ fontSize: 13, color: "#e2e8f0" }}>{question.scenario.resultAddress}</div>
                  </div>
                </div>
                <div style={{ padding: "10px 14px", borderRadius: 8, background: "#1a2535", border: "1px solid #2a3650" }}>
                  <div style={{ fontSize: 10, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.1em", color: "#475569", marginBottom: 4 }}>Additional Context</div>
                  <div style={{ fontSize: 13, color: "#94a3b8", lineHeight: 1.6 }}>{question.scenario.additionalContext}</div>
                </div>
              </div>
            </div>

            {/* Answer form */}
            {!result && (
              <div style={{ borderRadius: 12, background: "#111827", border: "1px solid #1e293b", marginBottom: 16, overflow: "hidden" }}>
                <div style={{ padding: "14px 18px", background: "#0f172a", borderBottom: "1px solid #1e293b" }}>
                  <span style={{ fontSize: 11, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.12em", color: "#64748b" }}>Your Rating</span>
                </div>
                <div style={{ padding: 18, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
                  <div style={{ padding: 14, borderRadius: 8, background: "#0f172a", border: "1px solid #312e81" }}>
                    <div style={{ fontSize: 11, fontWeight: 700, color: "#818cf8", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: 10 }}>Relevance</div>
                    <SelectField label="Rating" value={answer.relevance} onChange={v => setAnswer(a => ({ ...a, relevance: v }))} options={["", ...RELEVANCE_OPTIONS]} color="#312e81" />
                    <SelectField label="Reason (if applicable)" value={answer.relevanceReason} onChange={v => setAnswer(a => ({ ...a, relevanceReason: v }))} options={RELEVANCE_REASONS} color="#312e81" />
                  </div>
                  <div style={{ padding: 14, borderRadius: 8, background: "#0f172a", border: "1px solid #1e3a5f" }}>
                    <div style={{ fontSize: 11, fontWeight: 700, color: "#38bdf8", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: 10 }}>Name Accuracy</div>
                    <SelectField label="Rating" value={answer.name} onChange={v => setAnswer(a => ({ ...a, name: v }))} options={["", ...NAME_OPTIONS]} color="#1e3a5f" />
                    <SelectField label="Sub-type (if Incorrect)" value={answer.nameReason} onChange={v => setAnswer(a => ({ ...a, nameReason: v }))} options={NAME_REASONS} color="#1e3a5f" />
                  </div>
                  <div style={{ padding: 14, borderRadius: 8, background: "#0f172a", border: "1px solid #14532d" }}>
                    <div style={{ fontSize: 11, fontWeight: 700, color: "#4ade80", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: 10 }}>Address Accuracy</div>
                    <SelectField label="Rating" value={answer.address} onChange={v => setAnswer(a => ({ ...a, address: v }))} options={["", ...ADDRESS_OPTIONS]} color="#14532d" />
                    <SelectField label="Sub-type (if Incorrect)" value={answer.addressReason} onChange={v => setAnswer(a => ({ ...a, addressReason: v }))} options={ADDRESS_REASONS} color="#14532d" />
                  </div>
                  <div style={{ padding: 14, borderRadius: 8, background: "#0f172a", border: "1px solid #78350f" }}>
                    <div style={{ fontSize: 11, fontWeight: 700, color: "#fbbf24", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: 10 }}>Pin Accuracy</div>
                    <SelectField label="Rating" value={answer.pin} onChange={v => setAnswer(a => ({ ...a, pin: v }))} options={["", ...PIN_OPTIONS]} color="#78350f" />
                  </div>
                </div>
                <div style={{ padding: "0 18px 18px" }}>
                  <button
                    onClick={submitAnswer}
                    disabled={evaluating}
                    style={{
                      width: "100%", padding: "13px", borderRadius: 8,
                      background: evaluating ? "#1e293b" : "linear-gradient(135deg, #4f46e5, #7c3aed)",
                      color: evaluating ? "#64748b" : "white",
                      border: "none", fontFamily: "inherit", fontSize: 14, fontWeight: 700,
                      letterSpacing: "0.05em", cursor: evaluating ? "not-allowed" : "pointer",
                      transition: "opacity 0.2s"
                    }}>
                    {evaluating ? "Evaluating..." : "Submit Answer →"}
                  </button>
                </div>
              </div>
            )}

            {/* Results */}
            {result && (
              <div style={{ borderRadius: 12, background: "#111827", border: "1px solid #1e293b", marginBottom: 16, overflow: "hidden" }}>
                <div style={{ padding: "14px 18px", background: "#0f172a", borderBottom: "1px solid #1e293b", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                  <span style={{ fontSize: 11, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.12em", color: "#64748b" }}>Results</span>
                  <ScoreBadge score={result.totalScore} total={4} />
                </div>
                <div style={{ padding: 18 }}>
                  <FeedbackRow
                    label="Relevance"
                    correct={result.scores.relevance}
                    feedback={result.feedback.relevance}
                    userAnswer={`${answer.relevance}${answer.relevanceReason ? ' - ' + answer.relevanceReason : ''}`}
                    correctAnswer={`${question.correctAnswer.relevance}${question.correctAnswer.relevanceReason ? ' - ' + question.correctAnswer.relevanceReason : ''}`}
                  />
                  <FeedbackRow
                    label="Name Accuracy"
                    correct={result.scores.name}
                    feedback={result.feedback.name}
                    userAnswer={`${answer.name}${answer.nameReason ? ' - ' + answer.nameReason : ''}`}
                    correctAnswer={`${question.correctAnswer.name}${question.correctAnswer.nameReason ? ' - ' + question.correctAnswer.nameReason : ''}`}
                  />
                  <FeedbackRow
                    label="Address Accuracy"
                    correct={result.scores.address}
                    feedback={result.feedback.address}
                    userAnswer={`${answer.address}${answer.addressReason ? ' - ' + answer.addressReason : ''}`}
                    correctAnswer={`${question.correctAnswer.address}${question.correctAnswer.addressReason ? ' - ' + question.correctAnswer.addressReason : ''}`}
                  />
                  <FeedbackRow
                    label="Pin Accuracy"
                    correct={result.scores.pin}
                    feedback={result.feedback.pin}
                    userAnswer={answer.pin}
                    correctAnswer={question.correctAnswer.pin}
                  />
                  <div style={{ marginTop: 14, padding: "12px 14px", borderRadius: 8, background: "#0f172a", border: "1px solid #1e293b" }}>
                    <p style={{ margin: 0, fontSize: 13, color: "#94a3b8", lineHeight: 1.6 }}>{result.overallFeedback}</p>
                  </div>
                  <button
                    onClick={loadQuestion}
                    style={{
                      marginTop: 14, width: "100%", padding: "13px", borderRadius: 8,
                      background: "linear-gradient(135deg, #0f766e, #0891b2)",
                      color: "white", border: "none", fontFamily: "inherit",
                      fontSize: 14, fontWeight: 700, letterSpacing: "0.05em", cursor: "pointer"
                    }}>
                    Next Question →
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
