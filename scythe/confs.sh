# current version

export SCYTHE_VERSION=0.3.2

# tool dirs

export CONFS_DIR="$(realpath $SCYTHE_HOME/../confs)"
export EXERCISES_DIR="$(realpath $SCYTHE_HOME/../exercises)"
export HARVESTS_DIR="$(realpath $SCYTHE_HOME/../harvests)"

# user confs

if [ ! -r "$CONFS_DIR/confs.sh" ]; then
	echo "scythe: missing user confs '$CONFS_DIR/confs.sh'" >&2
	exit 1
fi
source "$CONFS_DIR/confs.sh"

# local dirs

export BASE_BUNDLE="$CONFS_DIR/basebundle"
export EXERCISES="$CONFS_DIR/${SCYTHE_EXAM_ID}.txt"
export REGISTERED_UIDS="$CONFS_DIR/${SCYTHE_EXAM_ID}.tsv"
export TM_SETTINGS_SERVER="$CONFS_DIR/${SCYTHE_EXAM_ID}.py"
export TM_SETTINGS_LOCAL="$CONFS_DIR/${SCYTHE_EXAM_ID}-t.py"

export HARVEST="$HARVESTS_DIR/$SCYTHE_EXAM_ID"

# remote endpoint

export REMOTE_ENDPOINT="http://$SCYTHE_SERVER/tm/$SCYTHE_TEACHER_ID/$SCYTHE_EXAM_ID/"

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
