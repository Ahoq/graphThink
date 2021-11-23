# GraphThink

A webapp that allows users to store insights and keywords as nodes and relationships in a Neo4j database. Users can also visualize the stored insights 
as nodes and relationships using vis.js. Moreover, users are able to run different graph algorithms on the stored data.

![webapp](https://github.com/ahoq/grapThink/blob/master/img/webapp.png?raw=true)

Registration/Login: The Flask app uses the neo4j database to register new users and store their info. Then subsequent queries are made to the neo4j database when the user is trying to login. All username and passwords are saved as nodes.

![login](https://github.com/ahoq/grapThink/blob/master/img/login.png?raw=true)

Once logged in, the user can now share/publish new insights about any specific topic. The user needs to provide a title, any tags associated with the insight, and a short description of the insight. All of these are stored as properties of the specific ‘insight’ node.

![publish](https://github.com/ahoq/grapThink/blob/master/img/publish.png?raw=true)

Click the ‘Publish’ button and your ‘insight’ will be published and stored in the neo4j database as a node along with all its associated properties. 

![success](https://github.com/ahoq/grapThink/blob/master/img/success.png?raw=true)

Now you can select ‘Insights' item from the right hand menu bar and you will be able to view the insight.

![insight](https://github.com/ahoq/grapThink/blob/master/img/insight.png?raw=true)

Also, you can visualize different nodes with different orientations by clicking on the ‘Plots’ page. The Flask app is querying the data (nodes, relationships, and properties) based on your filters from the neo4j database and then using the vis.js library to visualize the data as graphs.

![viz](https://github.com/ahoq/grapThink/blob/master/img/viz.png?raw=true)

Lastly, you can run different graph algorithms by moving to the ‘Algo’ page. Based on the your selection, the app will send a request to the neo4j database to run a specific path finding, centrality, or community detection algorithm. Once the algorithm executes, the webapp will retrieve the results and display them on the page.

![algo](https://github.com/ahoq/grapThink/blob/master/img/algo.png?raw=true)



