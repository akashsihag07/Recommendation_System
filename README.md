# WatchHub

*Find your next movie without the endless scrolling.*

A movie recommendation web app built around one idea: the ranking logic should be visible to the user, and it should be adjustable.

![WatchHub interface](docs/screenshots/img01_form.png)

> **This README is a project overview.** For the full technical details, including expanded architecture diagrams, request-flow walkthrough, per-module backend explanation, and the recommendation logic broken down in depth, see [`docs/documentation.pdf`](docs/documentation.pdf).

---

## Table of Contents

- [About the project](#about-the-project)
- [Why I chose this project](#why-i-chose-this-project)
- [What is special about it](#what-is-special-about-it)
- [System architecture](#system-architecture)
- [Architecture workflow](#architecture-workflow)
- [How the recommendation works](#how-the-recommendation-works)
- [Data preparation](#data-preparation)
- [Tools used](#tools-used)
- [Project structure](#project-structure)
- [Documentation](#documentation)
- [Sources and declarations](#sources-and-declarations)
- [AI usage declaration](#ai-usage-declaration)
- [Future scope](#future-scope)

---

## About the project

WatchHub is a movie recommendation web application. Given a set of preferences (genres, language, minimum rating, or a favorite movie), the app returns a ranked list of matches from a multilingual catalogue of approximately 43,000 films.

- Three containerized services: React frontend, FastAPI backend, MongoDB database.
- One Docker Compose command starts everything.
- No API keys, no external services, no configuration required.

For setup, see [`INSTALL.md`](INSTALL.md). For how to use the app, see [`USER_MANUAL.md`](USER_MANUAL.md). For full technical details, see [`docs/documentation.pdf`](docs/documentation.pdf).

---

## Why I chose this project

- **The data is clean and publicly available.** TMDB provides all the fields a recommender needs (genres, ratings, overviews, keywords) without scraping. Build time went into the recommender logic, not into data acquisition.
- **I know the domain well.** I could audit my own outputs at every step and recognize a wrong result without external verification.
- **The scope is well defined.** A movie recommender has a clear notion of what "working" looks like, which let me focus on execution quality from day one.
- **Existing apps have real gaps I wanted to address.** Weak multilingual coverage, opaque ranking systems, and no user control over how recommendations are weighted. These became direct build targets.

---

## What is special about it

- **Blended similarity using two techniques** for "more like this movie" matching: Jaccard similarity on structured tags combined with cosine similarity on sentence embeddings of plot overviews.
- **User-adjustable ranking weights** exposed as four sliders (Genre, Similarity, Rating, Popularity) in an Advanced panel. The scoring formula is not hidden or fixed.
- **Multilingual catalogue with a language filter.** Dozens of languages, not Hollywood-only.
- **Real posters and trailer links** on every card, loaded live from TMDB.
- **Plug-and-play deployment.** One Docker Compose command, no API keys.

### The blend in action: Jaccard vs Jaccard + embeddings

The clearest demonstration of the blend's value is a search with "Batman v Superman: Dawn of Justice" as the favorite movie.

**With Jaccard only** (structured tags: genres and keywords):

| Rank | Result |
|------|--------|
| 1 | Zack Snyder's Justice League |
| 2 | The Lord of the Rings: The Return of the King |
| 3 | The Lord of the Rings: The Fellowship of the Ring |
| 4 | The Lord of the Rings: The Two Towers |

Lord of the Rings ranks high because it shares broad genre tags (Action, Adventure, Fantasy) with Batman v Superman, but the stories are unrelated. Jaccard cannot see that.

**With Jaccard + sentence embeddings** (structured tags plus plot meaning):

| Rank | Result |
|------|--------|
| 1 | Zack Snyder's Justice League |
| 2 | The Dark Knight |
| 3 | Justice League: Warworld |
| 4 | Spider-Man: Across the Spider-Verse |

Lord of the Rings drops out entirely. The top results become thematically appropriate: other DC entries, a related Batman origin, and other superhero-versus-superhero conflicts. The tag component keeps results grounded; the embedding component captures plot meaning.

For screenshots of both cases and the full technical explanation, see [`docs/documentation.pdf`](docs/documentation.pdf) (Section 4).

---

## System architecture

The application runs as three independent services in Docker containers, connected over a private internal network.

```
+-----------------------------------------------------------+
|                    User's Web Browser                     |
+-----------------------------------------------------------+
                             |
                             |  HTTP  (port 3000)
                             v
+-----------------------------------------------------------+
|  Frontend Container                                       |
|  React (Vite build) served by nginx                       |
+-----------------------------------------------------------+
                             |
                             |  HTTP / JSON  (port 8000)
                             v
+-----------------------------------------------------------+
|  Backend Container                                        |
|  Python 3.11 + FastAPI + Uvicorn                          |
|                                                           |
|  In memory at startup:                                    |
|    - overview_vectors.npz  (43,000 x 384 embeddings)      |
+-----------------------------------------------------------+
                             |
                             |  MongoDB protocol (internal)
                             v
+-----------------------------------------------------------+
|  Database Container                                       |
|  MongoDB (not exposed outside the Docker network)         |
+-----------------------------------------------------------+


Offline (one-time, in Kaggle):
   Plot overviews  --->  Sentence embedding model  --->  overview_vectors.npz
                        (all-MiniLM-L6-v2 on GPU)
   The .npz file ships with the repo and is loaded by the backend at startup.
```

- The **frontend** is a React single-page app built with Vite and served as static files by nginx. It talks to the backend over HTTP.
- The **backend** exposes REST endpoints, runs the scoring logic, and queries MongoDB. It also holds the precomputed embedding vectors in memory for fast cosine similarity.
- The **database** stores the ~43,000 movie documents. It is internal to the Docker network and not reachable from outside.
- The **embedding model** is not part of the runtime. It runs once, offline, in a Kaggle notebook, and produces the `.npz` file that ships with the repo.

For a properly rendered architecture diagram and per-service detail, see [`docs/documentation.pdf`](docs/documentation.pdf) (Section 8.1).

---

## Architecture workflow

The end-to-end flow when a user clicks "Find my movies":

```
Step 1:  User picks preferences in the UI
         (genres, language, minimum rating, favorite movie, optional weights)

              |
              v

Step 2:  Frontend sends preferences as JSON
         POST /recommend  --->  Backend

              |
              v

Step 3:  Backend builds a MongoDB query from the hard filters
         (vote_count >= 25, min_rating, year range, language)

              |
              v

Step 4:  MongoDB returns candidate movies

              |
              v

Step 5:  If a favorite movie is named:
           - Look up its embedding vector (from memory)
           - Look up its genre + keyword tags

              |
              v

Step 6:  For each candidate movie, compute the four score components:
           - genre_match       (fraction of picked genres present)
           - similarity        (blended: 0.7 * cosine + 0.3 * jaccard)
           - rating            (movie.rating / 10)
           - popularity        (log-scaled)

           Combine with weights:
           final_score = 0.50*genre + 0.25*similarity + 0.15*rating + 0.10*popularity

              |
              v

Step 7:  Sort candidates by final_score, take top N
         Format each with title, poster path, trailer link, metadata

              |
              v

Step 8:  Backend returns JSON to Frontend
         Frontend renders each result as a card in the grid
```

---

## How the recommendation works

Every candidate movie is scored using a weighted sum of four components:

```
final_score = 0.50 * genre_match
            + 0.25 * similarity_to_favorite
            + 0.15 * rating
            + 0.10 * popularity
```

- **genre_match**: the fraction of the user's picked genres that this movie has.
- **similarity_to_favorite**: the blended similarity described above, used only when a favorite movie is provided.
- **rating**: the movie's rating divided by 10.
- **popularity**: log-scaled so blockbusters don't dominate.

Hard filters (minimum rating, year range, language) are applied first as a database query, so scoring only runs on movies that already passed the filters. Default weights can be overridden per request via the Advanced panel in the UI.

For the full derivation of each component, the popularity log-scaling formula, and a per-file backend walkthrough, see [`docs/documentation.pdf`](docs/documentation.pdf) (Section 8.3 and 8.4).

---

## Data preparation

- **Source**: *TMDB Movies Dataset* by asaniczka on Kaggle, ~1.45 million rows.
- **Pivot from two datasets to one.** Started with TMDB 5000 + IMDb India, hit real problems (mismatched popularity scales, clashing genre vocabularies, missing overviews on one source), and switched to a single unified dataset that solved them at the source.
- **Filtering to a quality subset** (done offline in Kaggle):
    - `vote_count >= 25`
    - Non-empty `genres` and `overview`
    - `adult == False`
    - Result: ~43,000 movies.
- **Cleaning the rows** (in `cleaning.py`): split comma-separated genres and keywords into lists, extract the year from `release_date`, safely cast numeric fields, drop rows still missing essentials.
- **Precomputing embeddings offline.** Sentence embeddings for ~43,000 overviews are generated once in a Kaggle notebook (GPU-accelerated), saved as a compressed `.npz` file (~30 MB, float16), and loaded into memory at backend startup. The embedding model is never present in the runtime container.

More detail on each step in [`docs/documentation.pdf`](docs/documentation.pdf) (Section 5).

---

## Tools used

**Frontend**
- React (plain JavaScript, no TypeScript)
- Vite (build tool)
- nginx (serves the built static files)

**Backend**
- Python 3.11
- FastAPI (web framework)
- Pydantic (schema validation)
- Uvicorn (ASGI server)

**Database**
- MongoDB
- PyMongo (Python driver)

**ML (used offline in Kaggle)**
- sentence-transformers
- all-MiniLM-L6-v2 pre-trained model
- NumPy (runtime vector math)

**Orchestration**
- Docker
- Docker Compose

---

## Project structure

```
Recommendation_System/
├── README.md
├── INSTALL.md
├── USER_MANUAL.md
├── docker-compose.yml
├── backend/
│   ├── app/
│   │   ├── cleaning.py         # turns one CSV row into a clean movie record
│   │   ├── config.py           # env vars and file paths
│   │   ├── database.py         # MongoDB connection
│   │   ├── main.py             # FastAPI entry, startup wiring
│   │   ├── recommender.py      # the main ranking function
│   │   ├── schemas.py          # request and response models
│   │   ├── scoring.py          # weighted scoring components
│   │   ├── seed.py             # loads the CSV into MongoDB once
│   │   ├── vectors.py          # loads embeddings, cosine similarity
│   │   └── routers/            # per-endpoint route files
│   ├── data/
│   │   ├── tmdb_movies_clean.csv    # ~43,000 movies, ~19 MB
│   │   └── overview_vectors.npz     # ~43,000 vectors, ~30 MB
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/         # cards, form, filters, results grid
│   │   ├── hooks/              # genres, languages, recommendations
│   │   ├── api/                # fetch wrappers
│   │   ├── utils/              # poster URL builder, trailer link, etc.
│   │   └── styles/             # CSS
│   ├── Dockerfile
│   └── package.json
└── docs/
    ├── documentation.pdf       # full project documentation
    └── screenshots/            # screenshots referenced by docs
```

---

## Documentation

- [`INSTALL.md`](INSTALL.md): installation guide (prerequisites, cloning, and running the app).
- [`USER_MANUAL.md`](USER_MANUAL.md): user manual (how to use each part of the interface).
- [`docs/documentation.pdf`](docs/documentation.pdf): **full project documentation**, including in-depth technical overview, expanded architecture diagrams (system architecture, offline embedding pipeline, request-to-response workflow), per-module backend walkthrough, and the complete recommendation logic. Recommended reading for reviewers who want the technical depth behind the summary above.

---

## Sources and declarations

- **Movie data**: [TMDB Movies Dataset](https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies) by asaniczka on Kaggle, originally from [The Movie Database](https://www.themoviedb.org/). Attribution required by TMDB's terms of use.
- **Movie posters**: loaded live from `image.tmdb.org` at display time. Only the short poster path is stored locally.
- **Sentence embedding model**: [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) from the sentence-transformers library. Used offline, not a runtime dependency.
- **Frameworks and libraries** (all open source, standard permissive licenses): React, Vite, FastAPI, Pydantic, Uvicorn, MongoDB, PyMongo, NumPy, Docker, Docker Compose.

---

## AI usage declaration

As permitted by the project brief, AI assistants (Claude and Gemini) were used during development for:

- **Learning and discussion** of unfamiliar concepts and approaches before implementation. Final decisions on the project's direction were mine.
- **Repetitive frontend work** such as CSS, where the goal was clear but the manual effort would have been disproportionate.
- **Debugging specific errors** during development: sharing the error and relevant code, understanding why it was occurring, and then applying the fix.

---

## Future scope

Natural next steps that would extend this project meaningfully:

- **Cast and director as a similarity signal.** Currently the "more like this movie" feature uses plot overviews and structured tags. Adding cast and director as a fourth signal (via a Jaccard-style overlap on the shared cast set) would let users find "more Christopher Nolan films" or "more Tom Hanks dramas" naturally.

- **Live TMDB API sync.** The dataset is a snapshot. A scheduled job that pulls new releases from the TMDB API and appends them to MongoDB (with embeddings regenerated for the new entries) would keep the catalogue current.

- **Collaborative filtering.** The current recommender is entirely content-based (matching by movie attributes). Adding a "users who liked X also liked Y" signal would require user accounts and rating history, but it is the natural next step for any real recommender system.

- **Public cloud deployment.** The app currently runs locally via Docker Compose. Deploying to a managed platform (Fly.io, Render, or a Kubernetes cluster) would make it publicly reachable without a local install, closer to a real product experience.

---

**Author**: Akash Sihag (Roll No. 20)  
**Project**: Technical Project submission