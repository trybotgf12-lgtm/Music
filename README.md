# Telegram Music Bot (Pyrogram + PyTgCalls)

Group voice-chat music bot. Bot account leta hai commands, ek "assistant" (userbot)
account voice chat me join karke actual audio stream karta hai — Telegram bots
khud voice chat join nahi kar sakte, isliye ye 2-account setup standard hai.

## Commands
- `/play <song name / YouTube link>` — play/queue
- `/pause`, `/resume`
- `/skip`
- `/queue`
- `/stop` — leave voice chat

## 1. Credentials lo

1. **API_ID / API_HASH** — https://my.telegram.org → API Development Tools
2. **BOT_TOKEN** — Telegram pe [@BotFather](https://t.me/BotFather) se `/newbot`
3. **SESSION_STRING** — apne PC pe locally ye chalao (Render pe NAHI):
   ```bash
   pip install pyrogram tgcrypto
   python3 generate_session.py
   ```
   Ye ek doosra Telegram account (assistant) use karega jo voice chats join karega.
   Session string kisi ko mat dena — ye full account access deta hai.
4. **OWNER_ID** — apna Telegram numeric user ID (optional, future admin-only commands ke liye)

## 2. GitHub pe push karo

```bash
git init
git add .
git commit -m "Telegram music bot"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

## 3. Render pe Deploy (Free)

1. Render dashboard → **New +** → **Web Service**
2. Apna GitHub repo connect karo
3. **Environment**: `Docker` select karo (Dockerfile already included — ffmpeg
   iske bina Render ke default Python env me install nahi hota, isliye Docker
   zaroori hai)
4. Instance type: **Free**
5. Environment variables add karo (Render dashboard → Environment tab):
   - `API_ID`
   - `API_HASH`
   - `BOT_TOKEN`
   - `SESSION_STRING`
   - `OWNER_ID`
   - `PORT` — Render khud set kar deta hai, chhedo mat
6. **Create Web Service** → deploy start ho jayega. Logs me "PyTgCalls started"
   dikhega jab bot ready ho.

## Free tier ki important limitations

- **Sleep**: Render ka free Web Service ~15 min inactivity ke baad sleep ho sakta
  hai kyunki koi HTTP traffic nahi aata. Bot voice chats me continuously connected
  rehta hai, but agar Render phir bhi spin down kare to bot disconnect ho jayega.
  Isse rokne ke liye ek external uptime pinger (jaise UptimeRobot, free) `/`
  health endpoint ko har 5-10 min me hit karta rehna chahiye.
- **RAM/CPU**: Free tier bahut limited hai (512MB RAM). Ek time pe ek-do voice
  chats ke liye theek hai, heavy multi-group load pe struggle karega.
- **750 hrs/month** free tier limit hai — ek single service 24x7 chalane ke liye
  kaafi hai.
- Bot dono accounts (bot + assistant) ko group me add/admin karna zaroori hai.

## Local testing

```bash
pip install -r requirements.txt
cp .env.example .env   # fill values, then export them or use a tool like `dotenv`
python3 main.py
```
(ffmpeg locally install hona chahiye: `sudo apt install ffmpeg` / `brew install ffmpeg`)

## Project structure

```
tg-music-bot/
├── Dockerfile
├── requirements.txt
├── config.py
├── main.py
├── generate_session.py
└── bot/
    ├── client.py
    ├── helpers/
    │   ├── queue.py
    │   └── ytdl.py
    └── plugins/
        ├── start.py
        ├── play.py
        └── controls.py
```
