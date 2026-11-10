---
name: crypto_price
track: bonus
kind: live_api
provider: Binance
requires_env: []
inputs: [symbol, currency]
outputs: [tool, symbol, currency, price, status]
side_effect: false
---
# crypto_price

Tra cứu giá tiền mã hóa theo thời gian thực (BTC, ETH, SOL, BNB...) qua API công khai của Binance.
