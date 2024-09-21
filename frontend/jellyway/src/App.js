import React, { useState } from 'react';
import './App.css';

function App() {

  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = () => {
    setIsLoggedIn(true); // Update state to indicate the user is logged in
  };

  return (
    <main>
      <div className="jellyway">
        <header className="toolbar">
          <div className="toolbar-left">
            <img src={require('./grafics/logo_jellyway.png')} className="App-logo" alt="logo" />
            <span className="toolbar-title">JELLY WAY</span>
          </div>
        </header>
      </div>
      <div className="frame-uptime">
        <h1>Uptime METRO</h1>
      </div>
      <div className="checkbox">
            <input type="checkbox" id="chk" aria-hidden="true" />

            <div className="signup">
                <form>
                    <label htmlFor="chk" aria-hidden="true">Sign up</label>
                    <input type="text" name="txt" placeholder="User name" required />
                    <input type="email" name="email" placeholder="Email" required />
                    <input type="number" name="broj" placeholder="BrojTelefona" required />
                    <input type="password" name="pswd" placeholder="Password" required />
                    <button type="submit">Sign up</button>
                </form>
            </div>

            <div className="login">
                <form>
                    <label htmlFor="chk" aria-hidden="true">Login</label>
                    <input type="email" name="email" placeholder="Email" required />
                    <input type="password" name="pswd" placeholder="Password" required />
                    <button type="submit">Login</button>
                </form>
            </div>
        </div>
    </main>
  );
}

export default App;