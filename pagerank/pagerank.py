import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    result = {}

    # probability to choose a random link within the page: 
    if len(corpus[page]) == 0:
        surf_choice_prob = damping_factor/len(corpus.keys())
    else:
        surf_choice_prob = damping_factor/len(corpus[page])  

    # probability to choose a random page:
    rand_choice_prob = (1 - damping_factor)/len(corpus.keys())

    # update the result:
    for page_name in corpus.keys():
        if page_name in corpus[page]:
            result[page_name] = surf_choice_prob + rand_choice_prob
        else:
            result[page_name] = rand_choice_prob
            
    return result
    # raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # initiate at random:
    page = random.choice(list(corpus.keys()))

    # get rank:
    rank = transition_model(corpus,page,damping_factor)

    sample = []

    # initiate new sample:
    for i in range(n):
        next_page = random.choices(list(rank.keys()),list(rank.values()),k=1)
        next_page = next_page[0]

        # get new rank
        rank = transition_model(corpus,next_page,damping_factor)
        sample.append(next_page)

    # calculate rank from sample:
    final_rank = {x : sample.count(x)/len(sample) for x in sample}

    return final_rank
        
    # raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Iniate page rank equal 1/N:
    num_pages = len(corpus)
    initial_rank = 1 / num_pages
    random_choice_prob = (1- damping_factor)/num_pages

    page_ranks = {page_name:initial_rank for page_name in corpus.keys()}
    new_ranks = {page_name:None for page_name in corpus.keys()}
    
    max_rank_change = 1.0

    # Iterate until no rank change > 0.001
    while max_rank_change > 0.001:
        max_rank_change = 0
        for page_name in corpus.keys():
            surf_choice_prob = 0
            for other_page in corpus:
                # if page has no links, choose any page randomly
                if len(corpus[other_page]) == 0:
                    surf_choice_prob += page_ranks[other_page] + initial_rank
                # if page has links to page_name:
                elif page_name in corpus[other_page]:
                    surf_choice_prob += page_ranks[other_page]/len(corpus[other_page])
            new_rank = random_choice_prob + surf_choice_prob * damping_factor
            new_ranks[page_name] = new_rank

        # normalize rank:
        norm_factor = sum(new_ranks.values())
        new_ranks = {page: (rank / norm_factor) for page, rank in new_ranks.items()}

        # Keep track of rank changes:
        for page_name in corpus.keys():
            rank_change = abs(page_ranks[page_name] - new_ranks[page_name])
            if rank_change > max_rank_change:
                max_rank_change = rank_change

        page_ranks = new_ranks

    

    return page_ranks
    # raise NotImplementedError


if __name__ == "__main__":
    main()
