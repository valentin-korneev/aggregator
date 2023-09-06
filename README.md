# Платежный агрегатор

Windows (PowerShell)
```bash
Set-ExecutionPolicy RemoteSigned
```bash

```bash
python -m venv .venv
./.venv/Scripts/Activate.ps1
```

# Install 1
```bash
pip install -r requirements.txt
```

# Install 2
```bash
pip install fastapi
pip install uvicorn[standard]
pip install databases[postgresql]
pip install python-jose[cryptography]
pip install passlib[bcrypt]
pip install python-multipart
```

# Refresh requirements.txt
```bash
pip freeze > requirements.txt
```

# Install DB (Windows)
```bash
./database/_install.cmd
```

# Работа с docker
```bash
docker build -t aggregator_image .
docker run -d --name aggregator_container -p 80:80 -p 5432:5432 aggregator_image
```

# Работа с docker-compose
```bash
docker-compose build
docker-compose up -d
```

После выполнения можно запустить инициализацию БД
