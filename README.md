# Slide Generator API

A powerful backend application that generates customizable presentation slides on any topic using AI-powered content generation and Python-PPTX.

## Features

### Core Functionality
- **AI-Powered Content Generation**: Leverages OpenAI's GPT models to generate relevant, engaging presentation content
- **Custom Content Support**: Accept user-provided custom content for slides
- **Multiple Slide Layouts**:
  - Title slide
  - Bullet points (3-5 points)
  - Two-column layout
  - Content with image placeholder
- **Flexible Configuration**: 1-20 slides per presentation
- **Customizable Themes**: Support for custom fonts, colors, and styling
- **Citations & References**: Automatic inclusion of source citations
- **PowerPoint Export**: Generate professional .pptx files

### Advanced Features
- **Request/Response Validation**: Comprehensive input validation using Pydantic
- **Error Handling**: Robust error handling with detailed error messages
- **Rate Limiting**: Built-in API rate limiting to prevent abuse
- **Multiple Aspect Ratios**: Support for 16:9 and 4:3 aspect ratios
- **RESTful API**: Clean, well-documented REST API endpoints
- **Async Support**: Asynchronous request handling for better performance

## Project Structure

```
powerpoint/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application
│   ├── config.py                  # Configuration settings
│   ├── models.py                  # Pydantic models
│   └── services/
│       ├── __init__.py
│       ├── content_generator.py   # AI content generation
│       └── presentation_generator.py  # PowerPoint generation
├── generated_presentations/       # Output directory
├── sample_presentations/          # Sample outputs
├── requirements.txt               # Python dependencies
├── .env.example                   # Example environment variables
└── README.md                      # This file
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- OpenAI API key (optional, for AI-powered content generation)

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd C:\Users\VICTUS\Desktop\projects\powerpoint
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the example env file
   copy .env.example .env

   # Edit .env and add your OpenAI API key (optional)
   # OPENAI_API_KEY=your_api_key_here
   ```

   **Note**: The API works without an OpenAI API key by using fallback content generation.

5. **Create output directory**
   ```bash
   mkdir generated_presentations
   mkdir sample_presentations
   ```

### Running the Application

1. **Start the server**
   ```bash
   # Using uvicorn directly
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

   # Or using Python
   python -m app.main
   ```

2. **Access the API**
   - API Base URL: `http://localhost:8000`
   - Interactive API Docs: `http://localhost:8000/docs`
   - Alternative Docs: `http://localhost:8000/redoc`

