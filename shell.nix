{ pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/197ddbced2ae72efbef0f5f8838a7ad3fbd986eb.tar.gz") {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python38Full
    pkgs.python38Packages.pip
    pkgs.python38Packages.virtualenv
    pkgs.python38Packages.poetry
    pkgs.python38Packages.pylint
    pkgs.postgresql_12
    
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
