from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Config:
    subreddits: List[str]
    keywords: List[str]
    check_interval: int
    email: Optional[str] = None
    webhook: Optional[str] = None
    
    # Reddit API credentials (users need to set these)
    reddit_client_id: str = "YOUR_CLIENT_ID"
    reddit_client_secret: str = "YOUR_CLIENT_SECRET"
    reddit_user_agent: str = "reddit-scout/1.0"
    
    # Email settings (if using email notifications)
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
