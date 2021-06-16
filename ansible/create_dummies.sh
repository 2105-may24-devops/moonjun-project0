#! bin/bash

if [ ! -d "~/p0/project0/test" ]; then
    mkdir ~/p0/project0/test
else
    rm -rf ~/p0/project0/test
    mkdir ~/p0/project0/test
fi

for i in {1..10}; do
    mkdir ~/p0/project0/test/dummy-directory$i
    for (( j = 1; j <= 5; j++ )); do
        touch ~/p0/project0/test/dummy-directory$i/dummy-file$j
    done
done


mkdir ~/p0/project0/deletion


cp ~/p0/project0/ansible/test_delete.txt ~/p0/project0/deletion
mv ~/p0/project0/ansible/test_delete.txt ~/p0/project0/deletion/files-to-delete.txt