export default function YearRange({ from, to, onFromChange, onToChange }) {
  return (
    <div className="form-block">
      <label className="form-label">Released between</label>
      <div className="year-inputs">
        <input
          type="number"
          placeholder="1990"
          value={from}
          onChange={(e) => onFromChange(e.target.value)}
        />
        <span>and</span>
        <input
          type="number"
          placeholder="2016"
          value={to}
          onChange={(e) => onToChange(e.target.value)}
        />
      </div>
    </div>
  );
}
