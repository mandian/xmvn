#!/bin/bash
set -e
  
if [[ `grep -Es "%bcond_without\sbootstrap" *.spec` ]]
then
	sh ./xmvn-package-dependencies
fi

