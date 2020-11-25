# current version

export SCYTHE_VERSION=1.3.1

# tool dirs

export CONFS_DIR="$(realpath -eL $SCYTHE_HOME/../confs)"
export EXERCISES_DIR="$(realpath -eL $SCYTHE_HOME/../exercises)"
export BACKUPS_DIR="$(realpath -eL $SCYTHE_HOME/../backups)"

# local dirs

export BASE_BUNDLE="$CONFS_DIR/basebundle"
export EXERCISES="$CONFS_DIR/${SCYTHE_SESSION_ID}.txt"
export REGISTERED_UIDS="$CONFS_DIR/${SCYTHE_SESSION_ID}.tsv"
export TM_SETTINGS="$CONFS_DIR/${SCYTHE_SESSION_ID}-tm.py"
export ST_SETTINGS="$CONFS_DIR/${SCYTHE_SESSION_ID}-st.py"

export SCYTHE_BACKUPS="$BACKUPS_DIR/$SCYTHE_SESSION_ID"

# user confs (here so that can override any of the above)

if [ ! -r "$CONFS_DIR/confs.sh" ]; then
	echo "scythe: missing user confs '$CONFS_DIR/confs.sh'" >&2
	exit 1
fi
source "$CONFS_DIR/confs.sh"
if [ -z "$SCYTHE_EDITOR" ]; then
	export SCYTHE_EDITOR="$EDITOR"
fi


# functions

suite_latest_version() {
	local last_release_url=$(curl -sLo /dev/null -w '%{url_effective}' "https://github.com/scythe-suite/$1/releases/latest")
	echo "${last_release_url##*/}"
}

convert_mds() {
	local src_dir="$1"
	local dst_dir="$2"
	local name

	for doc in "$src_dir"/*.md; do
		name="${doc##*/}"
		name="${name%.md}"
		md2html "$doc" "$name" "$dst_dir/${name}.html"
	done
}
