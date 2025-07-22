# People-Tracking

Real-time people detection and tracking system using YOLO and DeepSORT with dynamic polygon configuration.

## Features

- Real-time people detection using YOLOv11
- Object tracking with DeepSORT
- Dynamic polygon area configuration via API
- Auto-refresh polygon from database
- RESTful API for configuration and statistics
- Containerized deployment with Docker

## Quick Start with Docker

### Prerequisites

- Docker and Docker Compose
- Git

### 1. Clone and Setup

```bash
git clone <repository-url>
cd people-tracking
cp .env.example .env
```

### 2. Build and Start Services

```bash
# Build Docker images
make build

# Start API and database
make up

# Run migrations and setup initial areas
make setup
```

### 3. Run Video Pipeline

```bash
# For video file processing
make pipeline

# For live webcam (optional)
make live
```

### 4. Access Services

- **API Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/
- **PostgreSQL**: localhost:5432

## Available Commands

```bash
make help          # Show all available commands
make build         # Build Docker images
make up            # Start API and database services
make pipeline      # Start video pipeline service
make live          # Start live video pipeline service
make migrate       # Run database migrations
make setup         # Setup initial database and area configuration
make logs          # Show logs from all services
make down          # Stop all services
make clean         # Clean up containers and volumes
make dev           # Development mode with auto-reload
```

## API Endpoints

### Configure Detection Area

**POST** `/api/config/area`

```json
{
    "area_id": "4aeb238c-be39-4c1b-8c9f-828669dddf62",
    "name": "Pedestrian Crossing Area",
    "polygon": [[300, 400], [900, 400], [1000, 720], [200, 720]]
}
```

Or create with auto-generated ID:

```json
{
    "name": "New Crossing Area",
    "polygon": [[300, 400], [900, 400], [1000, 720], [200, 720]]
}
```

### Get Statistics

**GET** `/api/stats/` - Historical data
**GET** `/api/stats/live` - Live counters

## Development

### Local Development (without Docker)

```bash
# Install dependencies
uv sync

# Setup environment
cp .env.example .env

# Run migrations
uv run alembic upgrade head

# Setup initial areas
uv run python scripts/setup_initial.py

# Start API
uv run uvicorn app.main:app --reload

# Run video pipeline
uv run python scripts/run_pipeline.py
```

### Project Structure

```
├── app/
│   ├── api/v1/endpoints/     # API endpoints
│   ├── core/                 # Core configuration
│   ├── models/               # Database models
│   ├── schemas/              # Pydantic schemas
│   ├── services/             # Business logic services
│   ├── utils/                # Utility functions
│   └── workers/              # Background workers
├── alembic/                  # Database migrations
├── data/videos/              # Video files
├── scripts/                  # Utility scripts
└── docker-compose.yml        # Container orchestration
```

## Configuration

### Environment Variables

Create `.env` file from `.env.example`:

```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/people_tracking
VIDEO_SOURCE=data/videos/test-1.mp4  # or 0 for webcam
YOLO_MODEL=yolo11n.pt
REFRESH_INTERVAL=10
```

### Dynamic Area Configuration

Areas can be configured dynamically via:

1. **API**: POST to `/api/config/area`
2. **Database**: Direct insertion to `areas` table
3. **Startup Script**: Modify `scripts/setup_initial.py`

The detection pipeline automatically refreshes polygon configurations every 10 seconds without requiring restart.

## Troubleshooting

### X11 Display Issues (Linux)

```bash
# Allow Docker to access X11
xhost +local:docker

# Or set DISPLAY environment variable
export DISPLAY=:0
```

### Camera Access Issues

```bash
# Check camera permissions
ls -la /dev/video*

# Add user to video group
sudo usermod -a -G video $USER
```

### Database Connection Issues

```bash
# Check PostgreSQL logs
make logs-db

# Reset database
make clean
make up
make setup
```

## License

[Add your license information here]