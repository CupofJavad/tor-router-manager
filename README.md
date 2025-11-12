# tor-router-manager

A modular Python SSH tool for managing and rotating Tor exit nodes on OpenWrt-based routers (e.g., [GL.iNet GL-AXT1800](https://www.gl-inet.com/products/gl-axt1800/)). Designed for use on macOS with PyCharm or CLI, it automates the deployment and execution of a router-side script that configures Tor to cycle through a custom list of ExitNodes, with logging, fallback handling, and cron-based scheduling.

---

## 🚀 Features

- 🔄 Rotate Tor exit nodes via custom country list
- 🛑 Auto-fallback when all configured exits fail
- 📡 Remote upload, SSH config, restart, and monitoring
- 🧪 Manual one-shot runs or automated cron jobs
- 🔍 Tail logs and verify bootstrap/debug info from your Mac
- ✅ Built with Paramiko, PyYAML, and clean modular structure

---

## 🖥️ Requirements

- Python 3.8+
- PyCharm (recommended) or CLI with `pip`
- Router running **OpenWrt** or **GL.iNet firmware v4+**
- Tor installed on router: `opkg update && opkg install tor`
- SSH access (password or key-based)

---

## 📦 Install & Setup

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/tor-router-manager.git
cd tor-router-manager
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your router connection

Edit `config.yaml`:

```yaml
router:
  host: "192.168.8.1"
  user: "root"
  password: ""       # or use key_path
  key_path: "~/.ssh/id_rsa"

tor:
  exit_list: ["IR", "KP", "SY", "VE", "SD", "ER", "BY", "CU", "NI", "MM", "CG"]
  fallback_cc: "SE"

schedule:
  line: "0 */4 * * * /root/rotate_exit.sh >/root/tor-rotate.log 2>&1"
```

---

## ▶️ Usage

### Launch from PyCharm or Terminal:

```bash
python main.py
```

You’ll see:

```text
Tor Router Manager — Menu
1) Deploy/Update router script
2) Ensure torrc basics + Restart Tor
3) Run rotation now (one shot)
4) Install 4-hour cron
5) Remove cron
6) Tail rotation log (last 60)
7) Show Tor bootstrap log lines
8) Edit EXIT_LIST and redeploy
9) Edit FALLBACK_CC and redeploy
10) Check exit IP (from this Mac)
0/q) Quit
```

---

## 🧪 Testing

To test rotation without cron:

1. Deploy script → `1`
2. Ensure torrc config → `2`
3. Run once → `3`
4. Tail output → `6`

For quicker testing, set a temporary fast cron:

```yaml
line: "*/5 * * * * /root/rotate_exit.sh >/root/tor-rotate.log 2>&1"
```

---

## 🔁 How It Works

- A shell script is rendered locally with your EXIT_LIST + fallback.
- Uploaded as `/root/rotate_exit.sh` on the router.
- Each run rotates to the next configured exit, restarts Tor, checks bootstrap.
- If all fail, a fallback country is used.
- All output logged to `/root/tor-rotate.log`.

---

## 📂 Project Structure

```bash
tor-router-manager/
├── main.py                # Entry point
├── ssh_utils.py           # SSH & SFTP helpers
├── tor_actions.py         # Tor-related router-side logic
├── config_handler.py      # Config load/save/edit
├── menu.py                # CLI interface
├── templates/
│   └── rotate_exit.sh     # Router-side shell script template
├── config.yaml            # Your config (editable)
├── requirements.txt
└── .gitignore
```

---

## 🔐 Security Notes

- Use SSH key auth (`key_path`) to avoid storing passwords.
- Nothing leaves your local machine — no 3rd-party APIs.

---

## 🧰 Development

Want to scaffold a fresh copy?

```bash
chmod +x bootstrap.sh
./bootstrap.sh
```

CLI-friendly, modular, and easy to adapt.

---

## 🧑‍💻 Author

**Javad** — *jack of all trades*  
Built with ❤️ on macOS + PyCharm

---

## 📄 License

MIT License — free for personal or commercial use.

---

## 🌐 Verify Tor Exit

Visit:

- https://check.torproject.org  
- https://ipleak.net

...while browsing through your router to confirm the exit node matches.

---

## 🙋 Need More?

Want to:
- Push to GitHub?
- Add Telegram alerts?
- Track uptime or geolocate current exit?

Let me know. This is built to evolve.