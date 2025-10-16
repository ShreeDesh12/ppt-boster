"""
LLM prompt templates for content generation
"""

SYSTEM_INSTRUCTION = """You are an expert presentation designer. Create engaging, well-structured presentation content."""


def get_generation_instruction(topic: str, num_slides: int, include_citations: bool) -> str:
    """
    Build the LLM instruction prompt for generating presentation content

    Args:
        topic: Presentation topic
        num_slides: Number of slides to generate
        include_citations: Whether to include citations

    Returns:
        Formatted instruction prompt
    """
    citations_requirement = ""
    if include_citations:
        citations_requirement = "\n- Include 2-3 source citations in JSON format at the end."

    instruction = f"""Create a {num_slides}-slide presentation about: {topic}

Requirements:
- Slide 1 must be a title slide with a catchy title and subtitle
- Use a variety of layouts: bullet_points, two_column, and content_with_image
- For bullet_points slides: provide exactly 3-5 bullet points
- For two_column slides: provide content for left and right columns
- For content_with_image slides: provide content text and image description
- Make content engaging, informative, and well-structured{citations_requirement}

Return the response in the following JSON format:
{{
  "slides": [
    {{
      "layout": "title",
      "title": "Main Title",
      "content": "Subtitle or tagline"
    }},
    {{
      "layout": "bullet_points",
      "title": "Key Points",
      "bullet_points": ["Point 1", "Point 2", "Point 3"]
    }},
    {{
      "layout": "two_column",
      "title": "Comparison",
      "left_column": "Left content",
      "right_column": "Right content"
    }},
    {{
      "layout": "content_with_image",
      "title": "Visual Section",
      "content": "Descriptive text",
      "image_description": "Description of relevant image"
    }}
  ],
  "citations": [
    {{"source": "Source name", "title": "Article title", "date": "2024"}}
  ]
}}

Ensure valid JSON format. Be creative and informative!"""

    return instruction


# Alternative instruction templates for different presentation styles

BUSINESS_PRESENTATION_INSTRUCTION = """Create a professional business presentation about: {topic}

Focus on:
- Executive-level insights
- Data-driven content
- Clear ROI and value propositions
- Professional and concise language

{base_requirements}"""


EDUCATIONAL_PRESENTATION_INSTRUCTION = """Create an educational presentation about: {topic}

Focus on:
- Clear explanations suitable for learners
- Step-by-step progression of concepts
- Examples and analogies
- Engaging and accessible language

{base_requirements}"""


TECHNICAL_PRESENTATION_INSTRUCTION = """Create a technical presentation about: {topic}

Focus on:
- Detailed technical specifications
- Architecture and design patterns
- Code examples where relevant
- Best practices and recommendations

{base_requirements}"""


MARKETING_PRESENTATION_INSTRUCTION = """Create a marketing presentation about: {topic}

Focus on:
- Compelling value propositions
- Customer benefits and outcomes
- Visual storytelling
- Persuasive and engaging language

{base_requirements}"""


def get_styled_instruction(topic: str, num_slides: int, include_citations: bool, style: str = "default") -> str:
    """
    Get instruction prompt with specific presentation style

    Args:
        topic: Presentation topic
        num_slides: Number of slides to generate
        include_citations: Whether to include citations
        style: Presentation style (default, business, educational, technical, marketing)

    Returns:
        Formatted instruction prompt
    """
    base_requirements = f"""Number of slides: {num_slides}

Layout requirements:
- Use a variety of layouts: title, bullet_points, two_column, content_with_image
- For bullet_points slides: exactly 3-5 bullet points
- For two_column slides: balanced content for both columns
- For content_with_image slides: descriptive text and image suggestions

JSON Format:
{{
  "slides": [...],
  "citations": [{{"source": "...", "title": "...", "date": "..."}}]
}}"""

    style_templates = {
        "business": BUSINESS_PRESENTATION_INSTRUCTION,
        "educational": EDUCATIONAL_PRESENTATION_INSTRUCTION,
        "technical": TECHNICAL_PRESENTATION_INSTRUCTION,
        "marketing": MARKETING_PRESENTATION_INSTRUCTION
    }

    if style in style_templates:
        return style_templates[style].format(
            topic=topic,
            base_requirements=base_requirements
        )
    else:
        return get_generation_instruction(topic, num_slides, include_citations)
