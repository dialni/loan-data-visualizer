import './App.css';
import * as Plot from "@observablehq/plot";
import PlotFigure from "./PlotFigure.jsx";
import { useEffect, useState } from 'react';

function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("http://localhost:xxxx/get-timeframe") // Change this to correct port
    .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((json) => {
        setData(json);
      })}, []);
  console.log("data:")
  console.log(data);

  return (
    <>
      <header>
        <h1>Loan Data Visualizer</h1>
      </header>
      <main>
        <section id='graph'>
          <div>
            <PlotFigure
              options={{
               color: {legend: true},
                marks: [
                  Plot.ruleY([0]),
                  Plot.lineY(data, {x: d => new Date(d.date * 1000), y: "reqAmount"})
                ]
              }}
            />
          </div>
        </section>
        <section id='info'>
          <div>
            <h2>What is Loan Data Visualizer?</h2>
            <p>This is a project that aims to visualize the online, private market of <a href="https://en.wikipedia.org/wiki/Peer-to-peer_lending" target="_blank">"peer-to-peer lending"</a> on public forums. Using Python, Postgres, and various libraries in Docker containers.</p>
            <p>These "peer-to-peer lending" forums deal outside of any traditional institutions, and therefore all posts and transactions are public in lieu of a standard credit rating. As such, we can see the live market activity and produce some statistics.</p>
            <p>The source code is available on <a href="https://github.com/dialni/loan-data-visualizer" target='_blank'>GitHub</a>.</p>
            <p>This tool was developed for educational purposes, as a side-project to test various technologies, and should not be involved in any decisions, finanical or otherwise.</p>
          </div>
          <div>
            <h2>Privacy Policy</h2>
            <p>In accordance with <a href='https://redditinc.com/policies/data-api-terms' target='_blank'>Reddit's Data API rules</a>, no identifiable information is stored. All stored data is deleted, gathered and then anonymized every 24 hours. [deleted] users content or data is not stored.</p>
            <p>This project only stores the following public data from the posts made on certain subreddits:</p>
            <ul>
              <li>Timestamp of post</li>
              <li>The tag in posts, e.g. [REQ], [PAID], etc.</li>
              <li>Monetary amounts specified in post, e.g. 500 USD</li>
              <li>Whether someone has replied to post with loan confirmation, or title contains "Pre-arranged"</li>
            </ul>
            <p>No cookies are used on this site.</p>
            <p>Any complaints or concerns are welcome at [MAKE FORWARDER EMAIL]</p>
          </div>
        </section>
      </main>
    </>
  )
}

export default App
