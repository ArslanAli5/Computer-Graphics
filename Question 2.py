#!/usr/bin/env python
# coding: utf-8

# In[30]:


# Q2 (a)




install.packages("rvest")
library(rvest)

### F12 Developer Mode located table html tag -> copy XPath

url <- "https://en.wikipedia.org/wiki/List_of_Singapore_MRT_stations"
mrt_stn <-  url %>%
  read_html() %>%
  html_nodes(xpath='//*[@id="mw-content-text"]/div/table[2]') %>%
  html_table(fill = TRUE)
mrt <- mrt_stn[[1]]
mrt <- mrt[,c(1:2,5,7:8)] 
names(mrt) <- c("Code","Name","Opening","Status","Location")
mrt <- subset(mrt,Code != Name)
mrt <- mrt[2:nrow(mrt),]

mrt$Code <- substr(mrt$Code, 1, 4)
mrt$Code <- iconv(mrt$Code, "ASCII", "UTF-8", sub="")

mrt$Name <- gsub('\\[.\\]',"",mrt$Name)

mrt <- mrt[mrt$Name != 'Reserved Station',]
mrt <- mrt[mrt$Name != 'Punggol Coast',]
mrt <- mrt[mrt$Status != 'TBA',]


#########
# MRT NSL Edgelist
ns_df <- mrt[substr(mrt$Code,1,2) == 'NS',]

sourceList <- ""
targetList <- ""
for (i in 1:nrow(ns_df)-1) {
  sourceList[i] <- ns_df$Name[i]
  targetList[i] <- ns_df$Name[i+1]
}

ns_edgelist <- data.frame(sourceList, targetList, "NSL")
names(ns_edgelist) <- c("source", "target", "network")

# MRT EWL Edgelist
ew_df <- mrt[substr(mrt$Code,1,2) == 'EW',]

sourceList <- ""
targetList <- ""
for (i in 1:nrow(ew_df)-1) {
  sourceList[i] <- ew_df$Name[i]
  targetList[i] <- ew_df$Name[i+1]
}

ew_edgelist <- data.frame(sourceList, targetList, "EWL")
names(ew_edgelist) <- c("source", "target", "network")

# MRT CAL Edgelist
cg_df <- mrt[substr(mrt$Code,1,2) == 'CG',]

sourceList <- ""
targetList <- ""
for (i in 1:nrow(cg_df)-1) {
  sourceList[i] <- cg_df$Name[i]
  targetList[i] <- cg_df$Name[i+1]
}

cg_edgelist <- data.frame(sourceList, targetList, "CAL")
names(cg_edgelist) <- c("source", "target", "network")


# MRT NEL Edgelist
ne_df <- mrt[substr(mrt$Code,1,2) == 'NE',]

sourceList <- ""
targetList <- ""
for (i in 1:nrow(ne_df)-1) {
  sourceList[i] <- ne_df$Name[i]
  targetList[i] <- ne_df$Name[i+1]
}

ne_edgelist <- data.frame(sourceList, targetList, "NEL")
names(ne_edgelist) <- c("source", "target", "network")


# MRT CCL Edgelist
cc_df <- mrt[substr(mrt$Code,1,2) == 'CC',]

sourceList <- ""
targetList <- ""
for (i in 1:nrow(cc_df)-1) {
  sourceList[i] <- cc_df$Name[i]
  targetList[i] <- cc_df$Name[i+1]
}

cc_edgelist <- data.frame(sourceList, targetList, "CCL")
names(cc_edgelist) <- c("source", "target", "network")


# MRT DTL Edgelist
dt_df <- mrt[substr(mrt$Code,1,2) == 'DT',]

sourceList <- ""
targetList <- ""
for (i in 1:nrow(dt_df)-1) {
  sourceList[i] <- dt_df$Name[i]
  targetList[i] <- dt_df$Name[i+1]
}

dt_edgelist <- data.frame(sourceList, targetList, "DTL")
names(dt_edgelist) <- c("source", "target", "network")


