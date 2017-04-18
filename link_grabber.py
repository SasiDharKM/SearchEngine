#!/usr/bin/env python2.7


def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except ImportError:
        return ""

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def union(p, q):
    for e in q:
        if e not in p:
            p.append(e)
   
def get_all_links(page):
    links = []
    while True:
        url,endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links    


def record_user_click(index, keyword, url):
    urls = lookup(index, keyword)
    if urls:
        for i in urls:
            if i[0] == url:
                i[1] = i[1]+1

  
def add_to_index(index, keyword, url):
    # format of index: [[keyword, [[url, count], [url, count],..]],...]
    if keyword in index:
    	index[keyword].append(url)
    else:
    	# key not found , add to index
    	index[keyword] =[url]

def add_page_to_index(index, url, content):
    words = content.split( )
    for i in words:
        add_to_index(index, word, url)


# web crawler for crawl-restriction by max_depth of search
#def crawl_web(seed, max_depth):
#    tocrawl=[seed]
#    crawled=[]
#    next_depth=[]
#    depth=0
#    index={}
#    while tocrawl and depth <= max_depth:
#        page=tocrawl.pop()
#        if page not in crawled:
#            content = get_page(page)
#           add_page_to_index(index,page,content)
#            union(next_depth,get_all_links(content))
#            crawled.append(page)
#       if not tocrawl:
#            tocrawl,next_depth = next_depth,tocrawl
#            depth = depth+1
#    return index 

def crawl_web(seed, max_depth):
    tocrawl=[seed]
    crawled=[]
    index={}
    graph={} # <url>:[list of pages it links to]
    while tocrawl and depth <= max_depth:
        page=tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index,page,content)
            outlinks=get_all_links(content)
            graph[page] = outlinks
            union(tocrawl,outlinks)
            crawled.append(page)
    return index,graph

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    return None

def is_reciprocal_link(graph, source, destination, k):
	if k == 0:
		if destination == source:
			return True
		return False
	if source in graph[destination]:
		return True
	for node in graph[destination]:
		if is_reciprocal_link(graph, source, node, k-1):
			return True
	return False

def compute_ranks(graph, k):
	d = 0.8  #damping factor for pagerank
	numloops = 10 # determines the accuracy of rank

	ranks = {}
	npages = len(graph)
	for page in graph:
		ranks[page] = 1.0/npages

	for i in range(0, numloops):
		newranks = {}
		for page in graph:
			newrank = (1-d)/npages
			for node in graph:
				if page in graph[node]: # node links to page
				  	if not is_reciprocal_link(graph, node, page, k): 
				  		newrank = newrank + d*(ranks[node] / len(graph[node])) #algorithm for page rank

			newranks[page] = newrank
		ranks = newranks

	return ranks

def best_res(index, ranks, keyword):
	pages = lookup(index, keyword)
	if not pages:
		return None
	best_page = pages[0]
	for res in pages:
		if ranks[res] > ranks[best_page]:
			best_page = res
	return best_page

def quicksort_pages(pages, ranks):
	#implementing the quicksort algorithm for ordering the search results efficiently

	if not pages or len(pages) <= 1:
		return pages
	else:
		pivot = ranks[pages[0]] # assigning pivot as the pivot element(usually random but doesn't matter) 
		worse = []
		better = []
		for page in pages[1:]:
			if ranks[page] <= pivot:
				worse.append(page)
			else:
				better.append(page)

		return quicksort_pages(better, ranks) + [pages[0]] + quicksort_pages(worse, ranks)


def ordered_search(index, ranks, keyword):
	# the method for returning the ordered search results
	pages = lookup(index, keyword)
	return quicksort_pages(pages, ranks)
