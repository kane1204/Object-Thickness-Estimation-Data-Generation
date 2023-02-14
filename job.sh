#!/bin/sh

export PYVISTA_OFF_SCREEN=true
export PYVISTA_USE_PANEL=true
export PYVISTA_VIRTUAL_DISPLAY=true
python test_job.py
