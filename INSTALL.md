# Installation instructions

Create an empty dir that we'll be the **base dir**, download and unpack the
[last release](https://github.com/scythe-suite/scythe/releases/latest) of the
`scythe.tgz`, `exercises.tgz`, and `confs.tgz` archives; you can accomplish such
task with

    version="v0.1.5"
    release_url="https://github.com/scythe-suite/scythe/releases/download/$version/"
    curl -sL $release_url/scythe.tgz | tar zxvf -
    curl -sL $release_url/confs\.tgz | tar zxvf -
    curl -sL $release_url/exercises.tgz | tar zxvf -

Observe that it is safe to download and unpack the `scythe.tgz` archive at any
time to update the tool, since it will not overwrite any of your files.

Every time you'll need to use this tool, just go to the *base dir* and set the
required environment variables using

    source ./setpath.sh

note that if you use [direnv](https://direnv.net/) just link `setpath.sh` to
`.envrc` and direnv will take care of this step for you!

Now setup your local configurations: go in the newly created `confs` dir and
move `confs.sh-template` to `confs.sh`, then edit the first lines of such file

    export DEFAULT_TEACHER_ID="<YOUR_NAME_HERE>"
    export REMOTE_USER="<REMOTE_USER_HERE>"
    export REMOTE_HOST="<REMOTE_HOST_HERE>"
    export SCYTHE_USE_SANDBOX="<NOT_NULL_IF_DOCKER_IS_AVAILABLE>"

to reflect your username, the credentials for the deploy site and whether to use
[Docker](https://www.docker.com/) as a sandbox for running the tests.

You are ready to install the various dependencies (this must be done the first
time you use the tool, or when an update of any of the dependencies is issued):
simply run

    scythe init

this will download the latest releases of
[tristo-mietitore](https://github.com/scythe-suite/tristo-mietitore),
[sim-fun-i](https://github.com/scythe-suite/sim-fun-i),
[scythe-viewer](https://github.com/scythe-suite/scythe-viewer),  and
[md2html](https://github.com/scythe-suite/md2html).

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
