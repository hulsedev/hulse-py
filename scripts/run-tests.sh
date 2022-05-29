export $(cat .env | xargs)

pytest tests/* -x --full-trace
