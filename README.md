# Battleship
Create a networked battleship with GUI

#Commands
- Run Original 
`python battleship2.py`

- Run Modified
`python3 battleship.py`

- check to see what's running on port 33000
`netstat -vanp tcp | grep 33000`

- stops program from accessing port 330000
`lsof -t -i tcp:33000 | xargs kill`