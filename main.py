# main.py — v1.1.0
# Entry point. Loads config, manages SSH, runs menu loop.

from ssh_utils import make_client
from config_handler import load_config
from menu import menu_loop

def main():
    cfg = load_config()
    try:
        with make_client(cfg) as client:
            menu_loop(cfg, client)
    except Exception as e:
        print(f"[SSH] Failed to connect to {cfg['router']['host']}: {e}")
        print("Tip: check SSH IP, auth credentials, and router status.")

if __name__ == "__main__":
    main()