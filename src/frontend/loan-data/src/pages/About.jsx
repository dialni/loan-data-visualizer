export default function About() {
  return (
    <>
      <h1>What is Loan Data Visualizer?</h1>
      <p>This is a project that aims to visualize the online activity of <a href="https://en.wikipedia.org/wiki/Peer-to-peer_lending" target="_blank">"peer-to-peer lending"</a> on public forums. Using Python, Postgres, and various libraries in Docker containers.</p>
      <p>These "peer-to-peer lending" forums deal outside of any traditional institutions, and therefore all posts and transactions are public in lieu of a standard credit rating. As such, we can see the live market activity and produce some statistics.</p>
      <p>The source code is available on <a href="https://github.com/dialni/loan-data-visualizer" target='_blank'>GitHub</a>.</p>
      <p>This tool was developed as a side-project for educational purposes to test various technologies, and should not be involved in any decisions, finanical or otherwise.</p>
    </>
  )
}