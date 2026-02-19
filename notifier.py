import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from rich.console import Console
from config import Config

console = Console()

class Notifier:
    def __init__(self, config: Config):
        self.config = config
    
    def notify(self, message: dict):
        """Send notifications via configured channels"""
        if self.config.email:
            self.send_email(message)
        
        if self.config.webhook:
            self.send_webhook(message)
    
    def send_email(self, message: dict):
        """Send email notification"""
        if not self.config.smtp_username or not self.config.smtp_password:
            console.print("[yellow]Email credentials not configured, skipping email[/yellow]")
            return
        
        try:
            msg = MIMEMultipart()
            msg["From"] = self.config.smtp_username
            msg["To"] = self.config.email
            msg["Subject"] = f"Reddit Scout: Match in r/{message['subreddit']}"
            
            body = f"""
New potential customer found!

Subreddit: r/{message['subreddit']}
Title: {message['title']}
Author: u/{message['author']}
Matched Keywords: {', '.join(message['keywords'])}
URL: {message['url']}
Time: {message['timestamp']}
"""
            msg.attach(MIMEText(body, "plain"))
            
            with smtplib.SMTP(self.config.smtp_server, self.config.smtp_port) as server:
                server.starttls()
                server.login(self.config.smtp_username, self.config.smtp_password)
                server.send_message(msg)
            
            console.print("[green]✓ Email sent[/green]")
        except Exception as e:
            console.print(f"[red]Email error: {e}[/red]")
    
    def send_webhook(self, message: dict):
        """Send webhook notification"""
        try:
            payload = {
                "text": f"🎯 New Match in r/{message['subreddit']}",
                "title": message['title'],
                "url": message['url'],
                "author": message['author'],
                "keywords": message['keywords'],
                "timestamp": message['timestamp'],
            }
            
            response = requests.post(self.config.webhook, json=payload, timeout=10)
            response.raise_for_status()
            console.print("[green]✓ Webhook sent[/green]")
        except Exception as e:
            console.print(f"[red]Webhook error: {e}[/red]")
