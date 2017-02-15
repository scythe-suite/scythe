#

export SCYTHE_VERSION=0.3.1

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

# exam and teacher
# (depending on:
#   $SCYTHE_CONF, inherited from the sourcer and
#   $TEACHER_ID possibly in external env, or $SCYTHE_TEACHER_ID from sourcer
# )

export EXAM_ID="$SCYTHE_CONF"

if [ -z "$TEACHER_ID" ]; then
	TEACHER_ID="$SCYTHE_TEACHER_ID"
fi
export TEACHER_ID

# local dirs

export BASE_BUNDLE="$CONFS_DIR/basebundle"
export EXERCISES="$CONFS_DIR/${EXAM_ID}.txt"
export REGISTERED_UIDS="$CONFS_DIR/${EXAM_ID}.tsv"
export TM_SETTINGS="$CONFS_DIR/${EXAM_ID}.py"

export HARVEST="$HARVESTS_DIR/$EXAM_ID"

# remote endpoint

export REMOTE_ENDPOINT="http://$SCYTHE_SERVER/tm/$TEACHER_ID/$EXAM_ID/"

# functions

suite_latest_version() {
	last_release_url=$(curl -sLo /dev/null -w '%{url_effective}' "https://github.com/scythe-suite/$1/releases/latest")
	echo "${last_release_url##*/}"
}
