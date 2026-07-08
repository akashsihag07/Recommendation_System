# WatchHub
*Find your next movie without the endless scrolling.*

A movie recommendation web app built around one idea: the ranking logic should be visible to the user, and it should be adjustable.

![WatchHub interface](docs/screenshots/img01_form.png)

For the full technical documentation, see [`docs/documentation.pdf`](docs/documentation.pdf).

---

## Table of Contents
* [Setup](#setup)
* [How to use it](#how-to-use-it)
* [Why I chose this project](#why-i-chose-this-project)
* [What is special about it](#what-is-special-about-it)
* [Data preparation](#data-preparation)
* [Tools used](#tools-used)
* [Sources and declarations](#sources-and-declarations)
* [AI usage declaration](#ai-usage-declaration)
* [Technical overview](#technical-overview)

---

## Setup

### Prerequisites
* The only tool required is **Docker Desktop**.
* Everything else (Python, Node.js, MongoDB, dependencies) runs inside containers.
* Nothing else needs to be installed on the host machine.

Install Docker Desktop from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop), launch it, wait for the whale icon in the menu bar, and confirm with:

```bash
docker --version
```

### Getting the code

**Option A: using Git**
```bash
git clone https://github.com/akashsihag07/Recommendation_System 20_Akash.S_TechnicalProject
cd 20_Akash.S_TechnicalProject
```

**Option B: downloading the ZIP**
1. Open [https://github.com/akashsihag07/Recommendation_System](https://github.com/akashsihag07/Recommendation_System)
2. Click the green **Code** button, then **Download ZIP**.
3. Extract, rename the folder to `20_Akash.S_TechnicalProject`, and open a terminal in it.

### Running the app
```bash
docker compose up --build
```
* First run takes 2 to 3 minutes (Docker downloads base images and seeds the database).
* Subsequent runs start in seconds.

Then open:
* Frontend: http://localhost:3000
* Backend API docs: http://localhost:8000/docs

### Stopping
```bash
docker compose down
```

---

## How to use it
* **Pick genres** by clicking one or more chips. Multiple selections are allowed.
* **Set language** from the dropdown to limit results to one language (e.g. Hindi), or leave as "Any language".
* **Set minimum rating** using the slider (0 to 10).
* Optionally, **enter a favorite movie title** in the "Loved a movie?" field to get recommendations similar to it.
* Open the **Advanced panel** to adjust the four scoring weights (Genre, Similarity, Rating, Popularity). Defaults are 50 / 25 / 15 / 10.
* Click **Find my movies** to see the ranked results.
* Each card shows the poster, title, year, runtime, rating with vote count, an expandable overview, genres, and a "Watch Trailer" link.

---

## Why I chose this project
* **The data is clean and publicly available.** TMDB provides all the fields a recommender needs (genres, ratings, overviews, keywords) without scraping. Build time went into the recommender logic itself, not into data acquisition.
* **I know the domain well.** I could audit my own outputs at every step. When the system returned a wrong result, I could recognize it as wrong without external verification.
* **The scope is well defined.** A movie recommender has a clear notion of what "working" looks like. That clarity was set from day one and let me focus on execution quality.
* **Existing apps have real gaps I wanted to address.** Weak multilingual coverage, opaque ranking systems, and no user control over how recommendations are weighted. These became direct build targets.

---

## What is special about it
* **Blended similarity using two techniques.** The "more like this movie" feature combines Jaccard similarity on structured tags with cosine similarity of sentence embeddings on plot overviews.
    * Jaccard alone is grounded but blind to thematic meaning that is not in the tags.
    * Embeddings alone capture meaning but can drift into unrelated genres.
    * Combined (70% embeddings, 30% Jaccard), the result is both grounded and thematically rich.
* **User-adjustable ranking weights.** Four sliders in an Advanced panel let users change how much each factor contributes to the ranking.
* **Multilingual catalogue with a language filter.** Dozens of languages, not Hollywood-only.
* **Real posters and trailer links** on every card, loaded live from TMDB.
* **Plug-and-play deployment.** One Docker command starts everything. No API keys, no configuration.

### Concrete impact of the blend
Searching for "Batman v Superman: Dawn of Justice" as a favorite movie:
* **With Jaccard only:** three Lord of the Rings films appeared near the top (broad genre overlap on Action, Adventure, Fantasy, but no thematic connection).
* **With Jaccard + embeddings:** Lord of the Rings drops out completely. Top results become thematically appropriate: The Dark Knight, Justice League: Warworld, Spider-Man: Across the Spider-Verse, and other DC/superhero-conflict films.

See `docs/documentation.pdf` (Section 6) for the before/after screenshots.

---

## Data preparation
* **Source:** *TMDB Movies Dataset* by asaniczka on Kaggle, ~1.45 million rows.
* **Pivot from two datasets to one.** Started with TMDB 5000 + IMDb India, hit real problems (mismatched popularity scales, clashing genre vocabularies, missing overviews on one source), and switched to a single unified dataset that solved them at the source.
* **Filtering to a quality subset** (done offline in Kaggle):
    * `vote_count >= 25`
    * Non-empty `genres` and `overview`
    * `adult == False`
    * Result: ~43,000 movies.
* **Cleaning the rows** (in `cleaning.py`):
    * Split comma-separated genres and keywords into lists.
    * Extract year from `release_date`.
    * Safe cast numeric fields.
    * Drop rows still missing essentials.
* **Precomputing embeddings offline.** Sentence embeddings for ~43,000 overviews are generated once in a Kaggle notebook (GPU-accelerated), saved as a compressed `.npz` file (~30 MB, float16), and loaded into memory at backend startup. The embedding model is never present in the runtime container.

---

## Tools used
**Frontend**
* React (plain JavaScript, no TypeScript)
* Vite (build tool)
* nginx (serves the built static files)

**Backend**
* Python 3.11
* FastAPI (web framework)
* Pydantic (schema validation)
* Uvicorn (ASGI server)

**Database**
* MongoDB
* PyMongo (Python driver)

**ML (used offline in Kaggle)**
* sentence-transformers
* all-MiniLM-L6-v2 pre-trained model
* NumPy (runtime vector math)

**Orchestration**
* Docker
* Docker Compose

---

## Sources and declarations
* **Movie data:** [TMDB Movies Dataset](https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies) by asaniczka on Kaggle, originally from [The Movie Database](https://www.themoviedb.org/). Attribution required by TMDB's terms of use.
* **Movie posters:** loaded live from `image.tmdb.org` at display time. Only the short poster path is stored locally.
* **Sentence embedding model:** [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) from the sentence-transformers library. Used offline; not a runtime dependency.
* **Frameworks and libraries** (all open source, standard permissive licenses): React, Vite, FastAPI, Pydantic, Uvicorn, MongoDB, PyMongo, NumPy, Docker, Docker Compose.

---

## AI usage declaration
As permitted by the project brief, AI assistants (Claude and Gemini) were used during development for:
* **Learning and discussion** of unfamiliar concepts and approaches before implementation. Final decisions on the project's direction were mine.
* **Repetitive frontend work** such as CSS, where the goal was clear but the manual effort would have been disproportionate.
* **Debugging specific errors** during development: sharing the error and relevant code, understanding why it was occurring, and then applying the fix.

---

## Technical overview

**Architecture.** Three containerized services on a custom Docker network:
* Frontend (React) on port 3000
* Backend (FastAPI) on port 8000
* Database (MongoDB), internal to the Docker network

At startup the backend seeds MongoDB from the shipped CSV if the collection is empty, then loads the precomputed embedding vectors into memory.

**Scoring formula:**
```text
final_score = 0.50 * genre_match + 0.25 * similarity_to_favorite + 0.15 * rating + 0.10 * popularity
```
* `genre_match`: fraction of picked genres this movie has.
* `similarity_to_favorite`: blended similarity (only used when a favorite is provided).
* `rating`: rating / 10.
* `popularity`: log-scaled.

Weights are the defaults; users can override them per request via the Advanced panel.

**Request flow:**
1. Frontend sends preferences to the backend.
2. Backend applies hard filters (rating, year, language) as a MongoDB query to get candidates.
3. If a favorite is named, its embedding vector and tag sets are looked up.
4. Each candidate is scored using the weighted formula.
5. Top N are ranked, formatted, and returned to the frontend.
6. Frontend renders the results as cards.

More detail in `docs/documentation.pdf` (Section 10).

---

**Author:** Akash Sihag (Roll No. 20)