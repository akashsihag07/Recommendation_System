import { useState } from "react";

import GenrePicker from "./GenrePicker.jsx";
import LanguageSelect from "./LanguageSelect.jsx";
import RatingSlider from "./RatingSlider.jsx";
import YearRange from "./YearRange.jsx";
import FavoriteSearch from "./FavoriteSearch.jsx";

import WeightsPanel from "./WeightsPanel.jsx"; // for manual scoring

// Holds all the form state and bundles it into a preferences object on submit.
export default function PreferenceForm({ genres, languages, onSubmit, loading }) {
  const [picked, setPicked] = useState([]);
  const [language, setLanguage] = useState("any");
  const [minRating, setMinRating] = useState(6);
  const [yearFrom, setYearFrom] = useState("");
  const [yearTo, setYearTo] = useState("");
  const [favorite, setFavorite] = useState("");
  const [weights, setWeights] = useState({ gen: 50, sim: 25, rat: 15, pop: 10 });//for manuals scoring.

  function toggleGenre(g) {
    setPicked((prev) =>
      prev.includes(g) ? prev.filter((x) => x !== g) : [...prev, g]
    );
  }
//function update for mnaual scor
 function handleSubmit() {
    const defaults = { gen: 50, sim: 25, rat: 15, pop: 10 };
    const customised = Object.keys(defaults).some((k) => weights[k] !== defaults[k]);

    const payload = {
      genres: picked,
      lang: language,
      min_rating: Number(minRating),
      year_from: yearFrom ? Number(yearFrom) : null,
      year_to: yearTo ? Number(yearTo) : null,
      fav_movie: favorite.trim() || null,
      limit: 12,
    };

    if (customised) {
      payload.weights = {
        gen: weights.gen / 100,
        sim: weights.sim / 100,
        rat: weights.rat / 100,
        pop: weights.pop / 100,
      };
    }

    onSubmit(payload);
  }

  return (
    <section className="form">
      <GenrePicker genres={genres} selected={picked} onToggle={toggleGenre} />

      <div className="form-row">
        <LanguageSelect languages={languages} value={language} onChange={setLanguage} />
        <RatingSlider value={minRating} onChange={setMinRating} />
      </div>


      <div className="form-row">
        <YearRange
          from={yearFrom}
          to={yearTo}
          onFromChange={setYearFrom}
          onToChange={setYearTo}
        />
      </div>

      <FavoriteSearch value={favorite} onChange={setFavorite} />

       <WeightsPanel weights={weights} onChange={setWeights} /> 

      <button className="submit-btn" onClick={handleSubmit} disabled={loading}>
        {loading ? "Searching\u2026" : "Find my movies"}
      </button>
    </section>
  );
}