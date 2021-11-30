import logo from './logo.svg';
import { BrowserRouter, Link, Routes, Route } from 'react-router-dom';
import './App.css';

import Listeners from './components/listeners/Listeners'
import Artists from './components/artists/Artists';

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        
        <header className="App-header">
          <h1>Music Recommender</h1>
        </header>
          {/* <div className="subheader">
            <div className = 'page-links'>
              <Link className = 'App-link' to="/">LISTENERS</Link>
              <Link className = 'App-link' to="/artists">ARTISTS</Link>
            </div>
          </div> */}
        {/* <Routes>
          <Route path = "/artists" element = {<Artists/>}> 
          </Route>
          <Route path = "/" element={<Listeners/>}> 
          </Route>
        </Routes> */}

        <Artists></Artists>
        <Listeners></Listeners>
      </div>
    </BrowserRouter>
  );
}

export default App;
