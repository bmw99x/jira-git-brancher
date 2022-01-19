# Remove BRANCHES_CREATED.txt at startup to purge old usages of the git brancher
: > BRANCHES_CREATED.txt
SCRIPT_DIR=$(pwd)
echo "Git brancher running..."

function git_brancher() {
    # If the branch exists, dont do the checkout -b etc.
    echo "Checking for new tickets started..."
    OUTPUT=$(python3 git_brancher.py)
    BRANCH=$(echo $OUTPUT | cut -d'|' -f 1)
    DIR=$(echo $OUTPUT | cut -d'|' -f 2 )
    # If the branch and directory are non-empty, proceed
    echo $BRANCH
    if [ "${BRANCH}" ] && [ "${DIR}" ]; then
        echo "New branch created: ${BRANCH} with VS Directory: ${DIR}"
        # Checkout the git branch, suppresing the output, then open vscode in that directory
        cd $DIR 
        git checkout $BRANCH 2>/dev/null || git checkout -b $BRANCH 
        code .
    fi
    # Go back to the original working directory
    cd $SCRIPT_DIR
}

while true; do git_brancher; sleep 10; done