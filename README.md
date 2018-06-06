# Battleship
- create a mulitpler battleship with GUI using websockets

## Run On Local Machine
1. Open up 3 terminals and navigate to Battleship
```bash
cd Desktop/Battleship
```
2. Start the server on first terminal
```bash
python3 server.py
```
3. Start the clients on other two terminals
```bash
python newClient.py
```
4. Create Boards for each client and play!

---
## Run on AWS
1. Launch an AWS instance [here](https://aws.amazon.com/getting-started/tutorials/launch-a-virtual-machine/?trk=gs_card)
2. SSH into the AWS instance
3. Git clone Battleship Repo
```
git clone git@github.com:tfrancis03/Battleship.git
```
4. cd into Battleship and run the server
```
python3 server.py
```
5. Open up `port 5000` on AWS instance in Security Groups
![Click on Security Groups](/images/aws1.jpg)
![Add Custom TCP Rule with port 5000](/images/aws1.jpg)

6. Clone Battleship on local machines
7. Change `ipAdress` in `newClient.py` to the public ip addess of AWS instance
```bash
ipAddress = 'AWS_IP_ADDRESS_HERE'
```
8. Run the client and play!
```bash
python newClient.py
```

---
#Commands
- Run Original 
`python battleship2.py`

- Run Modified
`python3 battleship.py`

- check to see what's running on port 33000
`netstat -vanp tcp | grep 5000`

- stops program from accessing port 330000
`lsof -t -i tcp:5000 | xargs kill`