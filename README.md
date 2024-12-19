# Loyalty Program Design Service

This FastAPI service generates comprehensive loyalty program designs using OpenAI's GPT-4 model, incorporating customer analysis and business objectives.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/fsilva7456/loyalty-program-design-service.git
   cd loyalty-program-design-service
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your OpenAI API key:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'  # On Windows: set OPENAI_API_KEY=your-api-key-here
   ```

## Running the Service

1. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

2. The service will be available at `http://localhost:8000`

## API Documentation

- API documentation is available at `http://localhost:8000/docs`
- OpenAPI specification is available at `http://localhost:8000/openapi.json`

### Generate Program Design Endpoint

`POST /generate`

Example request:
```json
{
  "company_name": "Example Corp",
  "previous_data": {
    "customer_analysis": "Customer analysis details...",
    "loyalty_crm_objectives": "Loyalty objectives..."
  },
  "current_prompt_data": {
    "existing_generated_output": "Previous program design...",
    "user_feedback": "Add more digital engagement features"
  },
  "other_input_data": {}
}
```

Example response:
```json
{
  "generated_output": "Loyalty Program Design for Example Corp...\n1. Program Overview...\n2. Key Features...",
  "structured_data": {
    "loyalty_program_design": {
      "program_name": "ExampleRewards Plus",
      "overview": "A modern, digital-first loyalty program...",
      "target_audience": [
        "Digital-savvy consumers",
        "High-value customers"
      ],
      "tiers": [
        {
          "name": "Gold",
          "requirements": ["$1000 annual spend"],
          "benefits": ["Priority support", "Early access"],
          "earning_multiplier": 1.5
        }
      ],
      "earning_mechanisms": [
        {
          "type": "Purchase Points",
          "points_ratio": "10 points per $1",
          "description": "Standard earning on all purchases",
          "restrictions": ["Excludes tax and shipping"]
        }
      ],
      "redemption_options": [
        {
          "category": "Discounts",
          "description": "$10 off purchase",
          "points_required": "1000 points",
          "restrictions": ["Minimum $50 purchase"]
        }
      ],
      "special_features": [
        "Mobile app integration",
        "Social sharing rewards"
      ],
      "technology_requirements": [
        "CRM integration",
        "Mobile app platform"
      ]
    }
  }
}
```

## Key Features

- Uses OpenAI's GPT-4 model for program design
- Incorporates customer analysis and business objectives
- Supports iterative refinement through feedback
- Provides both narrative explanation and structured program design
- Includes detailed specifications for:
  - Program tiers and benefits
  - Earning mechanisms
  - Redemption options
  - Technology requirements

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)