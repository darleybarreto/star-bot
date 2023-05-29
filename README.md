### Installation instructions

You will need either `podman` or `docker` to build an image from the `dockerfile` in the root of the repo.
```bash
podman build -t scraper -f dockerfile
```

```bash
docker build -t scraper -f dockerfile .
```

### How to run

You need to pass the team name as argument to the `run` command:

```bash
podman run --rm scraper:latest TeamName
```

For instance,

```bash
podman run --rm scraper:latest Cruzeiro
```

```bash
docker run --rm scraper:latest Cruzeiro
```