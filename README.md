# People Tracking System

A real-time system for detecting and counting people using computer vision with YOLO11 and DeepSORT tracking.

## Checklist Requirements Technical Test
- [ Done ] Database Design
- [ Done ] Video Dataset Collection
- [ Done ] Object Detection and Tracking
- [ Done ] Counting and Polygon Area Management
- [ Done ] Prediction (Forecasting)
- [ Done ] API Integration for Configuration and Monitoring
- [ Done ] Deployment

## 🎯 Main Features

- **Real-time Detection**: Detect people using YOLO11
- **Object Tracking**: Multi-object tracking with DeepSORT
- **Area-based Counting**: Count people entering/exiting polygon areas
- **REST API**: Configuration and monitoring via API
- **Dynamic Configuration**: Update detection areas in real-time

## 🗄️ Database Design

### ERD (Entity Relationship Diagram)

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     AREAS       │    │   DETECTIONS    │    │    COUNTERS     │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ id (UUID) PK    │◄──┐│ id (BIGINT) PK  │    │ id (BIGINT) PK  │
│ name (VARCHAR)  │   ││ tracking_id     │    │ area_id (UUID)  │◄─┐
│ coordinates*    │   ││ area_id (UUID)  │────┘│ in_count (INT)  │  │
│ polygon (JSON)  │   ││ frame_time      │     │ out_count (INT) │  │
│ created_at      │   ││ bbox (JSON)     │     │ updated_at      │  │
│ updated_at      │   ││ entered (BOOL)  │     └─────────────────┘  │
└─────────────────┘   ││ created_at      │                        │
                      │└─────────────────┘                        │
                      └───────────────────────────────────────────┘

