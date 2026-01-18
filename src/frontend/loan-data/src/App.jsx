// Libraries
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

// Pages
import './App.css';
import Dashboard from './pages/Dashboard/Dashboard.jsx'
import About from './pages/About.jsx'
import PrivacyPolicy from './pages/PrivacyPolicy.jsx'
import NotFound from './pages/NotFound.jsx'

export default function App() {
  return (
    <div className='app'>
      <BrowserRouter>
        <aside>
          <h1>dialni.com</h1>
          <nav>
            <ul>
              <li><Link to='/'>Dashboard</Link></li>
              <li><Link to='/about'>What is this?</Link></li>
              <li><Link to='/privacy-policy'>Privacy Policy</Link></li>
              <li><a href='https://github.com/dialni/loan-data-visualizer' target='_blank'>GitHub</a></li>
            </ul>
          </nav>
        </aside>
        <main>
          <Routes>
            <Route index element={<Dashboard />} />
            <Route path="/about" element={<About />} />
            <Route path="/privacy-policy" element={<PrivacyPolicy />} />
            <Route path="/*" element={<NotFound />} />
          </Routes>
        </main>
      </BrowserRouter>
    </div>
  );
}