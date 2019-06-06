if [ ! -f ./secretkey.txt ]; then
    python3 docker/scripts/generate_secret_key.py >> secretkey.txt
fi