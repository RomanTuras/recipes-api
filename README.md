# Recipes API

`source $(poetry env info --path)/bin/activate`

`python entry.py`

`docker build --no-cache . -t mac4r/recipes-api`

`docker container run -dp 80:80 -t mac4r/recipes-api:latest`

