{ pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/197ddbced2ae72efbef0f5f8838a7ad3fbd986eb.tar.gz") {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python38Full
    python38Packages.pip
    python38Packages.virtualenv
    python38Packages.poetry
    python38Packages.pylint
    python38Packages.pytest
    postgresql_12
    dhall
    dhall-json
  ];

  shellHook = ''
  export PGHOST=$HOME/postgres
  export PGDATA=$PGHOST/data
  export PGDATABASE=postgres
  export PGLOG=$PGHOST/postgres.log

  mkdir -p $PGHOST

  if [ ! -d $PGDATA ]; then
    initdb --auth=trust --no-locale --encoding=UTF8
  fi

  if ! pg_ctl status
  then
    pg_ctl start -l $PGLOG -o "--unix_socket_directories='$PGHOST'"
  fi

  poetry config virtualenvs.in-project true
  poetry env use python3.8
  poetry install
  echo "Starting app now"
  poetry run uvicorn app.main:app --reload

'';
}
