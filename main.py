import typer
from rich.console import Console
from monitor import RedditMonitor
from config import Config

app = typer.Typer()
console = Console()

@app.command()
def start(
    subreddits: str = typer.Option(..., "--subreddits", "-s", help="Comma-separated subreddit names"),
    keywords: str = typer.Option(..., "--keywords", "-k", help="Comma-separated keywords (supports regex)"),
    check_interval: int = typer.Option(60, "--interval", "-i", help="Check interval in seconds"),
    email: str = typer.Option(None, "--email", "-e", help="Email address for notifications"),
    webhook: str = typer.Option(None, "--webhook", "-w", help="Webhook URL for notifications"),
):
    """Start monitoring Reddit for potential customers"""
    config = Config(
        subreddits=subreddits.split(","),
        keywords=keywords.split(","),
        check_interval=check_interval,
        email=email,
        webhook=webhook,
    )
    
    console.print("[bold green]Starting Reddit Scout...[/bold green]")
    console.print(f"Monitoring subreddits: {', '.join(config.subreddits)}")
    console.print(f"Keywords: {', '.join(config.keywords)}")
    console.print(f"Check interval: {config.check_interval}s\n")
    
    monitor = RedditMonitor(config)
    monitor.start()

if __name__ == "__main__":
    app()
