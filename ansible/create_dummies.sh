#! bin/bash

mkdir ~/p0/project0/test

for i in {1..10}; do
    mkdir ~/p0/project0/test/dummy-directory$i
    for (( j = 1; j <= $(( ($RANDOM % 10) + 1)); j++ )); do
        touch ~/p0/project0/test/dummy-directory$i/dummy-file$j
    done
done