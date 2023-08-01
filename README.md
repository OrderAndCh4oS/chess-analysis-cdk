# Chess Analysis CDK

## Run Docker

```sh
cd src
docker build --platform linux/amd64 -t app .                                        
docker run -p 8080:80 app
```

## Deploy

```sh
pnpm cdk:deploy
```

## Destroy

```sh
pnpm cdk:destroy
```
