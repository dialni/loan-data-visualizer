# Loan Data Visualizer (for Reddit)
On online forums and social media, such as Facebook or Reddit, there exists communities that facillitate private loans online. These loans might be in the range of $5 to several thousands of dollars, and are done outside any traditional institutions, such as banks or credit unions.

This is a project that aims to visualize such ["peer-to-peer lending"](https://en.wikipedia.org/wiki/Peer-to-peer_lending) communities, with a focus on Reddit in particular.

These "peer-to-peer lending" forums deal outside of any traditional institutions, and therefore all posts and transactions are public in lieu of a standard credit rating. As such, we can see the live market activity and produce some statistics for a React dashboard.

This tool was developed for educational purposes, as a side-project to test various technologies, and should not be involved in any decisions, finanical or otherwise.

# How to run
1. Request access to [Reddit Data API](https://support.reddithelp.com/hc/en-us/requests/new?ticket_form_id=14868593862164) and add the data to your environment variables
2. Install the required dependencies (This is easily done with Docker using the `deploy.sh` script)
3. If not done already, run using `./deploy.sh` or setup your own infrastructure manually.

# I don't have access to Reddit Data API!
Due to the [Reddit Data API rules](https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki), it is not possible to have this data hosted on GitHub directly. Instead, an online tool will be available soon<sup>tm</sup> and a link will be posted here.

# FAQ
**Q: Will more features be added in the future?**

**A:** Probably not, as this was a fun side-project to try out some cool technologies.

**Q: These loans seem awesome! Should I try to participate?**

**A:** Peer-to-peer lending have massive risks associated with them, and most countries/regions have laws against these things. Contact a legal professional and do your own research.

# License
This project is licensed under the GPLv3 license. More details are in the `LICENSE.md` file.