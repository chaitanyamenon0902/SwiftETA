import { useState } from "react";
import { submitFeedback } from "../services/api";

function FeedbackForm({ predictionId }) {
  const [actualEta, setActualEta] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async () => {
    if (!actualEta) return;
    try {
      const payload = {
        prediction_id: predictionId,
        actual_eta: parseFloat(actualEta),
      };

      await submitFeedback(payload);
      setSubmitted(true);
      setActualEta("");
    } catch (err) {
      console.error(err);
      alert("Feedback failed");
    }
  };

  if (submitted) {
    return (
      <div className="bg-green-900/20 border border-green-700 rounded-lg p-4">
        <p className="text-green-400 font-medium">Feedback submitted successfully.</p>
        <p className="text-green-300 text-sm mt-1">This data helps improve future predictions.</p>
      </div>
    );
  }

  return (
    <div className="bg-slate-950 border border-slate-800 rounded-xl p-5">
      <h3 className="text-lg font-bold text-white">Wrong Prediction?</h3>
      <p className="text-slate-400 text-sm mt-1">
        Help improve the engine using the actual delivery outcome.
      </p>

      <input
        type="number"
        placeholder="Actual delivery time (mins)"
        value={actualEta}
        onChange={(e) => setActualEta(e.target.value)}
        className="w-full mt-4 bg-slate-900 border border-slate-700 rounded-lg px-4 py-3 text-white outline-none focus:ring-2 focus:ring-green-500 transition"
      />

      <button
        onClick={handleSubmit}
        className="w-full mt-4 bg-green-600 hover:bg-green-700 text-white rounded-lg py-3 font-semibold transition"
      >
        Submit Feedback
      </button>
    </div>
  );
}

export default FeedbackForm;