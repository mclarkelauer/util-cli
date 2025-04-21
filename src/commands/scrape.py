import click
import logging

# init logging
logger = logging.getLogger(__name__)

import requests
from bs4 import BeautifulSoup
from collections import deque


def fetch_links(url):
    """
    Fetches all the links (href attributes of <a> tags) from a given webpage URL.

    Args:
        url (str): The URL of the webpage to scrape.

    Returns:
        list: A list of strings, where each string is a link found on the page.
              Returns an empty list if the request fails or no links are found.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        links = []
        for link in soup.find_all('a', href=True):
            links.append(link['href'])
        return links
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching URL: {e}")
        raise e
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise e


class Scraper:
    def __init__(self, url, depth=0, stay_in_domain=True):
        self.start_url = url
        self.depth = depth
        self.work_queue = deque()
        self.completed = {}
        self.stay_in_domain = stay_in_domain

        self.work_queue.append(self.start_url)

    def pop_next_url(self):
        url = self.work_queue.popleft()
        logger.debug(f"deque - {url}")
        return url

    def check_if_done(self, url):
        if url in self.completed:
            logger.debug(f"already completed: {url}")
            return True
        return False

    def push_next_url(self, url):
        if url not in self.work_queue and url not in self.completed:
            self.work_queue.append(url)

    def run(self):
        while len(self.work_queue) > 0:
            url = self.pop_next_url()
            if self.check_if_done(url):
                logger.debug(f"Skipping url, already compelted: {url}")
            else:
                try: 
                    links = fetch_links(url)
                except Exception as e:
                    logger.error(f"There was an error fetching {url} : {e}")
                    self.completed[url] = False
                    continue
                self.completed[url] = True


                for link in links:
                    if link != '#' and "arlingtonsoccerclub" in link:
                        self.push_next_url(link)
        
@click.command()
@click.option('-u', '--url', 'url')
@click.option('-d', '--depth', help='Depth of Crawl, 0 for unbounded search', default=0, show_default=True)  
@click.pass_context
def scrape(ctx, url, depth):
    logger.debug(f"Options: {url}, {depth}")
    click.echo(f"Fetching {url} and searching for deadlinks")
    scraper = Scraper(url=url, depth=depth)
    scraper.run()


