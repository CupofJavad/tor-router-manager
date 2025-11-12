# config_handler.py — v1.1.0
# Loads, saves, and updates config.yaml using PyYAML.

import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent / "config.yaml"

def load_config():
    return yaml.safe_load(CONFIG_PATH.read_text())

def save_config(cfg):
    CONFIG_PATH.write_text(yaml.safe_dump(cfg, sort_keys=False))

def update_exit_list(cfg, new_list):
    cfg["tor"]["exit_list"] = new_list
    save_config(cfg)

def update_fallback_cc(cfg, new_cc):
    cfg["tor"]["fallback_cc"] = new_cc
    save_config(cfg)