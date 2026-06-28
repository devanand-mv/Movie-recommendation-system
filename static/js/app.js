/**
 * CineSuggest AI Frontend Controller
 * Directs page load loads, user selection toggles, API calling, and card layout drawing.
 */

document.addEventListener("DOMContentLoaded", () => {
    // Inputs & buttons
    const movieSelect = document.getElementById("movie-select");
    const btnGenerate = document.getElementById("btn-generate");
    const methodRadios = document.getElementsByName("method");
    const btnContent = document.getElementById("btn-content");
    const btnCollaborative = document.getElementById("btn-collaborative");

    // UI blocks
    const emptyState = document.getElementById("empty-state");
    const resultsHeadline = document.getElementById("results-headline");
    const queryMovieTitle = document.getElementById("query-movie-title");
    const activeMethodBadge = document.getElementById("active-method-badge");
    const movieGrid = document.getElementById("movie-grid");

    // Navigation tabs
    const navRecommender = document.getElementById("nav-recommender");
    const navDocs = document.getElementById("nav-docs");
    const recommenderSection = document.getElementById("recommender-section");
    const docsSection = document.getElementById("docs-section");

    // Tab switching
    navRecommender.addEventListener("click", () => {
        navRecommender.classList.add("active");
        navDocs.classList.remove("active");
        recommenderSection.classList.add("active");
        docsSection.classList.remove("active");
    });

    navDocs.addEventListener("click", () => {
        navDocs.classList.add("active");
        navRecommender.classList.remove("active");
        docsSection.classList.add("active");
        recommenderSection.classList.remove("active");
        
        // Retrigger MathJax typesetting if available when document shows
        if (window.MathJax) {
            window.MathJax.typeset();
        }
    });

    // Toggle button handler
    btnContent.addEventListener("click", () => {
        btnContent.classList.add("active");
        btnCollaborative.classList.remove("active");
        document.querySelector('input[name="method"][value="content"]').checked = true;
    });

    btnCollaborative.addEventListener("click", () => {
        btnCollaborative.classList.add("active");
        btnContent.classList.remove("active");
        document.querySelector('input[name="method"][value="collaborative"]').checked = true;
    });

    // 1. Fetch movies and populate dropdown
    fetch("/api/movies/list")
        .then(res => res.json())
        .then(data => {
            movieSelect.innerHTML = '<option value="">-- Choose a Movie --</option>';
            data.forEach(movie => {
                const opt = document.createElement("option");
                opt.value = movie.movieId;
                opt.textContent = movie.title;
                movieSelect.appendChild(opt);
            });
        })
        .catch(err => {
            console.error("Error loading movie catalog:", err);
            movieSelect.innerHTML = '<option value="">Failed to load movies</option>';
        });

    // 2. Click handler to call recommendations
    btnGenerate.addEventListener("click", () => {
        const movieId = movieSelect.value;
        if (!movieId) {
            alert("Please select a movie from the dropdown first!");
            return;
        }

        const selectedMethod = document.querySelector('input[name="method"]:checked').value;
        
        // Show loading state
        btnGenerate.disabled = true;
        btnGenerate.textContent = "Analyzing Catalog...";

        fetch("/api/movies/recommend", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                movieId: parseInt(movieId),
                method: selectedMethod,
                top_n: 6
            })
        })
        .then(res => res.json())
        .then(data => {
            btnGenerate.disabled = false;
            btnGenerate.textContent = "Generate Recommendations";

            if (data.error) {
                alert("Error: " + data.error);
                return;
            }

            renderRecommendations(data);
        })
        .catch(err => {
            btnGenerate.disabled = false;
            btnGenerate.textContent = "Generate Recommendations";
            console.error("Network error:", err);
            alert("A network error occurred. Please check console.");
        });
    });

    // Genre-to-emoji mapping helper
    function getGenreEmoji(genreString) {
        const genres = genreString.split("|");
        const primary = genres[0].toLowerCase();
        
        const emojiMap = {
            "action": "💥",
            "adventure": "🧭",
            "animation": "🎨",
            "comedy": "😂",
            "crime": "🕵️",
            "drama": "🎭",
            "fantasy": "✨",
            "sci-fi": "🚀",
            "thriller": "😱",
            "romance": "💖",
            "mystery": "🔍",
            "musical": "🎵"
        };
        
        return emojiMap[primary] || "🍿";
    }

    // Render recommendation grid
    function renderRecommendations(response) {
        // Toggle view blocks
        emptyState.style.display = "none";
        resultsHeadline.style.display = "flex";
        movieGrid.style.display = "grid";

        // Set labels
        queryMovieTitle.textContent = response.query_movie.title;
        activeMethodBadge.textContent = response.method === "content" ? "Content-Based" : "Collaborative Filtering";
        activeMethodBadge.style.borderColor = response.method === "content" ? "var(--border-purple)" : "var(--border-pink)";
        activeMethodBadge.style.color = response.method === "content" ? "var(--primary)" : "var(--accent)";

        // Clear grid
        movieGrid.innerHTML = "";

        if (response.recommendations.length === 0) {
            movieGrid.innerHTML = '<div class="empty-state" style="grid-column: 1/-1;"><h3>No Matches Found</h3><p>The Collaborative Filtering engine did not find similar rating profiles. Try Content-Based filtering!</p></div>';
            return;
        }

        // Draw cards
        response.recommendations.forEach(movie => {
            const card = document.createElement("div");
            card.className = "movie-card";

            // Format match score percentage
            const matchScore = (movie.score * 100).toFixed(1);
            const emoji = getGenreEmoji(movie.genres);

            // Generate genre pills html
            const genrePillsHtml = movie.genres.split("|").map(genre => {
                const classFriendly = genre.toLowerCase().replace(/[^a-z0-9]/g, "-");
                return `<span class="genre-pill genre-${classFriendly}">${genre}</span>`;
            }).join("");

            card.innerHTML = `
                <div class="movie-poster-mock">
                    <span class="match-badge">${matchScore}% Match</span>
                    <span class="poster-icon">${emoji}</span>
                </div>
                <div class="movie-card-info">
                    <h4 class="movie-card-title">${movie.title}</h4>
                    <div class="genre-container">
                        ${genrePillsHtml}
                    </div>
                </div>
            `;

            movieGrid.appendChild(card);
        });
    }
});
