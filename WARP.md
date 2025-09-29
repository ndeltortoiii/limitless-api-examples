# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Repository Overview

This repository contains code examples for the Limitless Developer API, which provides access to lifelog data from Limitless users. The examples demonstrate realistic use cases for consuming transcript data and processing it with AI services.

## Project Structure

- **`python/`** - Python implementation with client library and examples
- **`typescript/`** - TypeScript implementation with equivalent functionality
- **`openapi.yml`** - Complete OpenAPI specification for the Limitless API
- **`notebooks/`** - Jupyter notebooks with data visualization examples

## Core Components

### API Client Libraries
Both Python and TypeScript implementations include:
- **`_client.py`** / **`_client.ts`** - Core API client with pagination support
- Handles authentication via `X-API-Key` header
- Automatic timezone detection and cursor-based pagination
- Configurable batch sizes and request limits

### Example Applications
- **Export Markdown** - Fetches and displays raw transcript content
- **Summarize Day** - Uses OpenAI to generate summaries of lifelog data
- **Chart Usage** - Jupyter notebook for visualizing recording patterns

## Development Commands

### Python Setup
```bash
cd python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Python Examples
```bash
# Export most recent lifelog as markdown
LIMITLESS_API_KEY="your_key" python export_markdown.py

# Generate AI summary of recent lifelogs
LIMITLESS_API_KEY="your_key" OPENAI_API_KEY="your_key" python summarize_day.py
```

### TypeScript Setup
```bash
cd typescript
npm install
```

### TypeScript Examples
```bash
# Export markdown
npm run export-markdown

# Generate summary
npm run summarize-day

# Build TypeScript
npm run build
```

### Environment Variables
Required for examples:
- `LIMITLESS_API_KEY` - API key from Limitless developer portal
- `OPENAI_API_KEY` - Required for summarization examples
- `LIMITLESS_API_URL` - Optional, defaults to `https://api.limitless.ai`

## API Architecture

### Core Data Model
The API returns lifelog entries with:
- **Hierarchical content structure** using nested `ContentNode` objects
- **Temporal metadata** with precise start/end times and offsets
- **Speaker identification** with special "user" designation
- **Rich content types** including headings, paragraphs, and blockquotes

### Pagination Strategy
The client libraries implement cursor-based pagination:
- Use `nextCursor` from response metadata for subsequent requests
- Configurable batch sizes (default 10 items per request)
- Automatic handling of pagination limits and termination

### Content Processing
Lifelogs support multiple output formats:
- Raw markdown for direct display
- Structured content nodes for programmatic processing
- Optional heading inclusion/exclusion
- Timezone-aware timestamp handling

## Key Implementation Details

### API Client Pattern
Both implementations follow identical patterns:
- Async/await in TypeScript, synchronous in Python
- Unified error handling for HTTP failures
- Automatic local timezone detection
- Progress logging for multi-page requests

### Data Visualization
The Jupyter notebook demonstrates:
- Timeline visualization of recording sessions
- Statistical analysis of usage patterns
- Integration with pandas and matplotlib
- Real-time API data fetching

### AI Integration
Summarization examples show:
- Context window management for large datasets
- Streaming response handling
- Prompt engineering for transcript analysis
- Integration with OpenAI GPT models

## Testing and Development

### Running Individual Examples
Each example script can be run independently with appropriate environment variables. The TypeScript package includes npm scripts for common tasks.

### API Testing
Use the provided cURL examples in the README for quick API validation:
```bash
curl -X GET "https://api.limitless.ai/v1/lifelogs" \
     -H "X-API-KEY: YOUR_API_KEY"
```

### Client Code Generation
The OpenAPI specification can be used to generate client libraries for additional languages beyond the provided Python and TypeScript implementations.