# tor_actions.py — v1.1.0
# Tor-related actions executed on the remote router.

from pathlib import Path
from ssh_utils import run, sftp_put

ROOT = Path(__file__).resolve().parent

REMOTE_SCRIPT = "/root/rotate_exit.sh"
REMOTE_TORRC  = "/etc/tor/torrc"
CRONTAB_FILE  = "/etc/crontabs/root"
CRON_SERVICE  = "/etc/init.d/cron"
TEMPLATE_PATH = ROOT / "templates" / "rotate_exit.sh"

def render_and_upload_script(cfg, client):
    exit_list = cfg["tor"]["exit_list"]
    fallback  = cfg["tor"]["fallback_cc"]

    tpl = TEMPLATE_PATH.read_text()
    rendered = tpl.replace("__EXIT_LIST__", " ".join(exit_list)) \
                  .replace("__FALLBACK_CC__", fallback)

    temp_script = ROOT / "_rotate_exit.rendered.sh"
    temp_script.write_text(rendered)

    sftp_put(client, str(temp_script), REMOTE_SCRIPT)
    print(f"✓ Uploaded router script with {exit_list=} {fallback=}")

def ensure_tor_basics(client):
    cmds = [
        f"grep -q '^ControlPort ' {REMOTE_TORRC} || echo 'ControlPort 9051' >> {REMOTE_TORRC}",
        f"grep -q '^CookieAuthentication ' {REMOTE_TORRC} || echo 'CookieAuthentication 1' >> {REMOTE_TORRC}",
        f"grep -q '^DataDirectory ' {REMOTE_TORRC} || echo 'DataDirectory /var/lib/tor' >> {REMOTE_TORRC}",
    ]
    for cmd in cmds:
        run(client, cmd)
    print("✓ Ensured torrc contains required directives")

def restart_tor(client):
    rc, _, _ = run(client, "/etc/init.d/tor restart")
    print(f"↻ Restarted Tor (rc={rc})")

def run_rotation_now(client):
    rc, out, err = run(client, REMOTE_SCRIPT)
    print(out or err or f"(exit {rc})")

def tail_log(client, lines=60):
    rc, out, _ = run(client, f"tail -n {lines} /root/tor-rotate.log 2>/dev/null || true")
    print(out or "(no log yet)")

def show_bootstrap_log(client):
    rc, out, _ = run(client, "logread -e 'Bootstrapped 100%' | tail -n 10 || true")
    print(out or "(no bootstrap logs found)")

def install_cron(cfg, client):
    cron_line = cfg["schedule"]["line"]
    rc, out, _ = run(client, f"grep -F '{cron_line}' {CRONTAB_FILE} || true")
    if not out:
        run(client, f"echo '{cron_line}' >> {CRONTAB_FILE}")
        run(client, f"{CRON_SERVICE} restart")
        print(f"✓ Installed cron: {cron_line}")
    else:
        print("✓ Cron already installed")
        run(client, f"{CRON_SERVICE} restart")

def remove_cron(cfg, client):
    cron_line = cfg["schedule"]["line"]
    run(client, f"sed -i '\\|{cron_line}|d' {CRONTAB_FILE}")
    run(client, f"{CRON_SERVICE} restart")
    print("✓ Removed cron and restarted service")

def check_exit_ip():
    import requests
    try:
        resp = requests.get("https://check.torproject.org/", timeout=10)
        if "Congratulations. This browser is configured to use Tor" in resp.text:
            print("✓ Tor detected at check.torproject.org")
        else:
            print("⚠️  Tor not detected — traffic not exiting via Tor.")
    except Exception as e:
        print(f"Error checking exit IP: {e}")