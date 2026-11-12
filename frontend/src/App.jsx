
import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [movies, setMovies] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [searched, setSearched] = useState(false);
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [detailsLoading, setDetailsLoading] = useState(false);
  const [rating, setRating] = useState(5);
  const [ratingMessage, setRatingMessage] = useState("");
  const [ratingError, setRatingError] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${API_URL}/recommendations/1`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch recommendations");
        }
        return response.json();
      })
      .then((data) => {
        setMovies(data.recommendations);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error:", error);
        setError("Unable to load movie recommendations.");
        setLoading(false);
      });
  }, []);

  const handleSearch = async () => {
    if (!searchTerm.trim()) {
      setSearchResults([]);
      setSearched(false);
      return;
    }

    setIsSearching(true);
    setSearched(true);
    setSelectedMovie(null);
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/movies/search?title=${encodeURIComponent(searchTerm)}`
      );

      if (!response.ok) {
        throw new Error("Movie search failed");
      }

      const data = await response.json();
      setSearchResults(data);
    } catch (error) {
      console.error("Search error:", error);
      setError("Unable to search movies.");
      setSearchResults([]);
    } finally {
      setIsSearching(false);
    }
  };

  const handleMovieClick = async (movieId) => {
    setDetailsLoading(true);
    setSelectedMovie(null);
    setRatingMessage("");
    setRatingError("");
    setRating(5);
    setError("");

    try {
      const response = await fetch(`${API_URL}/movies/${movieId}`);

      if (!response.ok) {
        throw new Error("Failed to fetch movie details");
      }

      const data = await response.json();
      setSelectedMovie(data);
    } catch (error) {
      console.error("Details error:", error);
      setError("Unable to load movie details.");
    } finally {
      setDetailsLoading(false);
    }
  };

  const handleRatingSubmit = async () => {
    setRatingMessage("");
    setRatingError("");

    try {
      const response = await fetch(`${API_URL}/ratings`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: 1,
          movie_id: selectedMovie.id,
          rating: Number(rating),
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Unable to submit rating");
      }

      setRatingMessage("Your rating was submitted successfully!");
    } catch (error) {
      console.error("Rating error:", error);
      setRatingError(error.message || "Unable to submit rating.");
    }
  };

  const closeDetails = () => {
    setSelectedMovie(null);
    setRatingMessage("");
    setRatingError("");
  };

  return (
    <div className="app">
      <header className="header">
        <h1>Movie Recommendation System</h1>
        <p>Discover movies recommended just for you!</p>
      </header>

      <section className="search-section">
        <h2>Search Movies</h2>

        <div className="search-bar">
          <input
            type="text"
            placeholder="Enter movie title..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") handleSearch();
            }}
          />

          <button onClick={handleSearch} disabled={isSearching}>
            {isSearching ? "Searching..." : "Search"}
          </button>
        </div>
      </section>

      {detailsLoading && (
        <p className="loading">Loading movie details...</p>
      )}

      {selectedMovie && (
        <section className="movie-details">
          <h2>Movie Details</h2>

          <p><strong>Movie ID:</strong> {selectedMovie.id}</p>
          <h3>{selectedMovie.title}</h3>
          <p><strong>Genres:</strong> {selectedMovie.genre}</p>

          <div className="rating-section">
            <h3>Rate this movie</h3>

            <select
              value={rating}
              onChange={(e) => setRating(Number(e.target.value))}
            >
              {[1, 2, 3, 4, 5].map((value) => (
                <option key={value} value={value}>
                  {value} Star{value > 1 ? "s" : ""}
                </option>
              ))}
            </select>

            <button onClick={handleRatingSubmit}>
              Submit Rating
            </button>

            {ratingMessage && (
              <p className="success">{ratingMessage}</p>
            )}

            {ratingError && (
              <p className="error">{ratingError}</p>
            )}
          </div>

          <button onClick={closeDetails}>Close Details</button>
        </section>
      )}

      {searched ? (
        <section>
          <h2>Search Results</h2>

          {isSearching && (
            <p className="loading">Searching movies...</p>
          )}

          {!isSearching && searchResults.length === 0 && (
            <p>No movies found. Try another title.</p>
          )}

          <div className="movie-grid">
            {searchResults.map((movie) => (
              <div
                className="movie-card"
                key={movie.id}
                onClick={() => handleMovieClick(movie.id)}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => {
                  if (e.key === "Enter") handleMovieClick(movie.id);
                }}
              >
                <p className="movie-id">MOVIE ID: {movie.id}</p>
                <h3>{movie.title}</h3>
                <p>Genres: {movie.genre}</p>
                <p>Click to view details</p>
              </div>
            ))}
          </div>
        </section>
      ) : (
        <section>
          <h2>Recommended Movies for You</h2>

          {loading && (
            <p className="loading">Loading movies...</p>
          )}

          <div className="movie-grid">
            {movies.map((movie) => (
              <div
                className="movie-card"
                key={movie.movieId}
                onClick={() => handleMovieClick(movie.movieId)}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => {
                  if (e.key === "Enter") handleMovieClick(movie.movieId);
                }}
              >
                <p className="movie-id">
                  MOVIE ID: {movie.movieId}
                </p>
                <h3>{movie.title}</h3>
                <p>
                  Genres: {movie.genres.split("|").join(", ")}
                </p>
                <p>Click to view details</p>
              </div>
            ))}
          </div>
        </section>
      )}

      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default App;
