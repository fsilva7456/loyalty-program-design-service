import os
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import json

app = FastAPI(title="Loyalty Program Design Service")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ProgramTier(BaseModel):
    name: str
    requirements: List[str]
    benefits: List[str]
    earning_multiplier: float

class EarningMechanism(BaseModel):
    type: str
    points_ratio: str
    description: str
    restrictions: List[str]

class RedemptionOption(BaseModel):
    category: str
    description: str
    points_required: str
    restrictions: List[str]

class LoyaltyProgramDesign(BaseModel):
    program_name: str
    overview: str
    target_audience: List[str]
    tiers: List[ProgramTier]
    earning_mechanisms: List[EarningMechanism]
    redemption_options: List[RedemptionOption]
    special_features: List[str]
    technology_requirements: List[str]

class PreviousData(BaseModel):
    customer_analysis: Optional[str] = None
    loyalty_crm_objectives: Optional[str] = None

class CurrentPromptData(BaseModel):
    existing_generated_output: str
    user_feedback: str

class ProgramDesignRequest(BaseModel):
    company_name: str
    previous_data: Optional[PreviousData] = None
    current_prompt_data: Optional[CurrentPromptData] = None
    other_input_data: Optional[Dict] = {}

class ProgramDesignResponse(BaseModel):
    generated_output: str
    structured_data: Dict

def construct_system_prompt() -> str:
    return """
You are an expert loyalty program designer. Create comprehensive loyalty program designs 
that align with business objectives and customer needs. Consider:

1. Program Structure and Mechanics
   - Tiering strategy
   - Points earning mechanisms
   - Redemption options

2. Customer Experience
   - Enrollment process
   - Member benefits
   - Digital integration

3. Business Requirements
   - Technology needs
   - Operational considerations
   - Success metrics

Provide your response in two parts:
1. A detailed explanation in natural language
2. A structured JSON object with this exact schema:
{
    "loyalty_program_design": {
        "program_name": "Name",
        "overview": "Brief description",
        "target_audience": ["audience1", "audience2"],
        "tiers": [
            {
                "name": "Tier Name",
                "requirements": ["requirement1", "requirement2"],
                "benefits": ["benefit1", "benefit2"],
                "earning_multiplier": 1.0
            }
        ],
        "earning_mechanisms": [
            {
                "type": "Mechanism Type",
                "points_ratio": "X points per $",
                "description": "Description",
                "restrictions": ["restriction1"]
            }
        ],
        "redemption_options": [
            {
                "category": "Category",
                "description": "Description",
                "points_required": "X points",
                "restrictions": ["restriction1"]
            }
        ],
        "special_features": ["feature1", "feature2"],
        "technology_requirements": ["requirement1"]
    }
}

Separate the two parts with [JSON_START] and [JSON_END] markers.
"""

def construct_user_prompt(
    company_name: str,
    customer_analysis: Optional[str] = None,
    loyalty_objectives: Optional[str] = None,
    existing_output: Optional[str] = None,
    feedback: Optional[str] = None
) -> str:
    prompt = f"Please design a loyalty program for {company_name}."
    
    if customer_analysis:
        prompt += f"\n\nConsider this customer analysis: {customer_analysis}"
    
    if loyalty_objectives:
        prompt += f"\n\nAlign with these loyalty objectives: {loyalty_objectives}"
    
    if existing_output and feedback:
        prompt += f"""
\n\nPrevious design: {existing_output}
\nPlease refine the design based on this feedback: {feedback}
"""
    
    return prompt

def extract_json_from_text(text: str) -> dict:
    try:
        start_marker = "[JSON_START]"
        end_marker = "[JSON_END]"
        json_str = text[text.find(start_marker) + len(start_marker):text.find(end_marker)].strip()
        return json.loads(json_str)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse structured data from response: {str(e)}"
        )

def generate_program_design(
    company_name: str,
    customer_analysis: Optional[str] = None,
    loyalty_objectives: Optional[str] = None,
    existing_output: Optional[str] = None,
    feedback: Optional[str] = None
) -> tuple[str, dict]:
    """Generate loyalty program design using OpenAI's API"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": construct_system_prompt()},
                {"role": "user", "content": construct_user_prompt(
                    company_name,
                    customer_analysis,
                    loyalty_objectives,
                    existing_output,
                    feedback
                )}
            ],
            temperature=0.7,
            max_tokens=2500
        )
        
        full_response = response.choices[0].message.content
        analysis = full_response[:full_response.find("[JSON_START]")].strip()
        structured_data = extract_json_from_text(full_response)
        
        return analysis, structured_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate", response_model=ProgramDesignResponse)
async def generate_design(request: ProgramDesignRequest):
    # Extract data from request
    customer_analysis = None
    loyalty_objectives = None
    if request.previous_data:
        customer_analysis = request.previous_data.customer_analysis
        loyalty_objectives = request.previous_data.loyalty_crm_objectives
    
    existing_output = None
    feedback = None
    if request.current_prompt_data:
        existing_output = request.current_prompt_data.existing_generated_output
        feedback = request.current_prompt_data.user_feedback
    
    # Generate program design
    generated_text, structured_data = generate_program_design(
        request.company_name,
        customer_analysis,
        loyalty_objectives,
        existing_output,
        feedback
    )
    
    return ProgramDesignResponse(
        generated_output=generated_text,
        structured_data=structured_data
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)