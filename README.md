# fastapi-todo-app

## Usage
```python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
docker run -e POSTGRES_PASSWORD=admin -p 5432:5432 -d postgres
uvicorn app.main:app --reload --port 8080
```

## Run
```
npm install
npm run dev
```

## Frontend
[click](https://github.com/makedonsky-it/todo-app-frontend)
