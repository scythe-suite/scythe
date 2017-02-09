# How to use the tool

## Prepare the configuration

Firt of all, design a few exercises and put them in the `exercises` dir.

Then a name for your exam, say `myexam`, then add

    ./confs/myexam.txt
    ./confs/myexam.tsv

* the first file must contain a *secret* followed by a list of exercise
  names, that is, names of directories under `exercises`;

* the second file must cotain a tab-separated list of *unique id*,
  and *last and first name* (exactly one tab per line, after the ids).

Give a look to the example unpacked in the previous step in case of doubt.

To prepare the configuartion file, just run

    source ./setenv.sh
    scythe prepare myexam

that will generate `./confs/myexam.py`, the configuration file required for all
the next steps.

## Run the exam

Now you can push the configuration to the remote server and start it with

    scythe push myexam
    scythe start myexam

at the end of the allowd time,

    scythe stop myexam

will stop the server (so that no student will be able to upload after the exam
deadline).

During the exam you can run

    scythe logtail myexam

to peek at server logs.

## Collect the student's work and evaluate it

During the exam, or at the end of it, run

    scythe get myexam

to copy the students uploads locally (under a suitable subdir of the `harvests`
dir); once you have a local copy of the uploads, you can run the test with

    scythe test myexam

and view the results with

    scythe view myexam

You can run these steps as many times as you want during the exam.