Relationships:
- AREAS (1) ←→ (N) DETECTIONS (area_id)
- AREAS (1) ←→ (1) COUNTERS (area_id)
```

### Database Schema

```sql
-- Table: areas (Definisi area deteksi)
CREATE TABLE areas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR NOT NULL,
    coordinates JSON NOT NULL,  -- Legacy field
    polygon JSON,               -- Koordinat polygon area
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Table: detections (Record setiap deteksi)
CREATE TABLE detections (
    id BIGSERIAL PRIMARY KEY,
    tracking_id VARCHAR NOT NULL,
    area_id UUID REFERENCES areas(id) ON DELETE CASCADE,
    frame_time TIMESTAMP WITH TIME ZONE NOT NULL,
    bbox JSON NOT NULL,         -- Bounding box {x, y, w, h}
    entered BOOLEAN NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table: counters (Agregasi counting per area)
CREATE TABLE counters (
    id BIGSERIAL PRIMARY KEY,
    area_id UUID REFERENCES areas(id) ON DELETE CASCADE UNIQUE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    in_count INTEGER DEFAULT 0,
    out_count INTEGER DEFAULT 0
);
```

## 🎥 Dataset Video

### Dataset Open-Source

**Rekomendasi dataset untuk testing:**

1. **Pedestrian Video Dataset Kaggle**
   - Multiple Object Tracking benchmark
   - Download: https://www.kaggle.com/datasets/dsptlp/pedestrians-videos
   - Format: MP4, annotations tersedia


### Video Source Configuration

```bash
# File video statis
VIDEO_SOURCE_TYPE=static
VIDEO_SOURCE_PATH=data/videos/test-1.mp4

```

## 🤖 Worker Detector

### Arsitektur Detection Pipeline

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Video Input │───►│ YOLO11      │───►│ DeepSORT    │───►│ Polygon     │
│             │    │ Detection   │    │ Tracking    │    │ Check       │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                           │                  │                  │
                           ▼                  ▼                  ▼
                   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
                   │ Person      │    │ Track ID    │    │ Count       │
                   │ Detection   │    │ Assignment  │    │ Update      │
                   └─────────────┘    └─────────────┘    └─────────────┘
```

### Core Components

1. **YOLO11 Detection**
   ```python
   model = YOLO("yolo11n.pt")
   results = model(frame, verbose=False)[0]
   
   # Filter person class (class_id = 0)
   for box in results.boxes:
       if int(box.cls[0]) == 0:  # person
           detections.append(([x1, y1, w, h], confidence, "person"))
   ```

2. **DeepSORT Tracking**
   ```python
   tracker = DeepSort(max_age=30, n_init=3, max_cosine_distance=0.2)
   tracks = tracker.update_tracks(detections, frame=frame)
   ```

3. **Polygon Area Detection**
   ```python
   inside = is_inside_polygon(polygon_area, (center_x, center_y))
   if inside and track_not_seen_before:
       counter.in_count += 1
   ```


## 🚀 Quick Start

### 1. Installation

```bash
# Clone repository
git clone <repository-url>
cd people-tracking

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Create PostgreSQL database
sudo -u postgres createdb people_tracking

# Configure environment
cp .env.example .env
# Edit DATABASE_URL in .env

# Run migrations
alembic upgrade head
```

### 3. Setup Initial Area

```bash
# Create default detection areas
python scripts/setup_initial.py
```

### 4. Running API Server

```bash
# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# API Documentation
http://localhost:8000/docs
```

### 5. Running Detection Pipeline

```bash
# Start people detection
python scripts/run_pipeline.py

# Press 'q' to quit
```

## 🔧 API Endpoints

### Setup Detection Area

```bash
POST /api/config/area
Content-Type: application/json

{
  "name": "Main Entrance",
  "polygon": [[300, 400], [900, 400], [1000, 720], [200, 720]]
}
```

### Get Statistics

```bash
GET /api/stats?area_id=<area-id>

# Response:
{
  "area_id": "uuid",
  "area_name": "Main Entrance", 
  "total_detections": 45,
  "in_count": 23,
  "out_count": 22,
  "last_updated": "2025-07-23T10:30:00Z"
}
```

## 📸 Visual Examples

### Polygon Area Configuration

Below is a visual example of how the system detects and tracks people within a configured polygon area:

#### Before: Initial Detection with Person Tracking
![Before - Person Detection](./images/people_tracking.png)

*The image illustrates the system detecting people (green bounding boxes) with tracking IDs and a blue polygon area that has been configured.*

#### After: Adjusted Polygon Area for Better Coverage  
![After - Adjusted Polygon](./images/dynamic_polygon_with_api.png)

*After adjusting the polygon area via the API, the detection area (green polygon) is expanded for better coverage.*

### Key Features Demonstrated:

1. **Real-time Person Detection**: Green bounding boxes indicate detected individuals with confidence scores.
2. **Tracking ID Assignment**: Each person is assigned a unique tracking ID (e.g., ID:5).
3. **Polygon Area Visualization**: 
    - **Blue**: Initial polygon area.
    - **Green**: Adjusted polygon area after API updates.
4. **Coordinate Display**: The bottom-left corner displays mouse coordinates and RGB values.
5. **Dynamic Area Updates**: Polygon areas can be updated in real-time without restarting the system.

### API Usage for Polygon Adjustment:

```bash
# Initial polygon setup
curl -X POST http://localhost:8000/api/config/area \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Pedestrian Crossing Area", 
    "polygon": [[300, 400], [900, 400], [1000, 720], [200, 720]]
  }'

# Adjusted polygon for better coverage
curl -X POST http://localhost:8000/api/config/area \
  -H "Content-Type: application/json" \
  -d '{
    "area_id": "existing-area-id",
    "name": "Pedestrian Crossing Area",
    "polygon": [[250, 350], [950, 350], [1050, 750], [150, 750]]
  }'
```

## 📊 Testing

### Video File Test

```bash
# Test dengan file video
python scripts/test_video.py
```

## ⚙️ Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/people_tracking

# Video Source
VIDEO_SOURCE_TYPE=static
VIDEO_SOURCE_PATH=data/videos/test-1.mp4
```

### Tuning Detection Parameters

```python
# app/workers/detector.py
tracker = DeepSort(
    max_age=30,              # Track memory (frames)
    n_init=3,                # Confirmations required
    max_cosine_distance=0.2, # Tracking sensitivity
    nn_budget=100            # Memory budget
)
```

## 🛠️ Development

### Project Structure

```
people-tracking/
├── app/
│   ├── api/v1/endpoints/     # API routes
│   ├── core/                 # Configuration & database
│   ├── models/               # SQLAlchemy models
│   ├── schemas/              # Pydantic schemas  
│   ├── services/             # Business logic
│   ├── utils/                # Utilities
│   └── workers/              # Detection worker
├── alembic/                  # Database migrations
├── data/videos/              # Test videos
├── scripts/                  # Utility scripts
└── requirements.txt
```

