"""
Content generation service using OpenAI API via HTTP requests
"""
import os
import json
import logging
import httpx
from typing import List, Optional, Tuple
from app.models import SlideContent, SlideLayout, Citation
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# System instruction for LLM
SYSTEM_INSTRUCTION = """You are an expert presentation designer. Create engaging, well-structured presentation content."""

# Load instruction template from file
def load_instruction_template():
    """Load the LLM instruction template from config file"""
    config_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = os.path.join(config_dir, 'config', 'llm_instruction.txt')

    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error loading instruction template: {e}")
        # Fallback to default
        return """Create a {num_slides}-slide presentation about: {topic}
Return in JSON format with slides and citations."""

INSTRUCTION_TEMPLATE = load_instruction_template()


class ContentGenerator:
    """Generates presentation content using LLM"""

    def __init__(self):
        logger.info("Initializing ContentGenerator")
        self.api_key = settings.openai_api_key
        self.api_url = "https://api.openai.com/v1/responses"

        if not self.api_key or self.api_key == "":
            logger.warning("OpenAI API key not configured. Using fallback content generation.")
        else:
            logger.info("OpenAI API key configured successfully")

    async def generate_slides(
        self,
        topic: str,
        num_slides: int,
        include_citations: bool = True
    ) -> Tuple[List[SlideContent], Optional[List[Citation]]]:
        """
        Generate slide content for a given topic

        Args:
            topic: Presentation topic
            num_slides: Number of slides to generate
            include_citations: Whether to include citations

        Returns:
            Tuple of (slides, citations)
        """
        logger.info(f"Starting slide generation for topic: '{topic}', num_slides: {num_slides}, include_citations: {include_citations}")

        self.__validate_parameters(topic, num_slides)

        if self.api_key and self.api_key != "":
            logger.info("Using LLM-based content generation")
            return await self._generate_with_llm(topic, num_slides, include_citations)
        else:
            logger.info("Using fallback content generation")
            return self._generate_fallback_content(topic, num_slides, include_citations)

    async def _generate_with_llm(
        self,
        topic: str,
        num_slides: int,
        include_citations: bool
    ) -> Tuple[List[SlideContent], Optional[List[Citation]]]:
        """Generate content using OpenAI API"""
        logger.debug(f"_generate_with_llm called with topic='{topic}', num_slides={num_slides}")

        try:
            logger.debug("Building LLM instruction prompt from template")

            # Prepare citations requirement
            citations_requirement = ""
            if include_citations:
                citations_requirement = "\n- Include 2-3 source citations in JSON format at the end."

            # Format the template with variables
            user_prompt = INSTRUCTION_TEMPLATE.format(
                num_slides=num_slides,
                topic=topic,
                citations_requirement=citations_requirement
            )
            logger.debug(f"Prompt length: {len(user_prompt)} characters")

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            payload = {
                "model": settings.llm_model,
                "input": f"{SYSTEM_INSTRUCTION}\n\n{user_prompt}",
                "temperature": settings.llm_temperature
            }

            logger.debug(f"Calling OpenAI API with model: {settings.llm_model}, temperature: {settings.llm_temperature}")

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=payload
                )

                logger.debug(f"OpenAI API response status: {response.status_code}")

                if response.status_code != 200:
                    logger.error(f"OpenAI API error: {response.status_code} - {response.text}")
                    logger.info("Falling back to default content generation")
                    return self._generate_fallback_content(topic, num_slides, include_citations)

                data = response.json()
                logger.debug(f"API response status: {data.get('status')}")

                # Handle different response structures
                if 'choices' in data:
                    # Standard chat completions format
                    content = data['choices'][0]['message']['content']
                elif 'output' in data:
                    # Responses API format
                    # Extract text from output[0]['content'][0]['text']
                    if isinstance(data['output'], list) and len(data['output']) > 0:
                        output_item = data['output'][0]
                        if 'content' in output_item and len(output_item['content']) > 0:
                            content = output_item['content'][0]['text']
                        else:
                            raise ValueError("No content found in response output")
                    else:
                        raise ValueError("Invalid output structure in response")
                else:
                    logger.error(f"Unexpected response structure: {data}")
                    raise ValueError("Unexpected API response structure")

                logger.debug(f"Received LLM response, length: {len(content)} characters")

                return self._parse_llm_response(content, num_slides)

        except Exception as e:
            logger.error(f"Error generating content with LLM: {str(e)}", exc_info=True)
            logger.info("Falling back to default content generation due to exception")
            return self._generate_fallback_content(topic, num_slides, include_citations)

    def _parse_llm_response(
        self,
        response: str,
        num_slides: int
    ) -> Tuple[List[SlideContent], Optional[List[Citation]]]:
        """Parse LLM response into structured format"""
        logger.debug(f"_parse_llm_response called with response length: {len(response)}")

        try:
            # Try to extract JSON from the response
            logger.debug("Extracting JSON from LLM response")
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1

            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                logger.debug(f"Found JSON block at positions {start_idx}:{end_idx}")

                data = json.loads(json_str)
                logger.debug(f"Successfully parsed JSON. Found {len(data.get('slides', []))} slides")

                slides = []
                for idx, slide_data in enumerate(data.get('slides', [])[:num_slides]):
                    slides.append(SlideContent(**slide_data))
                    logger.debug(f"Parsed slide {idx + 1}: layout={slide_data.get('layout')}, title={slide_data.get('title', '')[:30]}...")

                citations = None
                if 'citations' in data and data['citations']:
                    citations = [Citation(**c) for c in data['citations']]
                    logger.debug(f"Parsed {len(citations)} citations")

                logger.debug(f"Successfully created {len(slides)} slide objects")
                return slides, citations
            else:
                raise ValueError("No valid JSON found in response")

        except Exception as e:
            logger.error(f"Error parsing LLM response: {str(e)}", exc_info=True)
            logger.debug("Falling back to default content generation")
            # Fall back to default content
            return self._generate_fallback_content(
                topic="Generated Content",
                num_slides=num_slides,
                include_citations=False
            )

    def _generate_fallback_content(
        self,
        topic: str,
        num_slides: int,
        include_citations: bool
    ) -> Tuple[List[SlideContent], Optional[List[Citation]]]:
        """Generate fallback content when LLM is not available"""
        logger.debug(f"_generate_fallback_content called for topic='{topic}', num_slides={num_slides}")

        slides = []

        # Title slide
        logger.debug("Creating title slide")
        slides.append(SlideContent(
            layout=SlideLayout.TITLE,
            title=topic,
            content=f"A comprehensive overview of {topic}"
        ))

        # Generate remaining slides with varied layouts
        layouts = [
            SlideLayout.BULLET_POINTS,
            SlideLayout.TWO_COLUMN,
            SlideLayout.CONTENT_WITH_IMAGE,
            SlideLayout.BULLET_POINTS
        ]
        logger.debug(f"Generating {num_slides - 1} additional slides with varied layouts")

        for i in range(1, num_slides):
            layout = layouts[(i - 1) % len(layouts)]

            if layout == SlideLayout.BULLET_POINTS:
                slides.append(SlideContent(
                    layout=layout,
                    title=f"Key Points About {topic} ({i})",
                    bullet_points=[
                        f"Important aspect {i}.1 of {topic}",
                        f"Critical consideration {i}.2 for understanding",
                        f"Essential element {i}.3 to remember",
                        f"Notable feature {i}.4 worth exploring"
                    ]
                ))
            elif layout == SlideLayout.TWO_COLUMN:
                slides.append(SlideContent(
                    layout=layout,
                    title=f"Comparing Aspects of {topic}",
                    left_column=f"Traditional approaches to {topic} include established methods and proven techniques.",
                    right_column=f"Modern innovations in {topic} bring new perspectives and advanced solutions."
                ))
            elif layout == SlideLayout.CONTENT_WITH_IMAGE:
                slides.append(SlideContent(
                    layout=layout,
                    title=f"Visual Overview of {topic}",
                    content=f"This section provides a detailed exploration of {topic}, highlighting its significance and practical applications in real-world scenarios.",
                    image_description=f"Illustration showing key concepts of {topic}"
                ))

        # Add citations if requested
        citations = None
        if include_citations:
            logger.debug("Adding default citations")
            citations = [
                Citation(
                    source="Academic Research Database",
                    title=f"Comprehensive Study on {topic}",
                    date="2024"
                ),
                Citation(
                    source="Industry Publications",
                    title=f"Latest Trends in {topic}",
                    date="2024"
                )
            ]

        logger.debug(f"Fallback content generation complete. Generated {len(slides)} slides")
        return slides[:num_slides], citations

    def __validate_parameters(self, topic: str, num_slides: int):
        """Validate input parameters"""
        if not topic or topic.strip() == "":
            logger.error("Validation error: Topic must be a non-empty string")
            raise ValueError("Topic must be a non-empty string")

        if not (settings.min_slides <= num_slides <= settings.max_slides):
            logger.error(f"Validation error: Number of slides must be between {settings.min_slides} and {settings.max_slides}")
            raise ValueError(
                f"Number of slides must be between {settings.min_slides} and {settings.max_slides}"
            )

        logger.debug("Input parameters validated successfully")
