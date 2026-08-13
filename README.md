# SAMP-TMRP-BOT-Discord-Game-
 Multiverse Roleplay — Live SA-MP Server Discord Integration Bot
**Multiverse Roleplay Live SA-MP Integration Bot** is a 1,280+ line specialized Python automation engine developed by **MD SIBBIR AHMED**. Built with `Discord.py`, `mysql.connector`, `PIL (Pillow)`, and `asyncio`, the bot establishes a direct real-time bridge between the **Multiverse Roleplay** SA-MP game server MySQL database and the community Discord server.
### Key Technical Architecture
- **Real-Time Server Status Dashboard**: Continuously queries the live SA-MP MySQL database every 60 seconds to track online player counts, player names, score metrics, ping latencies, and uptime status. Automatically updates a formatted Markdown live status dashboard embed in Discord.
- **Dynamic PIL Image Graphics Engine**: Utilizes `Pillow (Image, ImageDraw, ImageFont)` to dynamically generate custom visual player identity cards. Combines in-game skin model renders, custom typography (`goodtimes.ttf`), and player stats (level, cash, bank balance, playtime) into high-resolution PNG image cards.
- **Account Verification & Database Sync**: Provides an account-linking bridge that pairs Discord user IDs directly with SA-MP in-game character profiles, verifying player identities and enforcing role synchronization across platforms.
- **Remote In-Game Moderation Suite**: Equips server administrators with real-time player lookups, account inspection, moderation logging, and database query executions directly from Discord commands.
### Key Features
- Automated 60-Second Server Uptime & Live Player Dashboard
- Dynamic PIL Canvas Player Profile & Stat Card Rendering
- Asynchronous MySQL Connection Pool (`mysql.connector`)
- Direct Discord-to-SAMP Account Verification & Role Sync
- Administrative Player Lookup, Ban Logs, and Inventory Inspection
Engineered for high-availability community management, this bot demonstrates backend database integration, asynchronous task scheduling, dynamic image generation, and live game-server telemetry synchronization.
---
**Developer**: MD SIBBIR AHMED  
**GitHub Repository**: [Sibbir2941/SAMP-MRP-Bot](https://github.com/Sibbir2941)  
