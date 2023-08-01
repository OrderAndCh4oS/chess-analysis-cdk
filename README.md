# Chess Analysis CDK

## Run Docker

```sh
cd src
docker build --platform linux/amd64 -t lambdas .                                        
docker run -p 8080:80 lambdas
```

## Deploy

```sh
pnpm cdk:deploy
```

## Destroy

```sh
pnpm cdk:destroy
```
