import { useState } from "react";

const DEFAULTS = { gen: 50, sim: 25, rat: 15, pop: 10 };

const LABELS = {
  gen: "Genre match",
  sim: "Similarity to favorite",
  rat: "Rating",
  pop: "Popularity",
};

export default function WeightsPanel({ weights, onChange }) {
  const [open, setOpen] = useState(false);

  function updateOne(key, value) {
    onChange({ ...weights, [key]: Number(value) });
  }

  function reset() {
    onChange(DEFAULTS);
  }

  return (
    <div className="weights-panel">
      <button
        type="button"
        className="weights-toggle"
        onClick={() => setOpen(!open)}
      >
        {open ? "\u25bc" : "\u25b6"} Advanced: adjust scoring weights
      </button>

      {open && (
        <div className="weights-body">
          <p className="weights-hint">
            Drag to change how much each part contributes to the ranking.
          </p>

          {Object.keys(DEFAULTS).map((key) => (
            <div key={key} className="weight-row">
              <label className="weight-label">
                {LABELS[key]}
                <span className="weight-value">{weights[key]}</span>
              </label>
              <input
                type="range"
                min="0"
                max="100"
                value={weights[key]}
                onChange={(e) => updateOne(key, e.target.value)}
                className="weight-slider"
              />
            </div>
          ))}

          <div className="weights-split">
            Current split:{" "}
            {Object.keys(DEFAULTS).map((key, i) => (
              <span key={key}>
                {LABELS[key].split(" ")[0]} {weights[key]}
                {i < 3 ? " \u00b7 " : ""}
              </span>
            ))}
          </div>

          <button type="button" className="weights-reset" onClick={reset}>
            Reset to defaults
          </button>
        </div>
      )}
    </div>
  );
}