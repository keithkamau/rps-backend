# Rock Paper Scissors Tournament - Backend API

A Flask-based REST API for a multiplayer Rock Paper Scissors tournament platform with WebSocket support.

## Live API

**Base URL:** `https://rps-backend-ro2g.onrender.com`

## Tech Stack

- **Framework:** Flask 3.1
- **Database:** PostgreSQL (Render)
- **WebSocket:** Flask-SocketIO
- **Auth:** JWT (PyJWT + bcrypt)
- **Rate Limiting:** Flask-Limiter
- **Deployment:** Docker + Render

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/signup` | Create new account | No |
| POST | `/api/auth/login` | Login | No |
| GET | `/api/auth/me` | Get current user | Yes |

### Tournaments

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/tournament/create` | Create tournament | Yes |
| GET | `/api/tournament/active` | Active tournaments | Yes |
| POST | `/api/tournament/<id>/join` | Join tournament | Yes |
| GET | `/api/tournament/<id>` | Tournament details | Yes |
| GET | `/api/tournament/<id>/bracket` | View bracket | Yes |

### Game

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/game/match/<id>` | Match details | Yes |
| POST | `/api/game/match/<id>/start-round` | Start a round | Yes |
| POST | `/api/game/match/<id>/round/<rid>/choice` | Submit choice | Yes |

### Spectator

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/spectator/match/<id>` | Spectate match | Yes |
| GET | `/api/spectator/active-matches` | Active matches | Yes |

### Admin / Stats

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/admin/stats` | Platform statistics | Yes |
| GET | `/api/admin/leaderboard` | Player leaderboard | Yes |
| GET | `/api/admin/tournaments` | All tournaments | Yes |

## WebSocket Events

| Event | Direction | Description |
|-------|-----------|-------------|
| `join_match` | Client → Server | Join a match room |
| `submit_choice` | Client → Server | Submit rock/paper/scissors |
| `join_tournament_room` | Client → Server | Join tournament updates |
| `spectate_match` | Client → Server | Spectate a match |
| `match_ready` | Server → Client | Both players present |
| `round_result` | Server → Client | Round winner & choices |
| `match_over` | Server → Client | Final match result |
| `next_round` | Server → Client | New round starting |
| `tournament_update` | Server → Client | Bracket updates |

## Quick Start (Local)

```bash
# Clone the repo
git clone <repo-url>
cd rock-paper-scissors-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run
python run.py

## Docker
```bash
docker build -t rps-backend .
docker run -d -p 5000:5000 --name rps-backend rps-backend
```

## Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage report
python -m pytest tests/ --cov=app -v

# Run specific test file
python -m pytest tests/test_auth.py -v
python -m pytest tests/test_game_logic.py -v
python -m pytest tests/test_tournament.py -v
python -m pytest tests/test_admin.py -v
python -m pytest tests/test_game_routes.py -v
python -m pytest tests/test_spectator.py -v
```

## Environment Variables

| Variable | Description | Default |
| DATABASE_URL | PostgreSQL connection string | sqlite:///app.db |
| SECRET_KEY | Flask secret key | - |
| JWT_SECRET_KEY | JWT signing key | - |
| FRONTEND_URL | CORS allowed origin | http://localhost:3000 |

## Example Requests

### Signup

```bash
curl -X POST https://rps-backend-ro2g.onrender.com/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"player1","email":"player@test.com","password":"Test1234"}'
```

### Login

```bash
curl -X POST https://rps-backend-ro2g.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"player1","password":"Test1234"}'
```

### Create Tournament

```bash
curl -X POST https://rps-backend-ro2g.onrender.com/api/tournament/create \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"name":"Championship"}'
```