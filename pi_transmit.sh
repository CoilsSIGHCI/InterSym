#!/bin/bash

# SSH credentials and server details
SSH_USER="uw"
SSH_HOST="uw.local"
SSH_PORT="22"

# Local and remote paths
LOCAL_PATH="."
# shellcheck disable=SC2088
REMOTE_PATH='~/InterSym'

# Make intermediate directories if they don't exist on the remote server
ssh -p $SSH_PORT $SSH_USER@$SSH_HOST "mkdir -p $REMOTE_PATH"

# Rsync command for transferring the entire directory
rsync -avz -e "ssh -p $SSH_PORT" $LOCAL_PATH $SSH_USER@$SSH_HOST:$REMOTE_PATH

echo "rsync operations completed."
