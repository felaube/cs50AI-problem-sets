import os
from random import randint, choices
import numpy as np
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
    # Initialize variable to store the probability distribution
    distribution = dict.fromkeys(corpus, 0)

    num_links = len(corpus[page])
    num_pages = len(corpus)

    if num_links == 0:
        # In case 'page' has no outgoing links,
        # all pages have equal probability to be chosen
        for link in corpus:
            distribution[link] = 1/num_pages
    else:
        # Add probability to pages linked to by 'page'
        for link in corpus[page]:
            distribution[link] += damping_factor/num_links

        # Add probability to pages chosen at random from all pages in corpus
        for link in corpus:
            distribution[link] += (1 - damping_factor)/num_pages

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize variable to store the number of hits each page received
    hits = dict.fromkeys(corpus, 0)
    pages = list(corpus.keys())

    num_pages = len(pages)

    # Generate first sample at random
    page = pages[randint(0, num_pages - 1)]
    hits[page] += 1

    for i in range(n - 1):
        # Generate a new sample according to the probability distribution
        # calculated on the current page
        distribution = transition_model(corpus, page, damping_factor)
        page = choices(list(distribution.keys()), list(distribution.values()))
        # The function "choices" returns a list.
        # Get the first (and only, in this case) element
        page = page[0]
        hits[page] += 1

    page_rank = dict.fromkeys(hits.keys())
    for page in page_rank:
        page_rank[page] = hits[page]/n

    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Set initial guess as 1/(total number of pages in corpus)
    num_pages = len(corpus)
    page_rank = dict.fromkeys(corpus, 1/num_pages)

    # Get the number of links on each page
    num_links = np.zeros(num_pages)

    for (i, page) in enumerate(corpus):
        num_links[i] = len(corpus[page])

    # A page that has no links at all should be interpreted as
    #  having one link for every page in the corpus (including itself)
    num_links[num_links == 0] = num_pages
    for page in corpus:
        if len(corpus[page]) == 0:
            for link in corpus:
                corpus[page].add(link)

    # Recalculate the PageRanks iteratively until
    # no PageRank value changes by more than 0.001
    # between the current rank values and the new rank values
    current_ranks = np.array(list(page_rank.values()))
    while True:
        # Calculate new rank for each page
        for page_p in page_rank:
            # Find out which pages link to page_p
            index = np.zeros(len(corpus), dtype=bool)
            for i, page_i in enumerate(corpus):
                if page_p in corpus[page_i]:
                    index[i] = True
            page_rank[page_p] = ((1 - damping_factor)/num_pages +
                                 damping_factor *
                                 sum(current_ranks[index]/num_links[index]))

        # Get the new calculated ranks
        new_ranks = np.array(list(page_rank.values()))

        # Check for stopping criteria
        if all(abs(new_ranks - current_ranks) <= 0.001):
            break

        # Update the current ranks if another iteration in needed
        current_ranks = new_ranks

    return page_rank


if __name__ == "__main__":
    main()
