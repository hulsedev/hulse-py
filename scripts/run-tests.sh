# read environment variables from file if available
if [ -f ".env" ]; then
    export $(cat .env | xargs)
fi

pytest tests/* -x --full-trace
