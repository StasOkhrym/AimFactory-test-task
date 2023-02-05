# AimFactory Test Task
### Small REST API without DRF
Implementing REST API with JSON-based payload.

## Installing using Github
Python 3.10 and Docker must be installed

- Clone repo and set up virtual environment:
```shell
git clone https://github.com/StasOkhrym/AmiFactory-test-task.git
python -m venv venv
source venv/bin/activate (Linux and macOS) or venv\Scripts\activate (Windows)
pip install -r requirements.txt
```
- Create `.env` file using `.env_sample` 
- Build docker container for database:
```shell
docker-compose up --build
```
- Apply migrations:
```shell
python manage.py migrate
```