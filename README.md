# Instagram Welcome Bot

**Features:**
- Bold + flashy welcome messages (Unicode + emojis)
- Auto @username + member count
- Random welcome message support
- Anti-leave alerts
- Admin commands:
  - `!setwelcome <text>` → add new welcome message
  - `!removewelcome <text>` → remove welcome message
  - `!addadmin <username>` → add admin
  - `!removeadmin <username>` → remove admin

**Setup (Termux / Linux / Windows):**

1. Install Python & pip
```bash
pkg update && pkg upgrade
pkg install python git  # Termux
