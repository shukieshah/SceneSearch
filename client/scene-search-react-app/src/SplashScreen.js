import React, { useState } from 'react';

const SplashScreen = ({videoInput, setVideoInput, onSubmit}) => {
  const handleInput = e => {
    setVideoInput(e.target.value);
  }

  return (
    <form onSubmit={onSubmit} className="input-form">
      <input className="input-bar" type="text"placeholder={"Enter a YouTube Video URL (e.g. www.youtube.com/watch?v=fHeQemJJQII)"} value={videoInput} onChange={handleInput}/>
      <button className="submit-button" type="submit">
        Process Video
      </button>
    </form>
  )
}

export default SplashScreen;
