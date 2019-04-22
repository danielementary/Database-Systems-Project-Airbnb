# DBS-Project

## Dependencies
### Git LFS (to clone repository)
https://git-lfs.github.com/

### MySQL
#### Configuration
- Install mysql-server
- Run mysql-server as root with `sudo mysql -u root`
- Create a new user with `GRANT ALL PRIVILEGES ON *.* TO 'Group32'@'localhost' IDENTIFIED BY '1234';` in mysql-server shell

#### Commands
- Start : `sudo service mysql start`
- Stop : `sudo service mysql stop`
- Status : `sudo service mysql status`

### Python MySQL (with Python 3.7)
#### Installation
`python -m pip install mysql-connector`

#### Tutorial
https://www.w3schools.com/python/python_mysql_getstarted.asp

## Interface
- Start server with `sudo service mysql start`
- Make sure user `Group32` with password `1234` has all privileges
- Launch app with `python3 main.py` in `Interface/`
