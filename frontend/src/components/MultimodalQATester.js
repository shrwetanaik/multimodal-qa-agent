import React, { useState } from "react";
import axios from "axios";

const MultimodalQATester = () => {
  const [screenshot, setScreenshot] = useState(null);
  const [prompt, setPrompt] = useState("");
  const [dom, setDom] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!screenshot || !prompt) return;

    const formData = new FormData();
    formData.append("screenshot", screenshot);
    formData.append("prompt", prompt);
    if (dom) formData.append("dom_html", dom);

    setLoading(true);
    try {
      const res = await axios.post("http://localhost:8000/test", formData);
      setResponse(res.data);
    } catch (err) {
      alert("Test failed: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h2>🧪 Multimodal QA Test Runner</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: "1rem" }}>
          <label>📷 Screenshot:</label><br />
          <input
            type="file"
            accept="image/png, image/jpeg"
            onChange={(e) => setScreenshot(e.target.files[0])}
            required
          />
        </div>
        <div style={{ marginBottom: "1rem" }}>
          <label>🧠 Prompt:</label><br />
          <textarea
            rows={3}
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="e.g. Test login with invalid email"
            style={{ width: "100%" }}
            required
          />
        </div>
        <div style={{ marginBottom: "1rem" }}>
          <label>🌐 DOM HTML (optional):</label><br />
          <textarea
            rows={5}
            value={dom}
            onChange={(e) => setDom(e.target.value)}
            placeholder="Paste HTML DOM here"
            style={{ width: "100%" }}
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? "Running..." : "Run Test"}
        </button>
      </form>

      {response && (
        <div style={{ marginTop: "2rem" }}>
          <h3>📋 Test Steps</h3>
          <pre style={{ background: "#f0f0f0", padding: "1rem" }}>
            {response.steps.join("\n")}
          </pre>
          <h4>Status: ✅ {response.status}</h4>
        </div>
      )}
    </div>
  );
};

export default MultimodalQATester;
