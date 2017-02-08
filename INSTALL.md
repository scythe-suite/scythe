# Installation instructions

First of all clone this repo with

    https://github.com/mapio/scythe

Now set the path and install the required dependencies

    . ./setpath.sh
    scythe init

this will download the latest releases of `tristo-mietitore`, `sim-fun-i`,
`scythe-viewer` and `md2html`.

Now you need to setup configurations; you can start from an example repo

    git clone https://github.com/mapio/scythe-confs-labprog confs

Now edit `confs/confs.sh` replacing `santini` with your name in line

    DEFAULT_TEACHER_ID="santini"

Note that if you want to keep track of your conigurations in a repo, you'll need
to change the remote (you will not be allowed to push to `mapio/scythe-confs-labprog`).

Make a directory named `./dirs` and add a subdirectory named `./dirs/exercises`
containing exercises, for instance, cloning

    cd ./dirs
    git clone git@github.com:mapio/labprog-infomus-esercizi.git exercises

It should be all set now. Again, if you want to edit and keep track of your exercises
you'll need to change the remote (you will not be allowed to push to `mapio/labprog-infomus-esercizi` either).

## Use

Choose an id for your exam, say `test_exam`, to prepare an exam just add

    ./confs/test_exam.txt
    ./confs/test_exam.tsv

the first file should contain a *secret* followed by a list of exercise names, the second file should cotain a tab-separated list of *matricola*, *cognome nome* (one tab per line).

To prepare the configuartion file, just run

    . ./setpath.sh
    scythe prepare test_exam

that will generate `./confs/test_exam.py`, the required configuration file.
