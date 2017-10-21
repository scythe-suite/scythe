walkup() {
    target=$1
    cur=$(pwd -P)
    while [ ! -z $cur ] && [ ! -r "$cur/$target" ]; do
        cur=${cur%/*}
    done
    echo "$cur/$target"
}
export -f walkup
