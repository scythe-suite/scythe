# How to use the tool

## Prepare the configuration

First of all, design a few exercises and put them in the `exercises` dir.

Then choose a name for your exam (the name must contain just *alphanumeric and
underscore* characters), say `myexam`, and add

    ./confs/myexam.txt
    ./confs/myexam.tsv

* the first file must contain, on the first line, a *secret* followed by a list
  of exercise names (one exercise per line), that is, names of directories in
  the `exercises` folder;

* the second file must contain a tab-separated list of *unique ids*,
  and *last and first name* (exactly one tab per line, after the ids).

Give a look to the example unpacked during the installation in case of doubt.

To prepare the configuration file, just run

    source ./setenv.sh
    scythe prepare myexam

that will generate `./confs/myexam.py`: the configuration file required for all
the next steps.

### The basic bundle

The `confs/basebunlde` directory contains a set of file that will be included in
all the exam configurations (alongside the exercises and test cases); for
example it can contain a README to help students during the exam and a set of
simplified commands to test and upload their solutions.

The `confs.tgz` contains a basic bundle for Java (and Shell) programming exams
with an Italian README and a few support commands that can be a reasonable
starting point for your own basic bundle.

## Run the exam

Now you can push the configuration to the remote server and start it with

    scythe push myexam
    scythe start myexam

At the end of the allowed time,

    scythe stop myexam

will stop the server (so that no student will be able to upload his solution
after the exam deadline).

During the exam you can run

    scythe logtail myexam

to peek at server logs.

## Collect the student's work and evaluate it

During the exam, or at the end of it, run

    scythe get myexam

to copy the students uploads locally (under a suitable subdirectory of the
`harvests` dir); once you have a local copy of the uploads, you can run the test
with

    scythe test myexam

and view the results with

    scythe view myexam

You can run these steps as many times as you want during the exam. The `test`
subcommand supports two options:

* `-c` to force a cleanup of previously compiled and executed tests,

* `-r <UIDS_FILE>.tsv` to restrict the evaluation to a subset of UIDs (the given
  file must have the same tab-separated format of the UIDs file used to prepare
  the exam configuration).
