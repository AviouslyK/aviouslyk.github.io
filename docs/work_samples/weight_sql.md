# Creating a SQL server, and database using Python, Docker, and Azure Data Studio


This was a personal project I embarked on to get more familiar with SQL. For a long time I've been tracking my weight on Excel . In this project I would like to set up a server, create a database, and then transfer all the information on my weight I've collected to that database - using SQL and Python.

## Install a SQL server 
Because I'm on a macOS I can't natively support Microsoft programs, I need to download and install Docker (https://www.docker.com) first.
Next I'll install Azure Data Studio (https://azure.microsoft.com/en-us/products/data-studio) to manage the server. 

Now that all the prequisistes are out of the way, let's being. We first use Docker to pull a Microsoft hosted Docker image azure-sql-edge. So in the terminal execute

```bash
docker pull mcr.microsoft.com/azure-sql-edge
```

Then to start running the server

```bash
docker run -d —-name MySQLServer -e ‘ACCEPT_EULA=Y’ -e ‘SA_PASSWORD=your_password123’ -p 1433:1433 mcr.microsoft.com/azure-sql-edge
```
