# current version

export SCYTHE_VERSION=1.3.3

# user confs

export CONFS_DIR="$(realpath -eL $SCYTHE_HOME/../confs)"
if [ ! -r "$CONFS_DIR/confs.sh" ]; then
	echo "scythe: missing user confs '$CONFS_DIR/confs.sh'" >&2
	exit 1
fi

# defaults

export EXERCISES_DIR="$SCYTHE_HOME/../exercises"
export BACKUPS_DIR="$SCYTHE_HOME/../backups"

export BASE_BUNDLE="$CONFS_DIR/basebundle"
export EXERCISES="$CONFS_DIR/${SCYTHE_SESSION_ID}.txt"
export REGISTERED_UIDS="$CONFS_DIR/${SCYTHE_SESSION_ID}.tsv"

export TM_SETTINGS="$CONFS_DIR/${SCYTHE_SESSION_ID}-tm.py"
export ST_SETTINGS="$CONFS_DIR/${SCYTHE_SESSION_ID}-st.py"

export SCYTHE_BACKUPS="$BACKUPS_DIR/$SCYTHE_SESSION_ID"

# possibly ovverriden by user values

source "$CONFS_DIR/confs.sh"

# fix missing SCYTHE_EDITOR

if [ -z "$SCYTHE_EDITOR" ]; then
	export SCYTHE_EDITOR="$EDITOR"
fi

# make all path absolute

export EXERCISES_DIR="$(realpath -mL $EXERCISES_DIR)"
if [ ! -d "$EXERCISES_DIR" ]; then
	echo "scythe: missing exercises dir '$EXERCISES_DIR'" >&2
	exit 1
fi
export BACKUPS_DIR="$(realpath -mL $BACKUPS_DIR)"
if [ ! -d "$BACKUPS_DIR" ]; then
	echo "scythe: missing backups dir '$BACKUPS_DIR'" >&2
	exit 1
fi

export BASE_BUNDLE="$(realpath -mL $BASE_BUNDLE)"
export EXERCISES="$(realpath -mL $EXERCISES)"
export REGISTERED_UIDS="$(realpath -mL $REGISTERED_UIDS)"

export TM_SETTINGS="$(realpath -mL $TM_SETTINGS)"
export ST_SETTINGS="$(realpath -mL $ST_SETTINGS)"
export SCYTHE_BACKUPS="$(realpath -mL $SCYTHE_BACKUPS)"

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