mrt_edgelist <- rbind(ns_edgelist,ew_edgelist,cg_edgelist,ne_edgelist,cc_edgelist,dt_edgelist)
mrt_edgelist$target <- as.character(mrt_edgelist$target)
mrt_edgelist$source <- as.character(mrt_edgelist$source)
mrt_edgelist$network <- as.character(mrt_edgelist$network)
mrt_edgelist[nrow(mrt_edgelist)+1,] <- c("Bayfront","Marina Bay","CEL")
mrt_edgelist[nrow(mrt_edgelist)+1,] <- c("Bayfront","Promenade","CCL")
mrt_edgelist[nrow(mrt_edgelist)+1,] <- c("Tanah Merah","Expo","CAL")
mrt_edgelist$type <- "undirected"


mrt_node <- mrt[substr(mrt$Code,1,2) != 'TE',]
names(mrt_node)[2] <- "id"
mrt_node$label <- mrt_node$id

mrt_nodes <- unique(mrt_node)
mrt_nodes <- mrt_nodes[!duplicated(mrt_nodes$id),]
mrt_nodes$Code <- substr(mrt_nodes$Code, 1, 2)

write.csv(mrt_nodes, file="mrt_nodes.csv", row.names=F)


install.packages("igraph")
library(igraph)

# rename for igraph edgelist format
names(mrt_edgelist) <- c("from","to","network","type")
mrt_nodes <- mrt_nodes[c(2,6,1,3,4,5)]

g = graph.data.frame(mrt_edgelist, mrt_nodes, directed=F)

# checking if multiple edges exists in the graph network
any_multiple(g)
which_multiple(g)
# Removing multiple edges to create a simplified graph 
E(g)[38]
E(g)[135]

simple_g <- g
simple_g <- delete_edges(simple_g,c(38,135))
any_multiple(simple_g) 

#### descriptive statistics ####
# list nodes & edges attributes
list.vertex.attributes(simple_g)
list.edge.attributes(simple_g)

# easy access to nodes, edges, and their attributes 
E(simple_g)       # The edges of the graph object
V(simple_g)       # The vertices of the graph object

# Network Size (num of nodes and edges)
summary(simple_g)
# Network Density
graph.density(simple_g,loop=FALSE)
# Greatest distance between any pair of vertices
diameter(simple_g)
# Average Path Length
mean_distance(simple_g, directed=F)
# Length of all paths in the graph
distances(simple_g)


### Generating graph attributes ###
V(simple_g)$degree=degree(simple_g, mode="all")
V(simple_g)$betweenness=betweenness(simple_g,normalized=T)
V(simple_g)$closeness=closeness(simple_g,normalized=T)

V(simple_g)$coreness=coreness(simple_g)
V(simple_g)$eigen=evcent(simple_g)$vector

# Specify graph layout to use
glay = layout_with_lgl(simple_g)
glay = layout_on_sphere(simple_g)

install.packages("plyr")
library(plyr)
# Generate node colors based on edge:network attribute
E(simple_g)$color <- mapvalues(E(simple_g)$network, c("NSL","EWL","CAL","NEL","CCL","DTL","CEL"), c("#D42E12","#009645","#009645","#9900AA","#FA9E0D","#FA9E0D","#005EC4"))
#V(g)$size <- deg*3

# plot degree graph 
plot(simple_g, layout=glay, edge.color=E(simple_g)$color, edge.width=3, edge.curve=1, 
     vertex.label.cex=.7, vertex.color="white", vertex.frame.color="black", 
     vertex.label.font=1.5, vertex.label=V(simple_g)$label, vertex.label.color="grey40",
     vertex.size=V(simple_g)$degree*3.5) 
# show the node(s) that holds the largest degree value
V(simple_g)$name[degree(simple_g)==max(degree(simple_g))]

