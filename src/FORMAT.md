 SET	uids:<SESSION_ID> -> JSON({uid : <UID>, info : <INFO>, status: <STATUS>})
HASH	texts:<SESSION_ID> -> <EXERCISE_NAME>: JSON({name: <TEXT_NAME>, text: <MARKDOWN_TEXT>})
HASH	cases:<SESSION_ID> -> <EXERCISE_NAME>: JSON([{name: <CASE_NAME>, args: <ARGS>, input: <INPUT>, expected: <EXPECTED>}+])

ZSET	timestamps:<SESSION_ID>:<UID> -> TIMESTAMP

HASH	solutions:<UID>:<TIMESTAMP> -> <EXERCISE_NAME>: JSON([{content: <SOURCE_CODE>, name: <FILE_NAME>}+])
HASH	results:<UID>:<TIMESTAMP> -> <EXERCISE_NAME>: JSON([{name: <CASE_NAME>, diffs: <ARGS>, errors: <INPUT>}+])
HASH	compilations:<UID>:<TIMESTAMP> -> <EXERCISE_NAME>: <COMPILER_OUTPUT>

HASH	summary:<SESSION_ID> -> <UID>: JSON([{name: <EXERCISE_NAME>, compile: <BOOLEAN>: diffs: <NUM_DIFFS>, errors: <NUM_ERRORS>, …}+])
