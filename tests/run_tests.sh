#!/bin/sh

export PYTHONPATH=../

nosetests --with-coverage --cover-package=ylog --cover-inclusive \
          --cover-erase
