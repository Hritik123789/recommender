import React from "react";

const Navbar = ({ onSearch }) => {
    const [query, setQuery] = React.useState("");

    const handleSubmit = (e) => {
        e.preventDefault();
        if (query.trim()) {
            onSearch(query);
            setQuery("");
        }
    };

    return (
        <nav className="bg-black/90 backdrop-blur-md p-4 flex flex-col sm:flex-row justify-between items-center fixed top-0 w-full z-10 shadow-lg">
            <h1 className="text-3xl font-extrabold text-netflixRed tracking-wide mb-3 sm:mb-0">
                🎬 CineMatch
            </h1>
            <form onSubmit={handleSubmit} className="flex w-full sm:w-auto">
                <input
                    type="text"
                    placeholder="Search for a movie..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    className="bg-gray-800 text-white px-4 py-2 rounded-l-md outline-none w-full sm:w-72"
                />
                <button
                    type="submit"
                    className="bg-netflixRed px-4 py-2 rounded-r-md font-semibold hover:bg-red-700 transition"
                >
                    Search
                </button>
            </form>
        </nav>
    );
};

export default Navbar;
