# 🍽️ Restaurant Reservation API

A production-ready RESTful API for managing restaurant reservations, built with Django REST Framework.

![Django](https://img.shields.io/badge/Django-4.2-green)
![DRF](https://img.shields.io/badge/DRF-3.14-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Docker](https://img.shields.io/badge/Docker-ready-blue)

## Features

- JWT Authentication (register, login, logout)
- Role-based access control (Customer, Owner, Admin)
- Restaurant & table management
- Reservation conflict detection
- Filtering, searching, pagination
- Swagger / OpenAPI documentation
- Dockerized with PostgreSQL

## Tech Stack

| Technology | Version |
|---|---|
| Python | 3.11 |
| Django | 4.2 |
| Django REST Framework | 3.14 |
| PostgreSQL | 15 |
| Docker & Docker Compose | latest |
| JWT | SimpleJWT |

## Quick Start (Docker)

```bash
git clone https://github.com/orifrustamovich/restaurant-reservation-api

cd restaurant-reservation-api

cp .env.example .env    # configure file .env

docker compose up --build
```
