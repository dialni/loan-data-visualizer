export default function PrivacyPolicy() {
  return (
    <>
      <h1>Privacy Policy</h1>
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
    </>
  )
}