# menu.py — v1.1.0
# CLI menu loop for tor-router-manager.

from config_handler import update_exit_list, update_fallback_cc
from tor_actions import (
    render_and_upload_script,
    ensure_tor_basics,
    restart_tor,
    run_rotation_now,
    install_cron,
    remove_cron,
    tail_log,
    show_bootstrap_log,
    check_exit_ip
)

def display_menu():
    print("\nTor Router Manager — Menu")
    print("1) Deploy/Update router script")
    print("2) Ensure torrc basics + Restart Tor")
    print("3) Run rotation now (one shot)")
    print("4) Install 4-hour cron")
    print("5) Remove cron")
    print("6) Tail rotation log (last 60)")
    print("7) Show Tor bootstrap log lines")
    print("8) Edit EXIT_LIST and redeploy")
    print("9) Edit FALLBACK_CC and redeploy")
    print("10) Check exit IP (from this Mac)")
    print("0/q) Quit")

def menu_loop(cfg, client):
    while True:
        display_menu()
        choice = input("Select option: ").strip().lower()

        if choice == "1":
            render_and_upload_script(cfg, client)
        elif choice == "2":
            ensure_tor_basics(client)
            restart_tor(client)
        elif choice == "3":
            run_rotation_now(client)
        elif choice == "4":
            install_cron(cfg, client)
        elif choice == "5":
            remove_cron(cfg, client)
        elif choice == "6":
            tail_log(client)
        elif choice == "7":
            show_bootstrap_log(client)
        elif choice == "8":
            edit_exit_list(cfg)
            render_and_upload_script(cfg, client)
        elif choice == "9":
            edit_fallback_cc(cfg)
            render_and_upload_script(cfg, client)
        elif choice == "10":
            check_exit_ip()
        elif choice in ("0", "q"):
            break
        else:
            print("Invalid input. Try again.")

def edit_exit_list(cfg):
    current = cfg["tor"]["exit_list"]
    print(f"Current EXIT_LIST: {current}")
    raw = input("New space-separated EXIT_LIST (or blank to cancel): ").strip()
    if raw:
        new_list = [c.strip().upper() for c in raw.split() if c.strip()]
        update_exit_list(cfg, new_list)
        print(f"✓ EXIT_LIST updated to: {new_list}")

def edit_fallback_cc(cfg):
    current = cfg["tor"]["fallback_cc"]
    print(f"Current FALLBACK_CC: {current}")
    raw = input("New fallback country code (2-letter ISO): ").strip().upper()
    if raw:
        update_fallback_cc(cfg, raw)
        print(f"✓ FALLBACK_CC updated to: {raw}")