import React from "react";

const MovieCard = ({ movie, onRecommend }) => {
    const image =
        movie.poster && movie.poster !== "null"
            ? movie.poster
            : "https://via.placeholder.com/300x450?text=No+Poster";

    const description =
        movie.overview && movie.overview !== "null"
            ? movie.overview.slice(0, 80) + "..."
            : "No description available.";

    return (
        <div className="bg-gray-900 rounded-lg overflow-hidden shadow-md hover:shadow-lg transform hover:scale-105 transition duration-300">
            <img
                src={image}
                alt={movie.title}
                className="w-full h-72 object-cover"
            />
            <div className="p-3 flex flex-col justify-between min-h-[140px]">
                <h2 className="text-base font-bold text-white truncate mb-2">
                    {movie.title}
                </h2>
                <p className="text-gray-400 text-sm mb-3 line-clamp-3">{description}</p>
                <button
                    onClick={() => onRecommend(movie.title)}
                    className="w-full bg-netflixRed py-1.5 rounded font-semibold text-sm hover:bg-red-700 transition"
                >
                    Recommend Similar
                </button>
            </div>
        </div>
    );
};

export default MovieCard;
