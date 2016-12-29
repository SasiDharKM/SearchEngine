
def get_page(url):
    try:
        import urlib
        return urlib.urlopen(url).read()
    except:
        return ''
    
def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link==-1:
        return None,0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)
            
def get_all_links(page):
    links=[]
    while True:
        url,endpos =get_next_target(page)
        if url:
            links.append(url)
            page=page[endpos:]
        else:
            break
    return links    

index=[]
def add_to_index(index, keyword, url):
    for i in index:
        if i[0]==keyword:
            i[1].append(url)
            return
    index.append([keyword,[url]])

def add_page_to_index(index, url, content):
    words = content.split( )
    for i in words:
        add_to_index(index, word, url)
        
def crawl_web(seed, max_depth):
    tocrawl=[seed]
    crawled=[]
    next_depth=[]
    depth=0
    index=[]
    while tocrawl and depth <= max_depth:
        page=tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index,page,content)
            union(next_depth,get_all_links(content))
            crawled.append(page)
        if not tocrawl:
            tocrawl,next_depth = next_depth,tocrawl
            depth = depth+1
    return crawled

def lookup(index, keyword):
    for i in index:
        if i[0]==keyword:
            return entry[1]
    return []
