import { useEffect, useLayoutEffect, useState } from "react";
import * as Plot from "@observablehq/plot";
import './css/Dashboard.css'
import DataPanel from "../../components/DataPanels/DataPanel.jsx";
import PlotFigure from "../../components/PlotFigure.jsx";

export default function Dashboard() {
  const [data, setData] = useState([]);
  const l = data.map((d) => (d)).sort(function (x, y) { return x.date - y.date }) // Guarantees list has been sorted

  // For actual production use
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

  // Function based off this StackOverflow answer: https://stackoverflow.com/a/70729520
  function getScreenWidth() {
    const [size, setSize] = useState(600);
    useLayoutEffect(() => {
      function updateSize() {
        setSize(window.innerWidth);
      }
      window.addEventListener('resize', updateSize);
      updateSize();
      return () => window.removeEventListener('resize', updateSize);
    }, []);
    return size;
  }

  // Data aggregation functions for DataPanels
  function calcSum(key) {
    let result = 0
    if (l.length === 0) {
      return 0;
    }

    for (let i = 7; i < 14; i++) {
      result += l[i][key]
    }
    return result;
  }

  function calcAvg(key) {
    if (data.length === 0) {
      return 0;
    }

    let result = 0
    for (let i = 7; i < 14; i++) {
      result += l[i][key]
    }
    return Number.parseFloat(result / 7).toFixed(2)
  }

  function calcTrend(key) {
    if (l.length === 0) {
      return 0;
    }

    let pastWeekSum = 0;
    let thisWeekSum = 0;

    for (let i = 0; i < 7; i++) {
      pastWeekSum += l[i][key]
      thisWeekSum += l[i + 7][key]
    }

    // This works for both total and average
    return Number.parseFloat((thisWeekSum - pastWeekSum) / pastWeekSum * 100).toFixed(2)
  }

  function calcDefaultRate(approvedKey, defaultKey) {
    if (l.length === 0) {
      return 0;
    }
    let defaults = 0
    let approved = 0

    for (let i = 7; i < 14; i++) {
      defaults += l[i][defaultKey]
      approved += l[i][approvedKey]
    }

    return Number.parseFloat(defaults / approved).toFixed(4)
  }

  function calcDefaultRateTrend(approvedKey, defaultKey) {
    if (l.length === 0) {
      return 0;
    }
    let defaults = 0
    let approved = 0

    for (let i = 0; i < 7; i++) {
      defaults += l[i][defaultKey]
      approved += l[i][approvedKey]
    }
    const thisWeekDefault = calcDefaultRate(approvedKey, defaultKey)
    const pastWeekDefault = Number.parseFloat(defaults / approved).toFixed(4)

    return Number.parseFloat((thisWeekDefault - pastWeekDefault) / pastWeekDefault * 100).toFixed(2)
  }

  return (
    <>
      <section className='TitleSection'>
        <h1>Loan Data Dashboard</h1>
        <h3>Summary of Past 7 Days vs. Previous Period</h3>
      </section>
      <section id='DataPanelSection'>
        <div>
          <DataPanel
            row1={{
              'title': 'Total loans requested',
              'val': calcSum('reqCount'),
              'valu': '',
              'tval': calcTrend('reqCount'),
              'tvalc': 'green'
            }}
            row2={{
              'title': 'Total amount requested',
              'val': calcSum('reqAmount'),
              'valu': 'USD',
              'tval': calcTrend('reqAmount'),
              'tvalc': 'green'
            }} />
        </div>
        <div>
          <DataPanel
            row1={{
              'title': 'Total loans approved',
              'val': calcSum('activeCount'),
              'valu': '',
              'tval': calcTrend('activeCount'),
              'tvalc': 'green'
            }}
            row2={{
              'title': 'Total amount approved',
              'val': calcSum('activeAmount'),
              'valu': 'USD',
              'tval': calcTrend('activeAmount'),
              'tvalc': 'green'
            }} />
        </div>
        <div>
          <DataPanel row1={{
            'title': 'Loans requested daily',
            'val': calcAvg('reqCount'),
            'valu': '',
            'tval': calcTrend('reqCount'),
            'tvalc': 'green'
          }}
            row2={{
              'title': 'Loans approved daily',
              'val': calcAvg('activeCount'),
              'valu': '',
              'tval': calcTrend('activeCount'),
              'tvalc': 'green'
            }} />
        </div>
        <div>
          <DataPanel
            row1={{
              'title': 'Default rate',
              'val': calcDefaultRate('activeCount',
                'loansUnpaid'),
              'valu': '%',
              'tval': calcDefaultRateTrend('activeCount', 'loansUnpaid'),
              'tvalc': 'red'
            }}
            row2={{
              'title': 'Total loans repaid',
              'val': calcSum('loansPaid'),
              'valu': '',
              'tval': calcTrend('loansPaid'),
              'tvalc': 'green'
            }} />
        </div>
      </section>
      <section id='GraphSection'>
        <div>
          <PlotFigure
            options={{
              width: Math.min(Math.max(getScreenWidth() - 300, 1411), 1530), // Magic number range for plot X-axis datetime format
              height: 450,
              marks: [
                Plot.ruleY([0]),
                Plot.lineY(data, { x: d => new Date(d.date * 1000), y: "reqAmount", stroke: 'blue' }),
                Plot.lineY(data, { x: d => new Date(d.date * 1000), y: "activeAmount", stroke: 'orange' })
              ]
            }}
          />
        </div>
        <h6>Daily Market Graph in USD (14-days, blue = loan amount requested, orange = loan amount approved)</h6>
        <p style={{ fontSize: 12 }}>This is purely an educational tool in development, and should not be used for anything.</p>
      </section>
    </>
  )
}