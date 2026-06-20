#!/bin/bash

curl --request POST \
  --url 'http://127.0.0.1:8000/fruits?=' \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/12.5.0' \
  --data '{"id" : 1,"name" : "apple","description" : "yummy","price" : 0.69}'

curl --request POST \
  --url 'http://127.0.0.1:8000/fruits?=' \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/12.5.0' \
  --data '{"id" : 2,"name" : "pear","description" : "juicy","price" : 1.10}'

curl --request POST \
  --url 'http://127.0.0.1:8000/fruits?=' \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/12.5.0' \
  --data '{"id" : 3,"name" : "banana","description" : "sweet","price" : 0.42}'

curl --request POST \
  --url 'http://127.0.0.1:8000/fruits' \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/12.5.0' \
  --data '{"id" : 4,"name" : "strawberry","description" : "sweet and red","price" : 2.50}'

curl --request POST \
  --url 'http://127.0.0.1:8000/fruits' \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/12.5.0' \
  --data '{"id" : 5,"name" : "blueberry","description" : "small antioxidant bomb","price" : 3.20}'

curl --request POST \
  --url 'http://127.0.0.1:8000/fruits' \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/12.5.0' \
  --data '{"id" : 6,"name" : "orange","description" : "fresh and full of vitamin c","price" : 0.85}'

curl --request POST \
  --url 'http://127.0.0.1:8000/fruits' \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/12.5.0' \
  --data '{"id" : 7,"name" : "mango","description" : "exotic and very tropical","price" : 1.99}'

curl --request POST \
  --url 'http://127.0.0.1:8000/fruits' \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/12.5.0' \
  --data '{"id" : 8,"name" : "watermelon","description" : "perfect for hot summer days","price" : 4.50}'

curl --request POST \
  --url 'http://127.0.0.1:8000/fruits' \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/12.5.0' \
  --data '{"id" : 9,"name" : "kiwi","description" : "hairy outside sour inside","price" : 0.55}'

curl --request POST \
  --url 'http://127.0.0.1:8000/fruits' \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/12.5.0' \
  --data '{"id" : 10,"name" : "pineapple","description" : "spiky king of fruits","price" : 2.79}'

curl --request POST \
  --url 'http://127.0.0.1:8000/fruits' \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/12.5.0' \
  --data '{"id" : 11,"name" : "cherry","description" : "double the fun","price" : 3.99}'

curl --request POST \
  --url 'http://127.0.0.1:8000/fruits' \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/12.5.0' \
  --data '{"id" : 12,"name" : "peach","description" : "soft and velvety skin","price" : 1.25}'

curl --request POST \
  --url 'http://127.0.0.1:8000/fruits' \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/12.5.0' \
  --data '{"id" : 13,"name" : "lemon","description" : "extremely sour but refreshing","price" : 0.40}'