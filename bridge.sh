#!/system/bin/sh
# Sleeps until the Fire remote appears on Bluetooth. Only then does it
# look for the PC. While the remote is gone, this process is blocked in
# the kernel and does not poll.
PC=$1
PORT=$2
TOKEN=$3
GRAB=/data/local/tmp/grabevent
SESSION=/data/local/tmp/bridge-session.sh

if [ -z "$BRIDGE_INNER" ]; then
  export BRIDGE_INNER=1
  setsid /system/bin/sh "$0" "$PC" "$PORT" "$TOKEN" </dev/null >>/data/local/tmp/bridge.log 2>&1 &
  exit 0
fi

trap '' HUP
echo $$ >/data/local/tmp/bridge.pid
export PC PORT TOKEN GRAB
echo "bridge $$ waiting for the remote" >>/data/local/tmp/bridge.log

find_dev() {
  dev=
  getevent -pl 2>/dev/null | while IFS= read -r line; do
    case "$line" in
      *"add device"*)
        dev=${line##* }
        ;;
      *"AR Keyboard"*)
        printf '%s\n' "$dev"
        break
        ;;
    esac
  done
}

while true; do
  dev=$(find_dev)
  if [ -n "$dev" ]; then
    echo "remote already at $dev" >>/data/local/tmp/bridge.log
    /system/bin/sh "$SESSION" direct "$dev"
  fi
  echo "sleeping until bluetooth remote appears" >>/data/local/tmp/bridge.log
  toybox inotifyd "$SESSION" /dev/input:n
  echo "inotifyd stopped" >>/data/local/tmp/bridge.log
  sleep 20
done
