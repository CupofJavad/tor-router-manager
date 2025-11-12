#!/bin/ash
# rotate_exit.sh — v1.0.0
# Rotates Tor ExitNodes on OpenWrt-based routers.

TORRC="/etc/tor/torrc"
INDEX_FILE="/etc/tor/exit_index"

# ==== FILLED BY MANAGER ====
EXIT_LIST="__EXIT_LIST__"
FALLBACK_CC="__FALLBACK_CC__"
# ===========================

ensure_basics() {
  grep -q '^ControlPort ' "$TORRC" || echo "ControlPort 9051" >> "$TORRC"
  grep -q '^CookieAuthentication ' "$TORRC" || echo "CookieAuthentication 1" >> "$TORRC"
  grep -q '^DataDirectory ' "$TORRC" || echo "DataDirectory /var/lib/tor" >> "$TORRC"
}

set_exit_country() {
  code="$1"
  [ -f "${TORRC}.bak" ] || cp "$TORRC" "${TORRC}.bak"
  sed -i '/^ExitNodes/d;/^StrictNodes/d' "$TORRC"
  printf "ExitNodes {%s}\nStrictNodes 1\n" "$code" >> "$TORRC"
}

restart_tor() {
  /etc/init.d/tor restart >/dev/null 2>&1
}

bootstrapped_ok() {
  t=0
  while [ $t -lt 90 ]; do
    if logread -e 'Bootstrapped 100%' | tail -n1 | grep -q 'Bootstrapped 100%'; then
      return 0
    fi
    sleep 3
    t=$((t+3))
  done
  return 1
}

[ -f "$INDEX_FILE" ] || echo 0 > "$INDEX_FILE"
idx="$(cat "$INDEX_FILE" 2>/dev/null || echo 0)"

set -- $EXIT_LIST
count=$#
[ $count -gt 0 ] || {
  logger -t tor-rotate "EXIT_LIST is empty"
  echo "EXIT_LIST empty"
  exit 1
}

attempts=0
success=0
ensure_basics

while [ $attempts -lt $count ]; do
  idx=$(( (idx % count) + 1 ))
  i=1; TARGET=""
  for code in $EXIT_LIST; do
    [ $i -eq $idx ] && TARGET="$code" && break
    i=$((i+1))
  done

  set_exit_country "$TARGET"
  restart_tor

  if bootstrapped_ok; then
    logger -t tor-rotate "ExitNodes {${TARGET}} active (index $idx/$count)"
    echo "ExitNodes {${TARGET}} active (index $idx/$count)"
    success=1
    break
  else
    logger -t tor-rotate "Failed to bootstrap with {${TARGET}}; trying next"
    echo "Failed to bootstrap with {${TARGET}}; trying next"
  fi

  attempts=$((attempts+1))
done

echo "$idx" > "$INDEX_FILE"

if [ $success -ne 1 ]; then
  set_exit_country "$FALLBACK_CC"
  restart_tor
  if bootstrapped_ok; then
    logger -t tor-rotate "All requested exits failed; forced {${FALLBACK_CC}}"
    echo "All requested exits failed this run; forced {${FALLBACK_CC}}"
  else
    logger -t tor-rotate "Fallback {${FALLBACK_CC}} also failed; check WAN / Tor service"
    echo "Fallback {${FALLBACK_CC}} also failed; check WAN / Tor service"
  fi
fi