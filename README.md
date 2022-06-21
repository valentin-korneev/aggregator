# aggregator
Платежный агрегатор

# Windows (PowerShell): Set-ExecutionPolicy RemoteSigned
python -m venv .venv
./.venv/Scripts/Activate.ps1

# Install 1
pip install -r requirements.txt

# Install 2
pip install fastapi
pip install uvicorn[standard]
pip install databases[postgresql]
pip install python-jose[cryptography]
pip install passlib[bcrypt]
pip install python-multipart

# Refresh requirements.txt
pip freeze > requirements.txt

# Install DB (Windows)
./database/_install.cmd

# Работа с docker
docker build -t aggregator_image .
docker run -d --name aggregator_container -p 80:80 -p 5432:5432 aggregator_image

# Работа с docker-compose
docker-compose build
docker-compose up -d
