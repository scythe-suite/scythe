# Installation instructions

To install the tool perform the following steps:

Download the last release of `scythe.zip`, `exercises.zip`, and `confs.zip` from
[this project releases](https://github.com/scythe-suite/scythe/releases).

Create an empty dir that we'll be the **base dir** and unzip the first archive
in it; every time you'll need to use this tool, just go to the *base dir* and
set the required environment variables using

    source ./setpath.sh

If you use [direnv](https://direnv.net/) just link `setpath.sh` to `.envrc` and
direnv will take care of this step for you!

Then install the various dependencies (this must be done the first time you use
the tool, or when an update is issued) simply running

    scythe init

this will download the latest releases of [tristo-mietitore](https://github.com/scythe-suite/tristo-mietitore), [sim-fun-i](https://github.com/scythe-suite/sim-fun-i),
[scythe-viewer](https://github.com/scythe-suite/scythe-viewer),  and [md2html](https://github.com/scythe-suite/md2html).

Now you need to setup your local configurations; unzip `confs.zip` in the *base
dir*, go in the newly created `confs` dir and copy `confs.sh-template` to
`confs.sh`, then edit the first lines of such file

    export DEFAULT_TEACHER_ID="<YOUR_NAME_HERE>"
    export REMOTE_USER="<REMOTE_USER_HERE>"
    export REMOTE_HOST="<REMOTE_HOST_HERE>"
    export SCYTHE_USE_SANDBOX="<NOT_NULL_IF_DOCKER_IS_AVAILABLE>"

to reflect your username, the credentials for the deploy site and whether to use
[Docker](https://www.docker.com/) as a sandbox for running the tests.

Finally unzip `exercises.zip` in the *base dir*, this is just an example set of
exercises, matching the example configuration in `confs`.

## A simple test

The unzipped example configuration and exercises should allow a simple test: run

    source ./setenv.sh
    scythe prepare example

this should generate `./confs/example.py`, the configuration file required for
all the next steps.

## Save your work!

If you want to edit and keep track of your configuration and exercises you are
suggested to turn `confs` and `exercises` into git repositories (after removing
the example exam configuration and exercises).