## API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00"
}
```

#### 2. Generate Presentation
```http
POST /api/v1/generate
```

**Request Body:**
```json
{
  "topic": "Artificial Intelligence in Healthcare",
  "num_slides": 8,
  "include_citations": true,
  "aspect_ratio": "16:9",
  "theme": {
    "primary_color": "#1F4788",
    "secondary_color": "#FFFFFF",
    "font_name": "Calibri",
    "font_size_title": 44,
    "font_size_body": 18
  }
}
```

**Response:**
```json
{
  "presentation_id": "550e8400-e29b-41d4-a716-446655440000",
  "topic": "Artificial Intelligence in Healthcare",
  "num_slides": 8,
  "slides": [...],
  "citations": [...],
  "file_path": "generated_presentations/550e8400-e29b-41d4-a716-446655440000.pptx",
  "generation_time_seconds": 3.45
}
```

#### 3. Download Presentation
```http
GET /api/v1/download/{presentation_id}
```

**Response:** PowerPoint file (.pptx)

#### 4. Delete Presentation
```http
DELETE /api/v1/presentations/{presentation_id}
```

**Response:**
```json
{
  "message": "Presentation deleted successfully",
  "presentation_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Request Parameters

#### GenerateRequest Model

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| topic | string | Yes | - | Topic or subject for the presentation (3-500 chars) |
| num_slides | integer | No | 5 | Number of slides (1-20) |
| custom_content | array | No | null | Custom slide content (overrides AI generation) |
| theme | object | No | default | Custom theme configuration |
| include_citations | boolean | No | true | Include source citations |
| aspect_ratio | string | No | "16:9" | Aspect ratio ("16:9" or "4:3") |

#### Theme Configuration

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| primary_color | string | "#1F4788" | Primary color in hex format |
| secondary_color | string | "#FFFFFF" | Secondary color in hex format |
| font_name | string | "Calibri" | Font family name |
| font_size_title | integer | 44 | Font size for titles (20-72) |
| font_size_body | integer | 18 | Font size for body text (10-36) |

#### Slide Layouts

1. **Title Slide**
   ```json
   {
     "layout": "title",
     "title": "Main Title",
     "content": "Subtitle"
   }
   ```

2. **Bullet Points**
   ```json
   {
     "layout": "bullet_points",
     "title": "Key Points",
     "bullet_points": [
       "Point 1",
       "Point 2",
       "Point 3"
     ]
   }
   ```

3. **Two-Column Layout**
   ```json
   {
     "layout": "two_column",
     "title": "Comparison",
     "left_column": "Left content",
     "right_column": "Right content"
   }
   ```

4. **Content with Image**
   ```json
   {
     "layout": "content_with_image",
     "title": "Visual Section",
     "content": "Main content",
     "image_description": "Image placeholder description"
   }
   ```

## Usage Examples

### Example 1: Basic Generation (cURL)
```bash
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Climate Change Solutions",
    "num_slides": 6
  }'
```

### Example 2: Custom Theme (Python)
```python
import requests

response = requests.post("http://localhost:8000/api/v1/generate", json={
    "topic": "Machine Learning Fundamentals",
    "num_slides": 10,
    "theme": {
        "primary_color": "#2E5090",
        "font_name": "Arial",
        "font_size_title": 40
    },
    "aspect_ratio": "4:3"
})

data = response.json()
print(f"Presentation created: {data['presentation_id']}")
```

### Example 3: Custom Content (JavaScript)
```javascript
const response = await fetch('http://localhost:8000/api/v1/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    topic: 'My Custom Presentation',
    custom_content: [
      {
        layout: 'title',
        title: 'Welcome',
        content: 'An Introduction'
      },
      {
        layout: 'bullet_points',
        title: 'Agenda',
        bullet_points: ['Topic 1', 'Topic 2', 'Topic 3']
      }
    ]
  })
});

const data = await response.json();
console.log('Generated:', data.file_path);
```

## Rate Limits

- Generate Presentation: 10 requests/minute
- Download Presentation: 20 requests/minute
- Delete Presentation: 30 requests/minute

## Error Handling

The API returns structured error responses:

```json
{
  "error": "ValidationError",
  "message": "Invalid request parameters",
  "details": {
    "field": "num_slides",
    "issue": "Value must be between 1 and 20"
  }
}
```

**Common Error Codes:**
- `400 Bad Request`: Invalid input parameters
- `404 Not Found`: Presentation not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server-side error

## Performance Optimization

The application includes several performance optimizations:

1. **Async Operations**: Asynchronous content generation for non-blocking I/O
2. **Rate Limiting**: Prevents server overload
3. **Efficient File Handling**: Optimized PowerPoint generation
4. **LRU Caching**: Cached settings for faster access

## Development

### Running Tests
```bash
pytest tests/ -v
```

### Code Quality
```bash
# Format code
black app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

## Sample Presentations

Three sample presentations are provided in the `sample_presentations/` directory:

1. **Artificial Intelligence.pptx** - AI fundamentals and applications
2. **Climate Change.pptx** - Environmental challenges and solutions
3. **Product Launch.pptx** - Business presentation example

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_api_key_here

# API Configuration
API_RATE_LIMIT=10/minute
MAX_SLIDES=20
MIN_SLIDES=1

# Environment
ENVIRONMENT=development
```

### Advanced Configuration

Edit `app/config.py` to customize:
- LLM model selection
- Temperature and token limits
- Output directory paths
- Cache settings

## Troubleshooting

### Issue: "OpenAI API key not configured"
**Solution**: Add your OpenAI API key to `.env` file, or use the application without it (fallback mode).

### Issue: "Module not found"
**Solution**: Ensure all dependencies are installed: `pip install -r requirements.txt`

### Issue: "Permission denied when saving files"
**Solution**: Check write permissions for the `generated_presentations` directory.

### Issue: Rate limit errors
**Solution**: Wait a moment between requests or adjust rate limits in configuration.

## Architecture

### Technology Stack
- **Framework**: FastAPI (modern, fast web framework)
- **Content Generation**: OpenAI GPT-3.5/4
- **Presentation Library**: python-pptx
- **Validation**: Pydantic v2
- **Rate Limiting**: SlowAPI
- **Async Support**: asyncio

### Design Patterns
- **Service Layer**: Separation of business logic
- **Dependency Injection**: FastAPI's DI system
- **Error Handling**: Centralized exception handlers
- **Configuration Management**: Pydantic Settings

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Ensure code quality (black, flake8, mypy)
5. Submit a pull request

## License

This project is provided as-is for evaluation purposes.

## Contact & Support

For questions or issues, please create an issue in the repository or contact the development team.

---

**Version**: 1.0.0
**Last Updated**: January 2024
