"""Web scraping commands with async support."""
import asyncio
from collections import deque
from urllib.parse import urljoin, urlparse
import asyncclick as click
import httpx
from bs4 import BeautifulSoup
from rich.console import Console
from rich.progress import Progress, TaskID
from rich.table import Table
from util.logging import logger

console = Console()

async def fetch_links(url: str, client: httpx.AsyncClient) -> list[str]:
    """
    Fetches all the links (href attributes of <a> tags) from a given webpage URL asynchronously.

    Args:
        url (str): The URL of the webpage to scrape.
        client (httpx.AsyncClient): The HTTP client to use.

    Returns:
        list: A list of strings, where each string is a link found on the page.
              Returns an empty list if the request fails or no links are found.
    """
    try:
        response = await client.get(url, timeout=30.0)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "html.parser")
        links = []
        
        for link_tag in soup.find_all("a", href=True):
            href = link_tag["href"]
            # Convert relative URLs to absolute URLs
            absolute_url = urljoin(url, href)
            links.append(absolute_url)
            
        logger.debug(f"Found {len(links)} links on {url}")
        return links
        
    except httpx.RequestError as e:
        logger.error(f"Request error fetching {url}: {e}")
        raise
    except Exception as e:
        logger.error(f"Error parsing {url}: {e}")
        raise


class AsyncScraper:
    """Async web scraper with breadth-first crawling."""
    
    def __init__(self, start_url: str, max_depth: int = 0, stay_in_domain: bool = True, max_concurrent: int = 5):
        self.start_url = start_url
        self.max_depth = max_depth
        self.stay_in_domain = stay_in_domain
        self.max_concurrent = max_concurrent
        
        # Parse the starting domain
        self.start_domain = urlparse(start_url).netloc
        
        # Work tracking
        self.work_queue = deque()
        self.completed = {}  # url -> success status
        self.failed_urls = []
        
        # Add starting URL
        self.work_queue.append((self.start_url, 0))

    def should_process_url(self, url: str) -> bool:
        """Check if URL should be processed based on domain restrictions."""
        if not self.stay_in_domain:
            return True
        
        parsed_url = urlparse(url)
        return parsed_url.netloc == self.start_domain or parsed_url.netloc == ""

    async def process_url(self, client: httpx.AsyncClient, url: str, depth: int) -> tuple[str, bool, list[str]]:
        """Process a single URL and return its links."""
        if url in self.completed:
            logger.debug(f"Already processed: {url}")
            return url, True, []
        
        if self.max_depth > 0 and depth >= self.max_depth:
            logger.debug(f"Max depth reached for: {url}")
            return url, True, []
        
        try:
            links = await fetch_links(url, client)
            self.completed[url] = True
            
            # Filter links based on domain restrictions
            if self.stay_in_domain:
                valid_links = [link for link in links if self.should_process_url(link)]
                logger.debug(f"Filtered {len(links)} -> {len(valid_links)} links for domain {self.start_domain}")
                return url, True, valid_links
            else:
                return url, True, links
                
        except Exception as e:
            logger.error(f"Failed to process {url}: {e}")
            self.completed[url] = False
            self.failed_urls.append(url)
            return url, False, []

    async def run(self):
        """Run the async scraper."""
        console.print(f"[bold green]🕷️  Starting async scrape of {self.start_url}[/bold green]")
        console.print(f"Max depth: {self.max_depth if self.max_depth > 0 else 'unlimited'}")
        console.print(f"Stay in domain: {self.stay_in_domain}")
        console.print(f"Max concurrent requests: {self.max_concurrent}")
        console.print("-" * 60)
        
        timeout = httpx.Timeout(30.0, connect=10.0)
        
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            with Progress() as progress:
                task = progress.add_task("[cyan]Scraping...", total=None)
                
                while self.work_queue:
                    # Get batch of URLs to process
                    current_batch = []
                    for _ in range(min(self.max_concurrent, len(self.work_queue))):
                        if self.work_queue:
                            current_batch.append(self.work_queue.popleft())
                    
                    if not current_batch:
                        break
                    
                    # Process batch concurrently
                    tasks = [
                        self.process_url(client, url, depth) 
                        for url, depth in current_batch
                    ]
                    
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    
                    # Process results and add new URLs to queue
                    for result in results:
                        if isinstance(result, Exception):
                            logger.error(f"Task failed: {result}")
                            continue
                            
                        url, success, new_links = result
                        
                        if success and new_links:
                            # Add new URLs to queue with incremented depth
                            current_depth = next((depth for u, depth in current_batch if u == url), 0)
                            for link in new_links:
                                if (link not in self.completed and 
                                    not any(link == queued_url for queued_url, _ in self.work_queue) and
                                    link != "#"):
                                    self.work_queue.append((link, current_depth + 1))
                    
                    progress.update(task, completed=len(self.completed))
        
        # Display results
        await self.display_results()

    async def display_results(self):
        """Display scraping results."""
        console.print(f"\\n[bold green]✅ Scraping completed![/bold green]")
        
        successful = sum(1 for success in self.completed.values() if success)
        failed = len(self.failed_urls)
        
        # Summary table
        table = Table(title="Scraping Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Count", style="green")
        
        table.add_row("Total URLs processed", str(len(self.completed)))
        table.add_row("Successful", str(successful))
        table.add_row("Failed", str(failed))
        
        console.print(table)
        
        # Show failed URLs if any
        if self.failed_urls:
            console.print(f"\\n[red]❌ Failed URLs ({len(self.failed_urls)}):[/red]")
            for url in self.failed_urls[:10]:  # Show first 10
                console.print(f"  • {url}")
            if len(self.failed_urls) > 10:
                console.print(f"  ... and {len(self.failed_urls) - 10} more")


@click.command()
@click.option("-u", "--url", required=True, help="Starting URL to scrape")
@click.option(
    "-d", "--depth", 
    default=1, 
    show_default=True,
    help="Maximum crawl depth (0 for unlimited)"
)
@click.option(
    "--stay-in-domain/--allow-external",
    default=True,
    help="Whether to stay within the starting domain"
)
@click.option(
    "--max-concurrent",
    default=5,
    show_default=True,
    help="Maximum concurrent requests"
)
@click.pass_context
async def scrape(ctx, url, depth, stay_in_domain, max_concurrent):
    """Scrape a website asynchronously for links and check for dead links."""
    
    # Validate URL
    try:
        parsed = urlparse(url)
        if not parsed.scheme:
            url = f"http://{url}"
            console.print(f"[yellow]⚠️  No scheme provided, assuming: {url}[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Invalid URL: {e}[/red]")
        return
    
    logger.debug(f"Starting scrape with options: url={url}, depth={depth}, stay_in_domain={stay_in_domain}")
    
    try:
        scraper = AsyncScraper(
            start_url=url,
            max_depth=depth,
            stay_in_domain=stay_in_domain,
            max_concurrent=max_concurrent
        )
        await scraper.run()
    except KeyboardInterrupt:
        console.print("\\n[yellow]⚠️  Scraping interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Scraping failed: {e}[/red]")
        logger.error(f"Scrape command error: {e}")
        raise