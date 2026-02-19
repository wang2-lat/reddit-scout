import re
import time
import schedule
import praw
from rich.console import Console
from datetime import datetime
from config import Config
from notifier import Notifier

console = Console()

class RedditMonitor:
    def __init__(self, config: Config):
        self.config = config
        self.notifier = Notifier(config)
        self.reddit = praw.Reddit(
            client_id=config.reddit_client_id,
            client_secret=config.reddit_client_secret,
            user_agent=config.reddit_user_agent,
        )
        self.seen_posts = set()
        
    def check_posts(self):
        """Check for new posts matching keywords"""
        for subreddit_name in self.config.subreddits:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                for post in subreddit.new(limit=20):
                    if post.id in self.seen_posts:
                        continue
                    
                    self.seen_posts.add(post.id)
                    
                    # Check if post matches any keyword
                    text = f"{post.title} {post.selftext}".lower()
                    matched_keywords = []
                    
                    for keyword in self.config.keywords:
                        try:
                            if re.search(keyword.lower(), text):
                                matched_keywords.append(keyword)
                        except re.error:
                            # If not valid regex, treat as plain text
                            if keyword.lower() in text:
                                matched_keywords.append(keyword)
                    
                    if matched_keywords:
                        self.handle_match(post, matched_keywords)
                        
            except Exception as e:
                console.print(f"[red]Error checking r/{subreddit_name}: {e}[/red]")
    
    def handle_match(self, post, keywords):
        """Handle a matched post"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message = {
            "title": post.title,
            "url": f"https://reddit.com{post.permalink}",
            "subreddit": post.subreddit.display_name,
            "author": str(post.author),
            "keywords": keywords,
            "timestamp": timestamp,
        }
        
        # Console notification
        console.print(f"\n[bold yellow]🎯 Match Found![/bold yellow] [{timestamp}]")
        console.print(f"[cyan]Subreddit:[/cyan] r/{message['subreddit']}")
        console.print(f"[cyan]Title:[/cyan] {message['title']}")
        console.print(f"[cyan]Author:[/cyan] u/{message['author']}")
        console.print(f"[cyan]Keywords:[/cyan] {', '.join(keywords)}")
        console.print(f"[cyan]URL:[/cyan] {message['url']}\n")
        
        # Send notifications
        self.notifier.notify(message)
    
    def start(self):
        """Start monitoring loop"""
        console.print("[green]Monitor started. Press Ctrl+C to stop.[/green]\n")
        
        # Initial check
        self.check_posts()
        
        # Schedule periodic checks
        schedule.every(self.config.check_interval).seconds.do(self.check_posts)
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            console.print("\n[yellow]Stopping monitor...[/yellow]")
