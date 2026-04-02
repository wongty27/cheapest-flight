# Cheapest Flight
A simple Rest API built with FastAPI to calculate cheapest flight price.

Source code: https://github.com/wongty27/cheapest-flight

Web: https://cheapest-flight-qarp.onrender.com/docs

Demo: https://drive.google.com/file/d/1YO6TZ2hITRuxIH4dBITBD3PTTO4VKCu8/view?usp=sharing

## JSON File Example
```json
{
  "n": 3,
  "flights": [
    {"src": 0, "dst": 1, "price": 100},
    {"src": 1, "dst": 2, "price": 100},
    {"src": 0, "dst": 2, "price": 500}
  ]
}
```