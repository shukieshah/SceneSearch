import React, { useEffect, useState } from 'react';
import { ClipLoader } from 'react-spinners';
import { Helmet } from 'react-helmet';
import SearchResult from './SearchResult';
import './App.css';

function App() {

  const BASE_URL = 'http://127.0.0.1:5000';

  const [videoUrl, setVideoUrl] = useState('https://www.youtube.com/watch?v=fHeQemJJQII');
  const [videoId, setVideoId] = useState('fHeQemJJQII');
  const [searchPhrase, setSearchPhrase] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchInput, setSearchInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    fetch(`${BASE_URL}/search_as_you_type?video_id=${videoId}&search_phrase=${searchPhrase}`)
      .then(res => res.json())
      .then(resJson =>  {
        setSearchResults(resJson.results);
      })
  }, [searchPhrase])

  useEffect(() => {
    if (searchQuery.length > 0) {
      setIsLoading(true);
      fetch(`${BASE_URL}/search_similar?video_id=${videoId}&search_phrase=${searchQuery}`)
        .then(res => res.json())
        .then(resJson => {
          setSearchResults(resJson.results);
          setIsLoading(false);
        })
    }
  }, [searchQuery])


  const handleSubmit = e => {
    e.preventDefault();
    setSearchQuery(searchPhrase);
    setSearchInput('');
  }

  const handleSearchInput = e => {
    setSearchPhrase(e.target.value);
    setSearchInput(e.target.value);
  }

  return (
    <div className="App">
      <Helmet>
        <title>{"SceneSearch"}</title>
      </Helmet>

      <header className="App-header">
        <h1 className="App-title">SceneSearch</h1>
      </header>

      <form onSubmit={handleSubmit} className="search-form">
        <input className="search-bar" type="text"placeholder={"Enter a phrase to search for relevant video scenes"} value={searchInput} onChange={handleSearchInput}/>
        <button className="search-button" type="submit">
          Search
        </button>
      </form>

      <div>
      {isLoading ?
        <div style={{ 'textAlign': 'center' }}>
          <h2>Searching...</h2>
          <br />
          <ClipLoader size={100} color={"#123abc"} />
          <br />
        </div>
        :

        <div>
        {searchInput.length > 0 && searchResults.length > 0 ?
          <div style={{ 'textAlign': 'center' }}>
            <h2>Top Suggestions</h2>
          </div>
          :
          null
        }

        {searchInput.length === 0 && searchResults.length > 0 ?
          <div style={{ 'textAlign': 'center' }}>
            <h2>Most Similar Search Results for "{searchQuery}"</h2>
          </div>
          :
          null
        }

        <div className="search-results">
        {searchResults.map(searchResult => (
          <SearchResult
            key={searchResult.document.timestamp}
            caption={searchResult.document.caption}
            timestamp={searchResult.document.timestamp}
            image={searchResult.document.image_path}
            searchInput={searchPhrase}
            videoUrl={videoUrl}
          />
        ))}
        </div>
        </div>
      }
      </div>
    </div>
  );
}

export default App;
