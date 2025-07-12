# Backend-Steam-Magic-Hat

A simple Django REST Framework API to track Steam users and their game libraries.

## Features

- Add Steam users by `steam_id`
- Fetch user profiles automatically from Steam API
- Track which games users own
- Basic CRUD operations via REST endpoints

## Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/fredfiesta/backend-steam-magic-hat.git
   cd backend-steam-magic-hat
   ```

2. Set up environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
   pip install -r requirements.txt
   ```

3. Add your Steam API key to `.env`:
   ```ini
   STEAM_API_KEY=your_key_here
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

- `GET /api/users/` - List all Steam users
- `POST /api/users/` - Add new user (requires `steam_id`)
- `GET /api/games/` - List all tracked games
- `GET /api/ownedgames/` - List all game ownerships
- `POST /api/ownedgames/` - Link user to game (requires `steam_id` and `app_id`)

## Requirements

- Python 3.8+
- Django 4.0+
- DRF 3.14+
- Steam API key
