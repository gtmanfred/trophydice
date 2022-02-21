#!/bin/bash
set -e

# set PYENV_VERSION
export PYENV_VERSION="${PYENV_VERSION:-3.9.10}"

usage="$(basename "$0") [-h] [-t VERSION] -- setup pyenv and install python version
where:
    -t VERSION  specify which python version to install
    -h          show this help text"

while getopts "ht:" opt; do
    case $opt in
        t) export PYENV_VERSION=$OPTARG
           ;;
        h) echo "$usage"
           exit
           ;;
        :) printf "missing argument for -%s\n" "$OPTARG" >&2
           echo "$usage" >&2
           exit 1
           ;;
        ?) printf "illegal option: -%s\n" "$OPTARG" >&2
           echo "$usage" >&2
           exit 1
           ;;
    esac
done

# Install dependencies
apt update
apt install -y git gcc libreadline-dev libbz2-dev zlib1g-dev libssl-dev libsqlite3-dev make libffi-dev curl
apt -y autoremove
apt autoclean

# install pyenv
if [ ! -d /usr/local/pyenv ]; then
	mkdir -p /usr/local/pyenv
	git clone git://github.com/yyuu/pyenv.git /usr/local/pyenv/
	git clone git://github.com/jawshooah/pyenv-default-packages.git /usr/local/pyenv/plugins/pyenv-default-packages
	git clone git://github.com/pyenv/pyenv-pip-rehash.git /usr/local/pyenv/plugins/pyenv-pip-rehash
	ln -vs /usr/local/pyenv/bin/* /usr/local/pyenv/plugins/*/bin/* /usr/local/bin
	tee /usr/local/pyenv/default-packages <<EOF
poetry>=1.0,<2
EOF
fi

# install python
pyenv install "${PYENV_VERSION}"
