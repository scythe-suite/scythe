export SCYTHE_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/scythe"
export PYTHONPATH="$SCYTHE_HOME/bin/tm:$SCYTHE_HOME/bin/sf"
export PATH="$SCYTHE_HOME/bin:$PATH"
