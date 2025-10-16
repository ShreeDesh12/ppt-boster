# Slide Generator API - Complete Documentation

## Base URL
```
http://localhost:8000
```

## Table of Contents
- [Endpoints](#endpoints)
- [Request Models](#request-models)
- [Response Models](#response-models)
- [Examples](#examples)
- [Error Handling](#error-handling)

---

## Endpoints

### 1. Health Check
Check if the API is running and healthy.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-10-16T16:30:03.931211"
}
```

---

### 2. Generate Presentation
Generate a PowerPoint presentation with AI or custom content.

**Endpoint:** `POST /api/v1/generate`

**Rate Limit:** 10 requests per minute

**Content-Type:** `application/json`

---

## Request Models

### GenerateRequest (Main Request Body)

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `topic` | string | **Yes** | - | 3-500 chars | Topic or subject for the presentation |
| `num_slides` | integer | No | 5 | 1-20 | Number of slides to generate |
| `custom_content` | array | No | null | - | Array of SlideContent objects (overrides AI) |
| `theme` | object | No | default | - | ThemeConfig object for styling |
| `include_citations` | boolean | No | true | - | Include source citations in slides |
| `aspect_ratio` | string | No | "16:9" | "16:9" or "4:3" | Presentation aspect ratio |

#### Sample Basic Request
```json
{
  "topic": "Introduction to Machine Learning",
  "num_slides": 7,
  "include_citations": true,
  "aspect_ratio": "16:9"
}
```

---

### ThemeConfig Object

Customize the visual appearance of your presentation.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `primary_color` | string | No | "#1F4788" | Hex format | Primary color for titles and accents |
| `secondary_color` | string | No | "#FFFFFF" | Hex format | Secondary/background color |
| `font_name` | string | No | "Calibri" | - | Font family name |
| `font_size_title` | integer | No | 44 | 20-72 | Font size for slide titles (points) |
| `font_size_body` | integer | No | 18 | 10-36 | Font size for body text (points) |

#### Sample Theme
```json
{
  "theme": {
    "primary_color": "#2E7D32",
    "secondary_color": "#FFFFFF",
    "font_name": "Arial",
    "font_size_title": 40,
    "font_size_body": 20
  }
}
```

**Color Format Rules:**
- Must start with `#`
- Must be exactly 7 characters (e.g., `#1F4788`)
- Valid hex color codes only

**Common Color Palettes:**
```json
// Professional Blue
{"primary_color": "#1F4788", "secondary_color": "#FFFFFF"}

// Modern Green
{"primary_color": "#2E7D32", "secondary_color": "#F5F5F5"}

// Vibrant Orange
{"primary_color": "#FF6B35", "secondary_color": "#004E89"}

// Corporate Purple
{"primary_color": "#6A1B9A", "secondary_color": "#FFFFFF"}

// Tech Red
{"primary_color": "#D32F2F", "secondary_color": "#FAFAFA"}
```

---

### SlideContent Object (custom_content array items)

Each slide in `custom_content` must follow this structure based on its layout type.

#### Common Fields (All Layouts)

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `layout` | string (enum) | **Yes** | See layouts below | Type of slide layout |
| `title` | string | **Yes** | 1-200 chars | Slide title text |
| `notes` | string | No | - | Speaker notes (not displayed on slide) |

#### Layout Types and Their Specific Fields

##### 1. Title Slide Layout
**Layout Value:** `"title"`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `layout` | string | **Yes** | Must be `"title"` |
| `title` | string | **Yes** | Main presentation title |
| `content` | string | No | Subtitle or tagline |

**Example:**
```json
{
  "layout": "title",
  "title": "Artificial Intelligence in Healthcare",
  "content": "Revolutionizing Patient Care and Medical Research"
}
```

---

##### 2. Bullet Points Layout
**Layout Value:** `"bullet_points"`

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `layout` | string | **Yes** | Must be `"bullet_points"` | Layout identifier |
| `title` | string | **Yes** | 1-200 chars | Slide title |
| `bullet_points` | array[string] | **Yes** | 3-5 items | List of bullet point strings |

**Example:**
```json
{
  "layout": "bullet_points",
  "title": "Key Benefits of Cloud Computing",
  "bullet_points": [
    "Scalability: Easily scale resources up or down",
    "Cost-Effective: Pay only for what you use",
    "Reliability: 99.99% uptime guarantee",
    "Security: Enterprise-grade security features",
    "Accessibility: Access from anywhere, anytime"
  ],
  "notes": "Emphasize the cost savings"
}
```

**Validation:**
- Must have exactly 3, 4, or 5 bullet points
- Each bullet point should be a meaningful string
- Recommended: Keep each point under 100 characters

---

##### 3. Two-Column Layout
**Layout Value:** `"two_column"`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `layout` | string | **Yes** | Must be `"two_column"` |
| `title` | string | **Yes** | Slide title |
| `left_column` | string | No | Content for left side |
| `right_column` | string | No | Content for right side |

**Example:**
```json
{
  "layout": "two_column",
  "title": "Traditional vs Modern Approach",
  "left_column": "Traditional Development:\n\n• Waterfall methodology\n• Long release cycles\n• Monolithic architecture\n• Manual testing\n• On-premise deployment\n• High upfront costs",
  "right_column": "Modern Development:\n\n• Agile/DevOps practices\n• Continuous deployment\n• Microservices architecture\n• Automated testing\n• Cloud-native solutions\n• Subscription-based pricing"
}
```

**Tips for Two-Column Content:**
- Use `\n` for line breaks
- Use `\n\n` for paragraph spacing
- Use `•` or `-` for bullet points within columns
- Keep content balanced between columns

---

##### 4. Content with Image Layout
**Layout Value:** `"content_with_image"`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `layout` | string | **Yes** | Must be `"content_with_image"` |
| `title` | string | **Yes** | Slide title |
| `content` | string | No | Main descriptive text |
| `image_description` | string | No | Description shown in image placeholder |
| `image_url` | string | No | URL to image (currently displays as placeholder) |

**Example:**
```json
{
  "layout": "content_with_image",
  "title": "Machine Learning Model Performance",
  "content": "Our latest deep learning model achieved 97.3% accuracy on the test dataset, surpassing industry benchmarks by 12%. The model uses a transformer architecture with attention mechanisms, trained on over 10 million data points. Inference time is under 50ms, making it suitable for real-time applications.",
  "image_description": "Graph showing model accuracy comparison",
  "image_url": "https://example.com/charts/ml-performance.png",
  "notes": "Highlight the 12% improvement over competitors"
}
```

---

### Citation Object (Response Only)

Citations are returned in the response when `include_citations: true` and AI generation is used.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `source` | string | **Yes** | Source name or URL |
| `title` | string | No | Title of article/publication |
| `date` | string | No | Publication date |

**Example:**
```json
{
  "citations": [
    {
      "source": "Nature Medicine",
      "title": "AI Applications in Medical Imaging",
      "date": "2023"
    },
    {
      "source": "https://www.nejm.org/doi/full/10.1056/NEJMra2034861",
      "title": "Machine Learning in Clinical Practice",
      "date": "January 2024"
    }
  ]
}
```

---

## Response Models

### GenerateResponse

| Field | Type | Description |
|-------|------|-------------|
| `presentation_id` | string (UUID) | Unique identifier for the presentation |
| `topic` | string | Presentation topic |
| `num_slides` | integer | Number of slides generated |
| `slides` | array[SlideContent] | Array of generated slide objects |
| `citations` | array[Citation] or null | Source citations (if applicable) |
| `file_path` | string | Path to generated .pptx file |
| `generation_time_seconds` | float | Time taken to generate (seconds) |

**Example Response:**
```json
{
  "presentation_id": "365f6536-abe2-4919-8bd3-597e5aeb3936",
  "topic": "Python Programming Basics",
  "num_slides": 5,
  "slides": [
    {
      "layout": "title",
      "title": "Python Programming Basics",
      "content": "A comprehensive overview of Python Programming Basics",
      "bullet_points": null,
      "left_column": null,
      "right_column": null,
      "image_url": null,
      "image_description": null,
      "notes": null
    }
  ],
  "citations": null,
  "file_path": "./generated_presentations/13b8f83f-13f2-4997-aedb-c5bfcd268146.pptx",
  "generation_time_seconds": 1.07
}
```

---

## Complete Examples

### Example 1: AI-Generated Presentation (Minimal)
```json
{
  "topic": "Introduction to Docker Containers",
  "num_slides": 6
}
```

**What happens:**
- AI generates 6 slides about Docker
- Uses default theme (blue)
- 16:9 aspect ratio
- Includes citations
- Mixed layouts (title, bullets, two-column, image)

---

### Example 2: Custom Theme + AI Content
```json
{
  "topic": "Sustainable Energy Solutions",
  "num_slides": 8,
  "include_citations": true,
  "aspect_ratio": "16:9",
  "theme": {
    "primary_color": "#2E7D32",
    "secondary_color": "#FFFFFF",
    "font_name": "Arial",
    "font_size_title": 40,
    "font_size_body": 20
  }
}
```

**What happens:**
- AI generates 8 slides
- Green theme (#2E7D32)
- Arial font throughout
- Citations included
- 16:9 format

---

### Example 3: Fully Custom Content
```json
{
  "topic": "Q4 2024 Performance Review",
  "include_citations": false,
  "aspect_ratio": "16:9",
  "custom_content": [
    {
      "layout": "title",
      "title": "Q4 2024 Performance Review",
      "content": "Outstanding Results & Strategic Vision"
    },
    {
      "layout": "bullet_points",
      "title": "Key Achievements This Quarter",
      "bullet_points": [
        "Revenue exceeded targets by 35% ($50M vs $37M projected)",
        "Successfully launched AI-powered analytics platform",
        "Expanded team from 380 to 450 employees",
        "Customer satisfaction score improved to 92% (up from 85%)"
      ]
    },
    {
      "layout": "two_column",
      "title": "Financial Performance Summary",
      "left_column": "Revenue Metrics:\n\n• Total Revenue: $50M\n• YoY Growth: 35%\n• Gross Margin: 68%\n• Operating Income: $12M\n• EBITDA: $15M\n• Cash Flow: $8M",
      "right_column": "Customer Metrics:\n\n• Active Customers: 150,000\n• New Customers: 25,000\n• Churn Rate: 2.1%\n• NPS Score: 72\n• LTV/CAC: 4.2x\n• Avg Deal Size: $5,200"
    },
    {
      "layout": "content_with_image",
      "title": "Product Innovation Highlights",
      "content": "Our flagship AI platform processed over 2.3 million transactions this quarter with 99.97% accuracy. The system reduced customer processing time by 65% and saved an estimated 180,000 work hours across our client base. Integration partnerships with Salesforce and HubSpot drove 40% of new customer acquisition.",
      "image_description": "Dashboard showing AI platform metrics and user growth"
    },
    {
      "layout": "bullet_points",
      "title": "Strategic Priorities for 2025",
      "bullet_points": [
        "Scale to $200M ARR through enterprise expansion",
        "Launch European operations (UK, Germany, France)",
        "Release mobile application (iOS & Android)",
        "Achieve SOC 2 Type II compliance by Q2"
      ]
    },
    {
      "layout": "two_column",
      "title": "Investment & Resource Allocation",
      "left_column": "Q1 2025 Budget:\n\n• Engineering: $8M\n• Sales & Marketing: $12M\n• Operations: $4M\n• R&D: $6M\n• Total: $30M",
      "right_column": "Hiring Plan:\n\n• Engineers: +50\n• Sales Reps: +30\n• Customer Success: +20\n• Product: +15\n• Total New Hires: +115"
    }
  ],
  "theme": {
    "primary_color": "#1F4788",
    "secondary_color": "#FFFFFF",
    "font_name": "Calibri",
    "font_size_title": 44,
    "font_size_body": 18
  }
}
```

**What happens:**
- Uses all your custom slides (6 slides)
- No AI generation
- Professional blue theme
- No citations
- Complete control over content

---

### Example 4: Mixed - Custom Theme with AI
```json
{
  "topic": "Cybersecurity Best Practices for 2025",
  "num_slides": 10,
  "include_citations": true,
  "aspect_ratio": "4:3",
  "theme": {
    "primary_color": "#D32F2F",
    "secondary_color": "#FAFAFA",
    "font_name": "Helvetica",
    "font_size_title": 36,
    "font_size_body": 16
  }
}
```

**What happens:**
- AI generates 10 slides about cybersecurity
- Red theme for emphasis
- 4:3 aspect ratio (classic format)
- Smaller fonts for more content
- Citations included

---

## cURL Examples

### Basic Generation
```bash
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Python Programming Basics",
    "num_slides": 5
  }'
```

### With Custom Theme
```bash
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Digital Marketing",
    "num_slides": 8,
    "theme": {
      "primary_color": "#FF6B35",
      "font_name": "Arial"
    }
  }'
```

### Fully Custom Content
```bash
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "My Custom Presentation",
    "custom_content": [
      {
        "layout": "title",
        "title": "Welcome",
        "content": "Getting Started"
      },
      {
        "layout": "bullet_points",
        "title": "Agenda",
        "bullet_points": [
          "Introduction",
          "Main Content",
          "Q&A"
        ]
      }
    ]
  }'
```

---

## Error Handling

### ErrorResponse Model

| Field | Type | Description |
|-------|------|-------------|
| `error` | string | Error type/category |
| `message` | string | Human-readable error message |
| `details` | object or null | Additional error details |

### Common Error Responses

#### 400 Bad Request - Validation Error
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

#### 400 Bad Request - Invalid Bullet Points
```json
{
  "error": "ValidationError",
  "message": "Bullet points layout requires 3-5 bullet points",
  "details": {
    "provided": 2,
    "required": "3-5"
  }
}
```

#### 400 Bad Request - Invalid Color
```json
{
  "error": "ValidationError",
  "message": "Color must be in hex format (e.g., #1F4788)",
  "details": {
    "field": "primary_color",
    "provided": "blue"
  }
}
```

#### 429 Too Many Requests - Rate Limit
```json
{
  "error": "RateLimitExceeded",
  "message": "Rate limit exceeded: 10 per 1 minute",
  "details": {
    "limit": "10/minute",
    "retry_after": 45
  }
}
```

#### 500 Internal Server Error
```json
{
  "error": "InternalServerError",
  "message": "Failed to generate presentation: Unexpected error occurred",
  "details": {
    "error": "Connection timeout"
  }
}
```

---

## Validation Rules Summary

### Field Validations

| Field | Validation Rules |
|-------|-----------------|
| `topic` | 3-500 characters, required |
| `num_slides` | 1-20, integer |
| `aspect_ratio` | Must be "16:9" or "4:3" |
| `primary_color` | Must start with #, exactly 7 chars |
| `font_size_title` | 20-72 points |
| `font_size_body` | 10-36 points |
| `title` (slide) | 1-200 characters |
| `bullet_points` | Must have 3-5 items for bullet_points layout |
| `layout` | Must be one of: title, bullet_points, two_column, content_with_image |

### Layout-Specific Validations

**Title Layout:**
- Must have `title`
- `content` is optional

**Bullet Points Layout:**
- Must have `title` and `bullet_points`
- `bullet_points` must contain 3-5 strings

**Two-Column Layout:**
- Must have `title`
- `left_column` and `right_column` are optional but recommended

**Content with Image Layout:**
- Must have `title`
- All other fields optional

---

## Rate Limits

| Endpoint | Limit |
|----------|-------|
| POST /api/v1/generate | 10 requests/minute |
| GET /api/v1/download/{id} | 20 requests/minute |
| DELETE /api/v1/presentations/{id} | 30 requests/minute |
| GET /health | No limit |

---

## Download Presentation

**Endpoint:** `GET /api/v1/download/{presentation_id}`

**Example:**
```bash
curl -o my_presentation.pptx \
  http://localhost:8000/api/v1/download/365f6536-abe2-4919-8bd3-597e5aeb3936
```

**Response:** Binary PowerPoint file (.pptx)

---

## Delete Presentation

**Endpoint:** `DELETE /api/v1/presentations/{presentation_id}`

**Example:**
```bash
curl -X DELETE \
  http://localhost:8000/api/v1/presentations/365f6536-abe2-4919-8bd3-597e5aeb3936
```

**Response:**
```json
{
  "message": "Presentation deleted successfully",
  "presentation_id": "365f6536-abe2-4919-8bd3-597e5aeb3936"
}
```

---

## Interactive API Documentation

Once the server is running, access interactive documentation at:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

These provide:
- Interactive API testing
- Automatic request/response examples
- Schema validation
- Try-it-out functionality

---

## Tips & Best Practices

### Content Tips
1. **Titles:** Keep slide titles under 60 characters for readability
2. **Bullet Points:** Each point should be concise (under 100 chars)
3. **Two-Column:** Balance content between columns
4. **Images:** Provide descriptive image_description for clarity

### Theme Tips
1. **Colors:** Use high contrast (dark on light or light on dark)
2. **Fonts:** Stick to standard fonts (Calibri, Arial, Helvetica)
3. **Sizes:** Larger fonts for presentations on big screens

### Performance Tips
1. **Batch Requests:** Generate multiple presentations concurrently if needed
2. **Caching:** Save generated presentation_id for downloads
3. **Custom Content:** Faster than AI generation (no API calls)

### Common Patterns

**Corporate Presentation:**
```json
{
  "aspect_ratio": "16:9",
  "theme": {
    "primary_color": "#1F4788",
    "font_name": "Calibri"
  }
}
```

**Academic Presentation:**
```json
{
  "aspect_ratio": "4:3",
  "include_citations": true,
  "theme": {
    "primary_color": "#2E5090",
    "font_name": "Times New Roman"
  }
}
```

**Marketing Presentation:**
```json
{
  "aspect_ratio": "16:9",
  "theme": {
    "primary_color": "#FF6B35",
    "font_name": "Arial",
    "font_size_title": 48
  }
}
```

---

## Version Information

- **API Version:** 1.0.0
- **Last Updated:** January 2025
- **Base Framework:** FastAPI 0.103.2
- **Python Version:** 3.7+

For questions or issues, please refer to the README.md or open an issue in the repository.
