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

that will generate `./confs/myexam-st.py` and `./confs/myexam-tm.py`: the
configuration files required for all the next steps.

### The "base bundle"

The `confs/basebunlde` directory contains a set of file that will be included in
all the exam configurations (alongside the exercises and test cases); for
example it can contain a `README` to help students during the exam and a set of
simplified commands to test and upload their solutions.

The `confs.tgz` contains a basic bundle for Java (and Shell) programming exams
with an Italian `README` (named `LEGGIMI.md`) and a few support commands that
can be a reasonable starting point for your own basic bundle.

## Run the exam

Now you can push the configuration to the remote server and start it with

    scythe start myexam

At the end of the allowed time,

    scythe stop myexam

will stop the server (so that no student will be able to upload his solution
after the exam deadline).

During the exam you can run

    scythe logtail myexam

to peek at server logs.

## Collect the student's work for backup purposes

During the exam, or at the end of it, run

    scythe backup myexam

to copy the students uploads locally (under a suitable subdirectory of the
`backups` dir).

## View the results

When you push your configurations, you'll be given a dashboard URL where you can
watch the real-time evaluations (with no restrictions); omitting the token (the
last part of the URL) will give you a private dashboard (where no details are
shown, not even the uid infos); on the other hand, with

    scythe auth myexam REALMS...

you'll get a token for the specified realms.
