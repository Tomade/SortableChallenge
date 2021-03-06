# SortableChallenge.py


## Introduction
This code addresses the programming challenge issued by Sortable (http://sortable.com/challenge/). It can be run
under either Python 2.x or 3.x. It assumes availability of the files "listings.txt" and "products.txt" in the same
location it runs from. To execute, issue the command "python
SortableChallenge.py" from a shell, or "chmod +x SortableChallenge.py; ./SortableChallenge.py".

## Algorithm overview:
Product and listing files are read into memory and allocated into lists of standard Python dictionaries, using
the standard json module. The resulting lists are then sorted by manufacturer + product name and processed ("merged")
together as follows.

The lists are scanned linearly "side by side", iterating over each product and keeping a numeric index into the 
listings table, initialized to point to the first one. For each product, we scan the listings until matching the 
product manufacturer, and then looking for a match on product name. For each positive match, we store the relevant 
data in a result list for later output at exit.

The algorithm relies on the sorting steps executed earlier to recognize when it is time to move to the next product,
while preserving the current position in the listings table. It ends once we have exhausted the list of products, or
we run out of product listings to examine. Execution time grows linearly in O(n) fashion where n is the number of
product listings.

Matches are detected using a simple substring regex search on word boundaries. This appears to yield rather accurate 
results given the nature of the data being processed and the preparatory sorting steps ("Canon" will match "Canon Canada",
"Agfa" will match "AgfaPhoto" etc), but may fail to recognize product matches where their names are formulated with 
missing spaces or other separators ("110 IS" won't match "110IS").  Further improvements to this logic should be feasible.
<br>

-- <b>Danilo Fiorenzano - June 15, 2016</b>
