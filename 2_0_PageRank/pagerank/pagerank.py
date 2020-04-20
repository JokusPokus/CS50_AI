import os
import random
import re
import sys
from copy import deepcopy

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
    prob_dist = dict()

    # If page doesn't link to any other site
    if not corpus[page]:
        prob = 1 / len(corpus)
        for site in corpus:
            prob_dist[site] = prob

        return prob_dist

    for site in corpus:
        # Choose site in corpus at random
        rand = (1 - damping_factor) / len(corpus)

        # Choose link from page at random
        linked = damping_factor * (1 / len(corpus[page])) if site in corpus[page] else 0

        prob_dist[site] = rand + linked

    return prob_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    counts = dict()
    current_page = random.choice([*corpus])
    counts[current_page] = 1
    for i in range(n-1):
        # Weights for choosing next link based on current page's transition function
        transition = transition_model(corpus, current_page, damping_factor)
        sites = [site for site in corpus]
        weights = [transition[site] for site in sites]
        current_page = random.choices(sites, weights)[0]
        counts[current_page] = counts.get(current_page, 0) + 1

    # Compute and return relative frequencies
    pagerank_s = dict()
    for site in corpus:
        pagerank_s[site] = counts.get(site, 0) / n
    return pagerank_s


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank_i = dict()

    # Initial probability for picking any site
    prob = 1 / len(corpus)
    for site in corpus:
        pagerank_i[site] = prob

    # Damping part of the formula is constant:
    damp = (1 - damping_factor) / len(corpus)

    converged = False

    # Repeat estimation until convergence
    while not converged:
        before = deepcopy(pagerank_i)

        # Consider pagerank component through pages that do not link to any other sites
        non_linking_sites = sum([pagerank_i[page] / len(corpus) if not corpus[page] else 0 for page in corpus])

        for site in pagerank_i:
            new_value = non_linking_sites
            # Add component for each page that links to the site
            new_value += sum([before[page] / len(corpus[page]) if (site in corpus[page]) else 0 for page in corpus])

            # Update pagerank according to formula
            pagerank_i[site] = damp + damping_factor * new_value

        # Assume convergence and try to negate it
        converged = True
        for site in pagerank_i:
            if abs(pagerank_i[site] - before[site]) > 0.001:
                converged = False
                break

    return pagerank_i


if __name__ == "__main__":
    main()
