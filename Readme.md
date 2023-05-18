# Custom StockFinder ClearURL

This repository uses https://github.com/AmanoTeam/Unalix to clean up the URLs.
The idea is clean up the urls and add a custom referal

## Docker Deploy

You must load to the container's environment the Token and Channel

## Kubernetes Deploy

You must create two Secrets: Token and Channel

kubectl create secret generic nvidia-telegram-token --from-literal=telegram-token=TOKEN --save-config
kubectl create secret generic nvidia-telegram-channel --from-literal=telegram-channel=CHANNEL --save-config