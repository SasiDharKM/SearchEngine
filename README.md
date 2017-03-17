# SearchEngine

This Project is for developing a very basic module of a Search Engine i.e. a hack which takes in a query and returns a page indexed in 
its database depending on the rank of the page.

This Project involes 3 general Steps
## |Finding the data
       It involves finding all the links available in the web using a seed page. The links are found are found by a 
       depth-first search routine and is stored for indexing.
## |Building an Index
       Now that the Raw collection of links is available to us, the data has to indexed in a efficient manner 
       to aid in the process of retrieval whe a query comes up.I have used the Hash table data structure for this 
       purpose as the searching for information in it is highly time efficient.
       
## |Ranking Pages       
