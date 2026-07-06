// Slider for the minimum rating. Controlled by the parent.
export default function RatingSlider({ value, onChange }) {
  return (
    <div className="form-block">
      <label className="form-label">
        Minimum rating: <strong>{value}</strong>
      </label>
      <input
        type="range"
        min="0"
        max="9"
        step="0.5"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
}
