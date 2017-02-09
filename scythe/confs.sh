# tool dirs

export CONFS_DIR="$(realpath $SCYTHE_HOME/../confs)"
export EXERCISES_DIR="$(realpath $SCYTHE_HOME/../exercises)"
export HARVESTS_DIR="$(realpath $SCYTHE_HOME/../harvests)"

# autodependencies begin [do not edit this comment]

export TRISTO_MIETITORE_VERSION="v0.2.3"
export SIM_FUN_I_VERSION="v0.2.0"
export SCYTHE_VIEWER_VERSION="v0.2.0"
export MD2HTML_VERSION="v0.2"

# autodependencies end [do not edit this comment]

# user confs

if [ ! -r "$CONFS_DIR/confs.sh" ]; then
	echo "scythe: missing user confs '$CONFS_DIR/confs.sh'" >&2
	exit 1
fi
source "$CONFS_DIR/confs.sh"

# exam and teacher
# (depending on:
#   $SCYTHE_CONF, inherited from the sourcer and
#   $TEACHER_ID possibly in external env
# )

export EXAM_ID="$SCYTHE_CONF"

if [ -z "$TEACHER_ID" ]; then
	TEACHER_ID=$DEFAULT_TEACHER_ID
fi
export TEACHER_ID

# local dirs

export BASE_BUNDLE="$CONFS_DIR/basebundle"
export EXERCISES="$CONFS_DIR/${EXAM_ID}.txt"
export REGISTERED_UIDS="$CONFS_DIR/${EXAM_ID}.tsv"
export TM_SETTINGS="$CONFS_DIR/${EXAM_ID}.py"

export HARVEST="$HARVESTS_DIR/$EXAM_ID"

# remote dirs and commands

export REMOTE_BASEDIR="/home/$REMOTE_USER/esami/$TEACHER_ID/$EXAM_ID"
export REMOTE_UPLOADS="$REMOTE_BASEDIR/uploads"
export REMOTE_ENDPOINT="http://$REMOTE_HOST/tm/$TEACHER_ID/$EXAM_ID/"
export REMOTE_RUN_COMMAND="cd /home/$REMOTE_USER/esami/ && /home/$REMOTE_USER/tm/run_tm.sh '$TEACHER_ID/$EXAM_ID'"
export REMOTE_STOP_COMMAND="docker rm -f '$TEACHER_ID-$EXAM_ID'"
export REMOTE_SESSIONS_COMMAND="if ! docker ps --filter label=scythe=tm | grep -q '$TEACHER_ID-$EXAM_ID'; then echo Stopped; else echo WARNING STILL RUNNING; fi"
export REMOTE_LOGTAIL_COMMAND="tail -f '$REMOTE_BASEDIR/uploads/'*.log"

# misc

export PYTHONPATH="$SCYTHE_HOME/bin/tm:$SCYTHE_HOME/bin/sf"
