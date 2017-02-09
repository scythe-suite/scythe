# Installation instructions

Download `scythe.zip`, `exercises.zip`, and `confs.zip` from [this project
releases](https://github.com/scythe-suite/scythe/releases).

Create an empty dir that we'll call the **base dir** and unzip the first archive
in it; every time you'll need to use this tool, just go where to the *base dir*
and set the path using

    source ./setpath.sh

The first time (or when an upgrade of the tool is issued), install the
dependencies with

    scythe init

this will download the latest releases of `tristo-mietitore`, `sim-fun-i`,
`scythe-viewer` and `md2html`.

Now you need to setup configurations; unzip `confs.zip` in the *base dir*, go in
the newly created `confs` dir and copy `confs.sh-template` to `confs.sh`, edit
the first lines of such files

    export DEFAULT_TEACHER_ID="<DEFAULT_TEACHER_HERE>"
    export REMOTE_USER="<REMOTE_USER_HERE>"
    export REMOTE_HOST="<REMOTE_HOST_HERE>"
    export SCYTHE_USE_SANDBOX="<NOT_NULL_IF_DOCKER_IS_AVAILABLE>"

to reflect your username, the credentials of the deploy site and whether to use
Docker as a sandbox for running the tests.

Finally, make a directory named `./dirs` in the *base dir* and unzip
`exercises.zip` in it.

If you want to edit and keep track of your configuration and exercises you are
suggested to turn `confs` and `dirs/exercises` to git repositories.

## Use

Choose an id for your exam, say `test_exam`, to prepare an exam just add

    ./confs/test_exam.txt
    ./confs/test_exam.tsv

the first file should contain a *secret* followed by a list of exercise names,
the second file should cotain a tab-separated list of *unique id*, and *last and
first name* (exactly one tab per line, after the ids).

To prepare the configuartion file, just run

    . ./setpath.sh
    scythe prepare test_exam

that will generate `./confs/test_exam.py`, the required configuration file.
