# CineSuggest AI: Hybrid Movie Recommendation Engine

CineSuggest AI is a movie recommendation engine designed to showcase two of the most popular recommendation paradigms in industry: **Content-Based Filtering** and **Collaborative Filtering**.

The system is built on a **Python Flask** backend implementing Scikit-Learn models, served via a **responsive, premium glassmorphism dark-mode dashboard** featuring custom SVG decorations, theatrical styling, and rich visual components.

---

## Algorithms Implemented

### 1. Content-Based Filtering
- **Vectorization**: Pipe-separated genres are cleaned and converted into numerical vectors using **TF-IDF (Term Frequency-Inverse Document Frequency)**.
- **Similarity Metric**: Recommends movies by calculating the **Cosine Similarity** between genre vectors. High similarity indicates close genre overlaps.

### 2. Collaborative Filtering
- **Data Modeling**: Builds a User-Item rating pivot matrix containing rating histories from simulated user groups.
- **Similarity Metric**: Employs **Item-Item Collaborative Filtering** using a **K-Nearest Neighbors (k-NN)** model configured with Cosine Distance. It searches for movies whose rating vectors across all users are geometrically closest.

---

## Tech Stack
- **Backend & ML**: Python, Flask, Pandas, NumPy, Scikit-Learn (TF-IDF Vectorizer, NearestNeighbors)
- **Frontend**: Vanilla HTML5, CSS3 (Custom Variables, Flexbox/Grid, Animations), Modern JS (ES6+, Fetch API), MathJax (for typesetting math formulas)
- **Deployment & Versioning**: Git-ready architecture

---

## Project Structure
```
movie-recommendation-system/
├── app.py                      # Flask backend API & routing
├── requirements.txt            # Python environment dependencies
├── README.md                   # Project documentation
├── data/
│   ├── movies.csv              # Curated movies catalog
│   └── ratings.csv             # Simulated ratings dataset
├── models/
│   └── recommender_model.py    # Hybrid recommender engine logic class
├── scripts/
│   └── generate_data.py        # Movie and rating simulator script
├── static/
│   ├── css/
│   │   └── style.css           # Premium UI stylesheet
│   └── js/
│       └── app.js              # Interactivity event handler & API requests
└── templates/
    └── index.html              # Main single-page dashboard layout
```

---

## Quick Setup & Execution

### 1. Prerequisites
Ensure you have Python 3.8+ installed.

### 2. Install Dependencies
Clone this repository (or copy folders) and install requirements:
```bash
pip install -r requirements.txt
```

### 3. Generate the Simulation Datasets
Run the dataset generator to create movies and user ratings:
```bash
python scripts/generate_data.py
```

### 4. Start the Web Server
Launch the Flask development server:
```bash
python app.py
```

### 5. View the Dashboard
Open your browser and navigate to:
[http://127.0.0.1:5001](http://127.0.0.1:5001)