# plot closeness graph
plot(simple_g, layout=glay, edge.color=E(simple_g)$color, edge.width=3, edge.curve=1, 
     vertex.label.cex=.7, vertex.color="white", vertex.frame.color="black", 
     vertex.label.font=.7, vertex.label=V(simple_g)$label, vertex.label.color="grey40",
     vertex.size=V(simple_g)$closeness*90) 
# show the node(s) that holds the largest closeness value
V(simple_g)$name[closeness(simple_g)==max(closeness(simple_g))]

# plot betweenness graph
plot(simple_g, layout=glay, edge.color=E(simple_g)$color, edge.width=3, edge.curve=1, 
     vertex.label.cex=.7, vertex.color="white", vertex.frame.color="black", 
     vertex.label.font=1, vertex.label=V(simple_g)$label, vertex.label.color="grey40",
     vertex.size=V(simple_g)$betweenness*60) 
# show the node(s) that holds the largest betweenness value
V(simple_g)$name[betweenness(simple_g)==max(betweenness(simple_g))]

# plot eigenvector graph
plot(simple_g, layout=glay, edge.color=E(simple_g)$color, edge.width=3, edge.curve=1, 
     vertex.label.cex=.7, vertex.color="white", vertex.frame.color="black", 
     vertex.label.font=1, vertex.label=V(simple_g)$label, vertex.label.color="grey40",
     vertex.size=V(simple_g)$eigen*20)
# show the node(s) that holds the largest eigenvector value
V(simple_g)$name[which.max(V(simple_g)$eigen)]

attr = data.frame(row.names=V(simple_g)$name,degree=V(simple_g)$degree,
                  coreness=V(simple_g)$coreness,betweenness=V(simple_g)$betweenness,
                  closeness=V(simple_g)$closeness,eigen=V(simple_g)$eigen)


############################################
######### basic statistic analysis #########
#### descriptive ####
table(attr$degree)
table(attr$coreness)
table(attr$betweenness)
table(attr$closeness)
table(attr$eigen)

attr




# In[18]:


## Q2 (b)

import matplotlib.pyplot as plt

price = [2.50, 1.23, 4.02, 3.25, 5.00, 4.40]
sales_per_day = [34, 62, 49, 22, 13, 19]

plt.scatter(price, sales_per_day)
plt.show()


# In[4]:


plt.plot(price, sales_per_day, "o")
plt.show()


# In[8]:


import timeit
import matplotlib.pyplot as plt

price = [2.50, 1.23, 4.02, 3.25, 5.00, 4.40]
sales_per_day = [34, 62, 49, 22, 13, 19]

print(
    "plt.scatter()",
    timeit.timeit(
        "plt.scatter(price, sales_per_day)",
        number=1000,
        globals=globals(),
    ),
)
print(
    "plt.plot()",
    timeit.timeit(
        "plt.plot(price, sales_per_day, 'o')",
        number=1000,
        globals=globals(),
    ),
)


# In[19]:


# Q2 (c)

import pandas as pd  
  
# assign data of lists.  
data = {'Name': ['Tom', 'Joseph', 'Krish', 'John'], 'Age': [20, 21, 19, 18]}  
  
# Create DataFrame  
df = pd.DataFrame(data)  
  
# Print the output.  
print(df)  


# In[17]:


# Q2 (d)

# This code for printing shortest path between
# two vertices of unweighted graph

# utility function to form edge between two vertices
# source and dest
def add_edge(adj, src, dest):

	adj[src].append(dest);
	adj[dest].append(src);

