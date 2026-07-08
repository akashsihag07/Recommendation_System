# Installation Guide

This guide walks you through setting up and running the project using Docker.

---

## 1. Setup

### 1.1 Prerequisites

- Only [Docker Desktop](https://www.docker.com/products/docker-desktop/) is required.
  - 📺 [Download for Windows](https://youtu.be/JBEUKrjbWqg?si=bWziNF3Za16TdRNs)
  - 📺 [Download for Mac](https://youtu.be/agkOZr27d3Y?si=APhnyP59NMtOpIAb)
- Launch Docker Desktop and wait for the whale icon to show it is running.
- Confirm the installation by running:

  ```bash
  docker --version
  ```

  A version number should be printed.

---

### 1.2 Getting the Project Code

> Use **Option A** if you have Git or developer tools already installed on your system.
> If not, use **Option B** instead.

**Option A — Using Git**

```bash
git clone https://github.com/akashsihag07/Recommendation_System 20_Akash_TechnicalProject
cd 20_Akash_TechnicalProject
```

> You can rename `20_Akash_TechnicalProject` in the command above to any folder name you prefer.

**Option B — Downloading the ZIP**

1. Open [https://github.com/akashsihag07/Recommendation_System](https://github.com/akashsihag07/Recommendation_System)
2. Click the green **Code** button, then **Download ZIP**.
3. Extract the ZIP file.
4. Rename the extracted folder to `20_Akash_TechnicalProject` (or any name you prefer).
5. Open a terminal and change directory into that folder.

---

### 1.3 Running the Application

From inside the project folder, run:

```bash
docker compose up --build
```

- **First run:** takes about 2–3 minutes.
- **Later runs:** start within seconds.

Once running, access the application here:

| Service   | URL |
|-----------|-----|
| App       | [http://localhost:3000](http://localhost:3000) |
| API Docs  | [http://localhost:8000/docs](http://localhost:8000/docs) |

---

### 1.4 Stopping the Application

```bash
docker compose down
```

---