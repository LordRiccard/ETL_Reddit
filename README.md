# ETL_Reddit

## Goals
* Provide a template on how to ``extract`` posts from reddit
* Show possible ways to increase the data's value using ``transform``
* Implement a way to ``load`` the data collected inside a database
## Structure
`````mermaid
flowchart LR
    a((Reddit)) --> |extract| b[extracted.csv] 
    b --> |transform| c[transformed.csv]
    c --> |load| d[(MySQL)]
`````
* ``r/explainlikeimfive`` was select for this implementation since it is pretty active and has many posts with text only
  * The topics collect were from ```Hot``` section
* ``MySQL`` was chosen as database, but it could be changed due to the nature of keywords
  * ``Neo4j`` could be a good alternative
* Yake was used to extract keywords
  * Sentiment analysis could be a future implementation focus (with a different subreddit too)
## Conclusion
* The project did achieve its goals and has shown room for improvement and expansion
* In the future, there could be projects that dive deep into the collected data, through AI tools and an expanded scope of subreddits