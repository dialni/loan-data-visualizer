import './App.css';
import * as Plot from "@observablehq/plot";
import PlotFigure from "./components/PlotFigure.jsx";
import DataPanel from './components/DataPanels/DataPanel.jsx';
import { useEffect, useState } from 'react';

function App() {
  const [data, setData] = useState([]);

  // For actual production use
/*  useEffect(() => {
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
*/
  // Load dummy data for live-editing
  useEffect(() => {
    const dummy_data=[{date:1768492631,reqCount:24,activeCount:5,reqAmount:7575,activeAmount:980,loansPaid:4,loansUnpaid:0},{date:1768406231,reqCount:55,activeCount:23,reqAmount:19817,activeAmount:7585,loansPaid:2,loansUnpaid:2},{date:1768319831,reqCount:49,activeCount:25,reqAmount:13719,activeAmount:5130,loansPaid:0,loansUnpaid:1},{date:1768233431,reqCount:48,activeCount:30,reqAmount:15750,activeAmount:8840,loansPaid:2,loansUnpaid:0},{date:1768147031,reqCount:51,activeCount:33,reqAmount:11955,activeAmount:6400,loansPaid:1,loansUnpaid:0},{date:1768060631,reqCount:40,activeCount:23,reqAmount:11395,activeAmount:5675,loansPaid:0,loansUnpaid:1},{date:1767974231,reqCount:40,activeCount:21,reqAmount:11630,activeAmount:4830,loansPaid:9,loansUnpaid:1},{date:1767887831,reqCount:54,activeCount:24,reqAmount:30153,activeAmount:7850,loansPaid:5,loansUnpaid:2},{date:1767801431,reqCount:57,activeCount:28,reqAmount:25120,activeAmount:10715,loansPaid:3,loansUnpaid:0},{date:1767715031,reqCount:61,activeCount:31,reqAmount:14390,activeAmount:6365,loansPaid:2,loansUnpaid:0},{date:1767628631,reqCount:58,activeCount:33,reqAmount:17598,activeAmount:11290,loansPaid:2,loansUnpaid:2},{date:1767542231,reqCount:50,activeCount:33,reqAmount:13760,activeAmount:8790,loansPaid:2,loansUnpaid:1},{date:1767455831,reqCount:49,activeCount:27,reqAmount:16022,activeAmount:10165,loansPaid:2,loansUnpaid:0},{date:1767369431,reqCount:63,activeCount:34,reqAmount:31530,activeAmount:15435,loansPaid:9,loansUnpaid:1},{date:1767283031,reqCount:43,activeCount:27,reqAmount:15505,activeAmount:6895,loansPaid:5,loansUnpaid:1},{date:1767196631,reqCount:58,activeCount:33,reqAmount:30077,activeAmount:13335,loansPaid:5,loansUnpaid:2},{date:1767110231,reqCount:34,activeCount:15,reqAmount:12743,activeAmount:4684,loansPaid:2,loansUnpaid:0},{date:1767023831,reqCount:0,activeCount:0,reqAmount:0,activeAmount:0,loansPaid:0,loansUnpaid:0},{date:1766937431,reqCount:0,activeCount:0,reqAmount:0,activeAmount:0,loansPaid:0,loansUnpaid:0},{date:1766851031,reqCount:0,activeCount:0,reqAmount:0,activeAmount:0,loansPaid:0,loansUnpaid:0},{date:1766764631,reqCount:0,activeCount:0,reqAmount:0,activeAmount:0,loansPaid:0,loansUnpaid:0},{date:1766678231,reqCount:0,activeCount:0,reqAmount:0,activeAmount:0,loansPaid:0,loansUnpaid:0},{date:1766591831,reqCount:0,activeCount:0,reqAmount:0,activeAmount:0,loansPaid:0,loansUnpaid:0},{date:1766505431,reqCount:0,activeCount:0,reqAmount:0,activeAmount:0,loansPaid:0,loansUnpaid:0},{date:1766419031,reqCount:0,activeCount:0,reqAmount:0,activeAmount:0,loansPaid:0,loansUnpaid:0},{date:1766332631,reqCount:0,activeCount:0,reqAmount:0,activeAmount:0,loansPaid:0,loansUnpaid:0},{date:1766246231,reqCount:0,activeCount:0,reqAmount:0,activeAmount:0,loansPaid:0,loansUnpaid:0},{date:1766159831,reqCount:0,activeCount:0,reqAmount:0,activeAmount:0,loansPaid:0,loansUnpaid:0},{date:1766073431,reqCount:0,activeCount:0,reqAmount:0,activeAmount:0,loansPaid:0,loansUnpaid:0},{date:1765987031,reqCount:0,activeCount:0,reqAmount:0,activeAmount:0,loansPaid:0,loansUnpaid:0}];
    setData(dummy_data)
  }, [])

  return (
    <>
      <header>
        <h1>Loan Data Visualizer</h1>
      </header>
      <main>
        <section id='data'>
          <div id='DataPanels'>
            <DataPanel title={"Amounts"} datadict={[["ReqAmount", 150000, " USD"], ["ActiveAmount", 85000, " USD"], ["30 Day Trend", -5.4, "%"]]} />
            <DataPanel title={"Amounts"} datadict={[["ReqAmount", 150000, " USD"], ["ActiveAmount", 85000, " USD"], ["30 Day Trend", -5.4, "%"]]} />
            <DataPanel title={"Amounts"} datadict={[["ReqAmount", 150000, " USD"], ["ActiveAmount", 85000, " USD"], ["30 Day Trend", -5.4, "%"]]} />
          </div>
          <div id='Graphs'>
            <div className='Graph'>
              <PlotFigure
                options={{
                  width: 500,
                  color: {legend: true},
                  marks: [
                    Plot.ruleY([0]),
                    Plot.lineY(data, {x: d => new Date(d.date * 1000), y: "reqAmount"})
                  ]
                }}
              />
            </div>
            <div className='Graph'>
              <PlotFigure
                options={{
                  width: 500,
                  color: {legend: true},
                  marks: [
                    Plot.ruleY([0]),
                    Plot.lineY(data, {x: d => new Date(d.date * 1000), y: "reqAmount"})
                  ]
                }}
              />
            </div>
            <div className='Graph'>
              <PlotFigure
                options={{
                  width: 500,
                  color: {legend: true},
                  marks: [
                    Plot.ruleY([0]),
                    Plot.lineY(data, {x: d => new Date(d.date * 1000), y: "reqAmount"})
                  ]
                }}
              />
            </div>
            <div className='Graph'>
              <PlotFigure
                options={{
                  width: 500,
                  color: {legend: true},
                  marks: [
                    Plot.ruleY([0]),
                    Plot.lineY(data, {x: d => new Date(d.date * 1000), y: "reqAmount"})
                  ]
                }}
              />
            </div>
            
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
