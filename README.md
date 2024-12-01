<div id="header" align="center">
    <div>
        <img src="https://media4.giphy.com/media/gjrYDwbjnK8x36xZIO/giphy.gif?cid=ecf05e476ht8f5g4s8rz6uaiu8lfpmhkz0u3wgd4dro098xo&ep=v1_gifs_related&rid=giphy.gif&ct=s" width="100">
        <h1 align="center">
            <b>CoverDanceBot</b>
        </h1>
        <div>Bot on aiogram to search for practice videos by category</div>
    </div>
</div>

<div align="center">

### 🛠️ Used languages and tools

<div>
    <img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/python/python-original-wordmark.svg" width="80" height="80">&nbsp;
    <img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/sqlalchemy/sqlalchemy-original-wordmark.svg" width="80" height="80">&nbsp;
    <img src="https://avatars.githubusercontent.com/u/33784865?s=200&v=4" width="80" height="80">&nbsp;
    <img src="https://raw.githubusercontent.com/devicons/devicon/ca28c779441053191ff11710fe24a9e6c23690d6/icons/postgresql/postgresql-original-wordmark.svg" width="80" height="80">&nbsp;
    <img src="https://raw.githubusercontent.com/devicons/devicon/ca28c779441053191ff11710fe24a9e6c23690d6/icons/docker/docker-original-wordmark.svg" width="80" height="80">&nbsp;
    <img src="https://raw.githubusercontent.com/devicons/devicon/ca28c779441053191ff11710fe24a9e6c23690d6/icons/redis/redis-original-wordmark.svg" width="80" height="80">&nbsp;
</div>

</div>

---

## Launching the project in dev-mode

### Set up and activate the virtual environment

 ```bash
python -m venv venv
source venv/bin/activate
```

In Windows, the activation command will be different:

```bat
venv\Scripts\activate
```

### Establish dependencies

* For development, install dependencies from the requirements/dev.txt file

    ```shell
    pip install -r requirements/dev.txt
    ```

* For production, install the dependencies from the requirements/prod.txt file

    ```shell
    pip install -r requirements/prod.txt
    ```

### Create an ".env" file in the root folder

```bash
cp .env.example .env
```

In Windows, the copy command will be different:

```bat
copy .env.example .env
```

Enter the environment variables in the .env file

### Launch redis and posgres

```bash
docker compose up -d redis postgres
```

### Go to the project folder

```bash
cd bot
```

### Apply migrations

```bash
alembic upgrade head
```

### Run the project

```bash
python .
```
