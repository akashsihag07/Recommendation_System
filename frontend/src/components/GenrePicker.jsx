// Genre selector.
// Displays the available genres and notifies the parent when one is toggled.
export default function GenrePicker({ genres, selected, onToggle }) {
  return (
    <div className="form-block">
      <label className="form-label">Pick your genres</label>
      <div className="chips">
        {genres.map((g) => (
          <button
            key={g}
            type="button"
            className={selected.includes(g) ? "chip chip-on" : "chip"}
            onClick={() => onToggle(g)}
          >
            {g}
          </button>
        ))}
      </div>
    </div>
  );
}
