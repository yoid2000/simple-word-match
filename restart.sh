#!/bin/bash

sudo systemctl stop simple-word-match
sudo systemctl daemon-reload
sudo systemctl start simple-word-match
sudo systemctl enable simple-word-match