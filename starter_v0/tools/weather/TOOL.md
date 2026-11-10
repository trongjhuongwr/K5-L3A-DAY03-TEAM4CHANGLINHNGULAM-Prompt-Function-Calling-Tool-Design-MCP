---
name: weather
track: bonus
kind: live_api
provider: Open-Meteo
requires_env: []
inputs: [city]
outputs: [tool, city, temperature_c, condition, humidity, status]
side_effect: false
---
# weather

Tra cứu thời tiết hiện tại và điều kiện khí hậu của một thành phố hoặc địa điểm trên thế giới.
