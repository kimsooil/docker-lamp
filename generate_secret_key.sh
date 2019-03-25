if [ ! -f ./secretkey.txt ]; then
    python3 ./generate_secret_key.py >> secretkey.txt
fi