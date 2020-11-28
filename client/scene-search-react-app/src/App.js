import React, { useEffect, useState } from 'react';
import { ClipLoader } from 'react-spinners';
import { Helmet } from 'react-helmet';
import SearchResult from './SearchResult';
import SplashScreen from './SplashScreen';
import './App.css';

function App() {

  const BASE_URL = 'http://127.0.0.1:5000';
  const GRANULARITY = '3';

  const [videoId, setVideoId] = useState('');
  const [videoTitle, setVideoTitle] = useState('');
  const [searchPhrase, setSearchPhrase] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchInput, setSearchInput] = useState('');
  const [videoInput, setVideoInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isProcessed, setIsProcessed] = useState(false);

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

  useEffect(() => {
    if (videoId.length > 0) {
      setIsLoading(true);
      fetch(`${BASE_URL}/process_video?video_id=${videoId}&granularity=${GRANULARITY}`)
        .then(res => res.json())
        .then(resJson => {
          setIsLoading(false);
          if (resJson.success) {
            setVideoTitle(resJson.video_title);
            setIsProcessed(true);
          } else {
            alert(resJson.error_message);
          }
        })
    }
  }, [videoId])

  const handleSearchSubmit = e => {
    e.preventDefault();
    setSearchQuery(searchPhrase);
    setSearchInput('');
  }

  const handleVideoSubmit = e => {
    e.preventDefault();
    setVideoId(parseVideoId(videoInput));
    setVideoInput('');
  }

  const parseVideoId = (videoUrl) => {
    if (videoUrl.split('v=').length < 2) {
      alert('Please enter a valid YouTube Url');
      return '';
    }

    var parsedVideoId = videoUrl.split('v=')[1];
    var ampersandPos = parsedVideoId.indexOf('&');
    if (ampersandPos != -1) {
      parsedVideoId = parseVideoId.substring(0, ampersandPos);
    }
    return parsedVideoId;
  }

  const handleSearchInput = e => {
    setSearchPhrase(e.target.value);
    setSearchInput(e.target.value);
  }

  return (
    <div className="App" style={!isProcessed ? { backgroundImage: "url(splashscreen.jpg)", backgroundSize: "cover", backgroundRepeat: "no-repeat", backgroundPosition: "center center" }: null }>
      <Helmet>
        <title>{"SceneSearch"}</title>
      </Helmet>

      <div>
        {!isProcessed ?
          <div className="splash-screen">
            <h1 className="App-title">SceneSearch</h1>
            <p className="description">A Video Search Engine Powered by Deep Learning</p>
            <SplashScreen videoInput={videoInput} setVideoInput={setVideoInput} onSubmit={handleVideoSubmit}/>
            {isLoading ?
              <div style={{ 'textAlign': 'center' }}>
                <h2>Processing Video...</h2>
                <p>This may take a few minutes</p>
                <br />
                <ClipLoader size={100} color={"#123abc"} />
                <br />
              </div>
              :
              null
            }
          </div>
          :
          <div>
            <header className="App-header">
              <h1>SceneSearch</h1>
            </header>
            <p className="description">{videoTitle}</p>
            <p style={{ 'textAlign': 'center' }}><a href={'https://www.youtube.com/watch?v=' + videoId} target="_blank">{'https://www.youtube.com/watch?v=' + videoId}</a></p>
            <form onSubmit={handleSearchSubmit} className="input-form">
              <input className="search-bar" type="text"placeholder={"Enter a phrase to search for relevant video scenes"} value={searchInput} onChange={handleSearchInput}/>
              <button className="submit-button" type="submit">
                Search
              </button>
            </form>

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
                    <p style={{ fontSize: 20 }}>Top Suggestions</p>
                  </div>
                  :
                  null
                }

                {searchInput.length === 0 && searchResults.length > 0 ?
                  <div style={{ 'textAlign': 'center' }}>
                    <p style={{ fontSize: 20 }}>Most Similar Search Results For <span style={{ color: 'blue' }}>"{searchQuery}"</span></p>
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
                      videoId={videoId}
                    />
                  ))}
                </div>
              </div>
             }
          </div>
         }
      </div>
    </div>
  );
}

export default App;