# a modified version of BFS that stores predecessor
# of each vertex in array p
# and its distance from source in array d
def BFS(adj, src, dest, v, pred, dist):

	# a queue to maintain queue of vertices whose
	# adjacency list is to be scanned as per normal
	# DFS algorithm
	queue = []

	# boolean array visited[] which stores the
	# information whether ith vertex is reached
	# at least once in the Breadth first search
	visited = [False for i in range(v)];

	# initially all vertices are unvisited
	# so v[i] for all i is false
	# and as no path is yet constructed
	# dist[i] for all i set to infinity
	for i in range(v):

		dist[i] = 1000000
		pred[i] = -1;
	
	# now source is first to be visited and
	# distance from source to itself should be 0
	visited[src] = True;
	dist[src] = 0;
	queue.append(src);

	# standard BFS algorithm
	while (len(queue) != 0):
		u = queue[0];
		queue.pop(0);
		for i in range(len(adj[u])):
		
			if (visited[adj[u][i]] == False):
				visited[adj[u][i]] = True;
				dist[adj[u][i]] = dist[u] + 1;
				pred[adj[u][i]] = u;
				queue.append(adj[u][i]);

				# We stop BFS when we find
				# destination.
				if (adj[u][i] == dest):
					return True;

	return False;

# utility function to print the shortest distance
# between source vertex and destination vertex
def printShortestDistance(adj, s, dest, v):
	
	# predecessor[i] array stores predecessor of
	# i and distance array stores distance of i
	# from s
	pred=[0 for i in range(v)]
	dist=[0 for i in range(v)];

	if (BFS(adj, s, dest, v, pred, dist) == False):
		print("Given source and destination are not connected")

	# vector path stores the shortest path
	path = []
	crawl = dest;
	path.append(crawl);
	
	while (pred[crawl] != -1):
		path.append(pred[crawl]);
		crawl = pred[crawl];
	

	# distance from source is in distance array
	print("Shortest path length is : " + str(dist[dest]), end = '')

	# printing path from source to destination
	print("\nPath is : : ")
	
	for i in range(len(path)-1, -1, -1):
		print(path[i], end=' ')
		
# Driver program to test above functions
if __name__=='__main__':
	
	# no. of vertices
	v = 8;

	# array of vectors is used to store the graph
	# in the form of an adjacency list
	adj = [[] for i in range(v)];

	# Creating graph given in the above diagram.
	# add_edge function takes adjacency list, source
	# and destination vertex as argument and forms
	# an edge between them.
	add_edge(adj, 0, 1);
	add_edge(adj, 0, 3);
	add_edge(adj, 1, 2);
	add_edge(adj, 3, 4);
	add_edge(adj, 3, 7);
	add_edge(adj, 4, 5);
	add_edge(adj, 4, 6);
	add_edge(adj, 4, 7);
	add_edge(adj, 5, 6);
	add_edge(adj, 6, 7);
	source = 0
	dest = 7;
	printShortestDistance(adj, source, dest, v);

	# This code is contributed by rutvik_56


# In[27]:


# DFS memoization

adjMatrix=[]

mp=dict()
 
# Function to implement DFS Traversal

def DFSUtility(node, stops, dst, cities):

    # Base Case

    if (node == dst):

        return 0
 

    if (stops < 0) :

        return 1e9

     
 

    key=(node, stops)
 

    # Find value with key in a map

    if key in mp:

        return mp[key]

     
 

    ans = 1e9
 

    # Traverse adjacency matrix of

    # source node

    for neighbour in range(cities):

        weight = adjMatrix[node][neighbour]
 

        if (weight > 0) :
 

            # Recursive DFS call for

            # child node

            minVal = DFSUtility(neighbour, stops - 1, dst, cities)
 

            if (minVal + weight > 0):

                ans = min(ans, minVal + weight)

         

     
 

    mp[key] = ans
 

    # Return ans

    return ans
# Function to find the cheapest price
# from given source to destination

def findCheapestPrice(cities, flights, src, dst, stops):

    global adjMatrix

    # Resize Adjacency Matrix

    adjMatrix=[[0]*(cities + 1) for _ in range(cities + 1)]
 

    # Traverse flight[][]

    for item in flights:

        # Create Adjacency Matrix

        adjMatrix[item[0]][item[1]] = item[2]

     
 

    # DFS Call to find shortest path

    ans = DFSUtility(src, stops, dst, cities)
 

    # Return the cost

    return -1 if ans >= 1e9 else int(ans)
     
 


# In[ ]:




