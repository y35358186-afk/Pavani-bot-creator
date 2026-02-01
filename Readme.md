# 🤖 Pavani Bot Creator

> **Deploy, Manage, and Monetize Telegram Bots with a Beautiful Web Interface**

[![Deploy to Render](https://img.shields.io/badge/Deploy%20to-Render-46E3B7?style=for-the-badge&logo=render)](https://render.com)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

A modern, mobile-first platform for deploying and managing Telegram bots with real-time monitoring, built-in monetization, and a beautiful purple/pink gradient UI.

## ✨ Features

- 🚀 **One-Click Bot Deployment** - Upload Python files and deploy instantly
- 📊 **Real-Time Monitoring** - Live logs streamed via WebSocket
- 🎨 **Beautiful Modern UI** - Gradient design, mobile-optimized
- 💰 **Built-in Monetization** - Ad system ready (PropellerAds/AdSense)
- 📱 **PWA Support** - Install as mobile app on any device
- 🌐 **Full API Access** - Bots can reach any internet API (TrueFX, Finnhub, etc.)
- ⚡ **Auto-Install Dependencies** - Reads and installs from requirements.txt
- 🔒 **Secure** - Password-protected admin panel
- 🔄 **Complete Bot Control** - Start, stop, restart, delete
- 📁 **Native File Picker** - Easy mobile file uploads
- 🎬 **30-Second Ad System** - Enforced ad viewing before deployment
- ∞ **Unlimited Bots** - Deploy as many as you need

## 🎯 Perfect For

- 🤖 Bot developers needing easy deployment
- 📲 Managing multiple Telegram/Discord bots
- 🧪 Testing bots in production environment
- 💵 Monetizing bot deployment services
- 📚 Learning bot development and deployment

## 🚀 Quick Deploy (5 Minutes)

### 1. Fork This Repository

Click the "Fork" button at the top right

### 2. Deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

**Or manually:**

1. Create account on [Render](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   ```
   Name: pavani-bot-creator
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app:app --host 0.0.0.0 --port $PORT
   ```
5. Add Environment Variable:
   ```
   ADMIN_PASSWORD = @Xavier1
   ```
6. Click "Create Web Service"
7. Wait 5 minutes - Done! 🎉

### 3. Access Your Platform

Visit: `https://your-app-name.onrender.com`

**Login:** `@Xavier1` (or your custom password)

## 💻 Local Development

### Prerequisites
- Python 3.8+
- pip

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/pavani-bot-creator.git
cd pavani-bot-creator

# Install dependencies
pip install -r requirements.txt

# Run application
uvicorn app:app --reload
```

Visit `http://localhost:8000`

**Default password:** `@Xavier1`

## 📱 Mobile Development (Android - Pydroid 3)

Perfect for coding on your phone!

```bash
# In Pydroid 3 terminal
pip install fastapi uvicorn python-multipart websockets

# Run
python app.py
```

Visit `http://localhost:8000` in mobile browser

## 🤖 Deploy Your First Bot

### 1. Create Your Bot

```python
# my_bot.py
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MyBot:
    def __init__(self):
        self.running = True
        
    async def run(self):
        logger.info("🚀 Bot starting...")
        
        while self.running:
            try:
                # Your bot logic here
                logger.info("📊 Bot working...")
                await asyncio.sleep(60)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error: {e}")
                await asyncio.sleep(10)

if __name__ == "__main__":
    bot = MyBot()
    asyncio.run(bot.run())
```

### 2. Create Requirements

```txt
# requirements.txt
requests==2.31.0
aiohttp==3.9.1
python-telegram-bot==20.7
```

### 3. Deploy via Dashboard

1. Login to your platform
2. Click "📁 Select bot.py"
3. Choose your bot file
4. Click "📁 Select requirements.txt"
5. Choose requirements file
6. Click "🎬 Watch Ad & Deploy"
7. Wait 30 seconds
8. Click "✅ Skip & Deploy"
9. **Bot runs 24/7 automatically!**

## 💰 Monetization Setup

### Add Real Ads (No Coding Required!)

#### Option 1: PropellerAds (Easiest - Instant Approval)

1. Sign up: [PropellerAds Publishers](https://publishers.propellerads.com)
2. Create ad zone
3. Copy script tag: `<script src="//propellerads.com/12345/zone.js"></script>`
4. In `app.py` line ~95, replace:

```html
<!-- OLD: -->
<div style="padding:30px;background:#0F172A...">
  <div>🎯 Pavani Bot Creator</div>
</div>

<!-- NEW: -->
<div style="padding:20px;background:#0F172A;min-height:250px">
  <script async src="//propellerads.com/YOUR_ID/YOUR_ZONE.js"></script>
</div>
```

5. Deploy - Earn immediately! 💰

#### Option 2: Google AdSense (Higher Revenue)

1. Apply: [Google AdSense](https://google.com/adsense)
2. Wait 1-2 weeks for approval
3. Get ad code
4. Replace in `app.py` line ~95
5. Deploy - Higher earnings! 💵

**Revenue Potential:**
- 100 users/day: $50-200/month
- 1000 users/day: $500-2000/month

See full guide: [ADS_MONETIZATION_GUIDE.md](ADS_MONETIZATION_GUIDE.md)

## 🎨 Customization

### Change Password

Environment variable on Render:
```
ADMIN_PASSWORD=YourSecurePassword
```

### Change Colors

Edit CSS in `app.py`:
```css
--primary: #8B5CF6;    /* Purple */
--secondary: #EC4899;  /* Pink */
--dark: #0F172A;       /* Background */
```

### Change Ad Timer

In JavaScript (line ~97):
```javascript
let timeLeft = 30; // Seconds
```

## 📚 Documentation

- **[Mobile Guide](MOBILE_GUIDE.md)** - Deploy from phone
- **[Ad Monetization](ADS_MONETIZATION_GUIDE.md)** - Setup ads
- **[How Ads Work](HOW_ADS_WORK.md)** - Technical details

## 🏗️ Architecture

### Tech Stack
- **Backend:** FastAPI (Python 3.8+)
- **Frontend:** Embedded HTML/CSS/JS
- **Real-time:** WebSockets
- **Deployment:** Render (Docker-compatible)
- **Mobile:** PWA

### File Structure
```
pavani-bot-creator/
├── app.py                      # Main application (100 lines!)
├── requirements.txt            # Python dependencies
├── Procfile                    # Render deployment config
├── README.md                   # This file
├── MOBILE_GUIDE.md            # Mobile deployment guide
├── ADS_MONETIZATION_GUIDE.md  # Ad setup guide
└── HOW_ADS_WORK.md            # Technical ad explanation
```

## 🔧 How It Works

### Bot Deployment Process

1. **User uploads** bot.py and requirements.txt
2. **System saves** files to `deployed_bots/` folder
3. **Auto-installs** dependencies: `pip install -r requirements.txt`
4. **Creates subprocess**: `python bot.py`
5. **Monitors output** via stdout/stderr
6. **Streams logs** to dashboard via WebSocket
7. **Bot runs 24/7** until stopped

### Security

- ✅ Password hashing (SHA-256)
- ✅ Session-based authentication
- ✅ CORS configured
- ✅ No code execution in main process
- ✅ Isolated bot processes

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repo
2. Create feature branch (`git checkout -b feature/Amazing`)
3. Commit changes (`git commit -m 'Add Amazing'`)
4. Push to branch (`git push origin feature/Amazing`)
5. Open Pull Request

## 📝 License

MIT License - see [LICENSE](LICENSE)

## ⚠️ Important Notes

### For Production Use:
- Change default password
- Add database for persistence (PostgreSQL)
- Setup monitoring (UptimeRobot)
- Add rate limiting
- Configure backups

### Render Free Tier:
- ✅ 750 hours/month
- ⚠️ Sleeps after 15 min inactivity
- ⚠️ 30s wake-up time
- Solution: UptimeRobot or upgrade to paid tier

## 🐛 Troubleshooting

### Bot Won't Start
- Check logs for errors
- Verify requirements.txt syntax
- Test bot locally first

### WebSocket Not Connecting
- Normal on free tier sleep
- Visit URL to wake app
- Check browser console

### Ads Not Showing
- Verify ad code is correct
- Check ad network dashboard
- Test on deployed URL (not localhost)

## 🎯 Roadmap

- [ ] Database integration (PostgreSQL)
- [ ] Multi-user support
- [ ] Bot templates library
- [ ] Email notifications
- [ ] Performance analytics
- [ ] Docker compose setup
- [ ] API for programmatic access
- [ ] Scheduled tasks
- [ ] Bot marketplace

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/pavani-bot-creator/issues)
- **Questions:** [Discussions](https://github.com/yourusername/pavani-bot-creator/discussions)

## ⭐ Show Your Support

If this project helped you, please give it a ⭐!

---

<div align="center">

**Made with ❤️ for bot developers worldwide**

[Deploy Now](https://render.com) • [Report Bug](https://github.com/yourusername/pavani-bot-creator/issues) • [Request Feature](https://github.com/yourusername/pavani-bot-creator/issues)

**Pavani Bot Creator** - Deploy bots, not infrastructure 🚀

</div>
