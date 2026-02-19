# Reddit Scout

Automated Reddit monitoring tool to find potential customers by tracking keywords and subreddits.

## Features

- Monitor multiple subreddits simultaneously
- Keyword matching with regex support
- Real-time notifications (console, email, webhook)
- Configurable check intervals
- Track seen posts to avoid duplicates

## Installation


## Reddit API Setup

1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Select "script" as the app type
4. Note your `client_id` and `client_secret`
5. Update these values in `config.py`

## Usage

Basic usage:


With email notifications:


With webhook:


## Options

- `--subreddits, -s`: Comma-separated subreddit names (required)
- `--keywords, -k`: Comma-separated keywords, supports regex (required)
- `--interval, -i`: Check interval in seconds (default: 60)
- `--email, -e`: Email address for notifications (optional)
- `--webhook, -w`: Webhook URL for notifications (optional)

## Email Configuration

To use email notifications, update the following in `config.py`:


For Gmail, use an App Password: https://support.google.com/accounts/answer/185833

## Examples

Monitor for SaaS opportunities:


Monitor for specific pain points:


## Tips

- Use regex for flexible matching: `"need.*(tool|software|solution)"`
- Start with longer intervals (120-300s) to avoid rate limits
- Monitor relevant subreddits where your target customers hang out
- Combine multiple notification methods for redundancy

## License

MIT
# 安装依赖
pip install -r requirements.txt

# 基础监控
python main.py start -s "entrepreneur,startups" -k "need help,looking for"

# 带邮件通知
python main.py start -s "entrepreneur" -k "need.*solution" -e "your@email.com" -i 120

# 带 Webhook
python main.py start -s "saas" -k "problem.*software" -w "https://hooks.slack.com/..."