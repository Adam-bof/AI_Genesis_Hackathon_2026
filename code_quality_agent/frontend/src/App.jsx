import React, { useState } from "react";
import { Editor } from "react-monaco-editor";
import { Chart } from "react-recharts";
import { Button, Card, CardHeader, CardTitle, CardContent, Spinner } from "./components/UI";

function App() {
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState("python");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [exportFormat, setExportFormat] useState("markdown");

  const languages = ["python", "javascript", "c"];

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("file", new Blob([code], { type: "text/plain" }), "code." + language);

      const response = await fetch("/api/v1/analyze", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error("Analysis error:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = () => {
    if (!results) return;
    const { analysis, performance, security } = results;

    if (exportFormat === "markdown") {
      const markdown = `# Code Analysis Report\n\n## Language: ${language}\n\n### Metrics\n- **Complexity**: ${JSON.stringify(analysis.metrics.complexity.map(c => c.complexity).join(", "))}\n- **Maintainability Index**: ${analysis.metrics.maintainability.mi}\n- **Lines of Code**: ${analysis.metrics.loc.code_lines}\n\n### Quality Issues\n${analysis.quality_issues.map((q, i) => `${i + 1}. ${q.type}: ${q.description}`).join("\n")}\n\n### Performance Issues\n${performance.performance_issues.map((p, i) => `${i + 1}. ${p.type}: ${p.description}`).join("\n")}\n\n### Security Issues\n${security.vulnerabilities.map((s, i) => `${i + 1}. ${s.type}: ${s.description}`).join("\n")}\n\n### Fix Suggestions\n${analysis.fix_suggestions.map((f, i) => `\n**Issue**: ${f.issue_type}\n**Explanation**: ${f.explanation}\n**Fixed Code**: \`\`\`\n${f.fixed_code}\n\`\`\`\n**Benefit**: ${f.benefit}`).join("\n")}`;

      const blob = new Blob([markdown], { type: "text/markdown" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "code-analysis-report.md";
      a.click();
      URL.revokeObjectURL(url);
    } else if (exportFormat === "pdf") {
      // PDF export would use jsPDF or similar
      alert("PDF export feature - coming soon!");
    }
  };

  return (
    <div style={{ padding: "2rem", maxWidth: "800px", margin: "0 auto" }}>
      <h1 style={{ textAlign: "center", color: "#2c3e50" }}>
        Autonomous Code Quality & Performance Agent
      </h1>

      <Card>
        <CardHeader>
          <CardTitle>Code Analysis</CardTitle>
        </CardHeader>
        <CardContent>
          <div style={{ marginBottom: "1rem" }}>
            <label style={{ marginRight: "0.5rem" }}>Language: </label>
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              style={{ padding: "0.25rem", borderRadius: "4px" }}
            >
              {languages.map((lang) => (
                <option key={lang} value={lang}>
                  {lang}
                </option>
              ))}
            </select>
          </div>

          <textarea
            rows={8}
            style={{
              width: "100%",
              padding: "0.5rem",
              borderRadius: "4px",
              border: "1px solid #ddd",
              marginBottom: "0.5rem",
              fontFamily: "monospace",
            }}
            value={code}
            onChange={(e) => setCode(e.target.value)}
            placeholder="Paste your code here..."
          ></textarea>

          <Button onClick={handleAnalyze} disabled={loading} style={{ marginBottom: "0.5rem" }}>
            {loading ? "Analyzing..." : "Analyze Code"}
          </Button>
        </CardContent>
      </Card>

      {results && (
        <Card>
          <CardHeader>
            <CardTitle>Analysis Results</CardTitle>
          </CardHeader>
          <CardContent>
            <h3>Metrics</h3>
            <p>
              <strong>Cyclomatic Complexity:</strong> {" "}
              {results.metrics.complexity.map((c) => (
                <span key={c.name}>{c.name}: {c.complexity}{", "}
              ))}</p>
            <p>
              <strong>Maintainability Index:</strong> {" "}
              {results.metrics.maintainability.mi} ({results.metrics.maintainability.grade})
            </p>
            <p>
              <strong>Lines of Code:</strong> {" "}
              {results.metrics.loc.code_lines} code /
              {results.metrics.loc.blank_lines} blank /
              {results.metrics.loc.comment_lines} comments
            </p>

            <h3>Quality Issues</h3>
            {results.quality_issues.length > 0 ? (
              <ul>
                {results.quality_issues.map((q, i) => (
                  <li key={i}>
                    <strong>{q.type}:</strong> {q.description}
                  </li>
                ))}
              </ul>
            ) : (
              <p>No quality issues detected ✓</p>
            )}

            <h3>Performance Issues</h3>
            {performance.performance_issues.length > 0 ? (
              <ul>
                {performance.performance_issues.map((p, i) => (
                  <li key={i}>
                    <strong>{p.type}:</strong> {p.description}
                  </li>
                ))}
              </ul>
            ) : (
              <p>No performance issues detected ✓</p>
            )}

            <h3>Security Issues</h3>
            {security.vulnerabilities.length > 0 ? (
              <ul>
                {security.vulnerabilities.map((s, i) => (
                  <li key={i}>
                    <strong>{s.type}:</strong> {s.description}
                  </li>
                ))}
              </ul>
            ) : (
              <p>No security vulnerabilities detected ✓</p>
            )}

            <h3>Fix Suggestions</h3>
            {analysis.fix_suggestions.length > 0 ? (
              analysis.fix_suggestions.map((f, i) => (
                <div key={i} style={{ marginBottom: "1rem", padding: "0.5rem", background: "#f8f9fa", borderRadius: "4px" }}>
                  <p><strong>Issue:</strong> {f.issue_type}</p>
                  <p><strong>Explanation:</strong> {f.explanation}</p>
                  <p><strong>Benefit:</strong> {f.benefit}</p>
                  <pre style={{ fontSize: "0.8rem", background: "#f1f1f1", padding: "0.5rem", borderRadius: "4px" }}>
                    <code>{f.fixed_code}</code>
                  </pre>
                </div>
              ))}
            ) : (
              <p>No fix suggestions available</p>
            )}
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Export Report</CardTitle>
        </CardHeader>
        <CardContent>
          <p>Export your analysis results:</p>
          <select
            value={exportFormat}
            onChange={(e) => setExportFormat(e.target.value)}
            style={{ marginBottom: "0.5rem", padding: "0.25rem" }}
          >
            <option value="markdown">Markdown (.md)</option>
            <option value="pdf">PDF (.pdf)</option>
          </select>
          <Button onClick={handleExport} disabled={!results}>
            Export Report
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}

export default App;