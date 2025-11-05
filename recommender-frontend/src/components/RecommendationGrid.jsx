import React from "react";
import MovieCard from "./MovieCard";

const RecommendationGrid = ({ movies, onRecommend }) => {
    // filter out duplicate titles (some models may repeat them)
    const uniqueMovies = movies.filter(
        (v, i, a) => a.findIndex((m) => m.title === v.title) === i
    );

    return (
        <div className="px-6 mt-24">
            <h2 className="text-2xl font-bold mb-6">Recommended Movies</h2>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
                {uniqueMovies.map((movie, index) => (
                    <MovieCard key={index} movie={movie} onRecommend={onRecommend} />
                ))}
            </div>
        </div>
    );
};

export default RecommendationGrid;
