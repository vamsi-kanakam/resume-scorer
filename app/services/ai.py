import os
from anthropic import AsyncAnthropic
from dotenv import load_dotenv

load_dotenv()

client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

PROMPT_TEMPLATE = """
You are an expert resume reviewer and recruiter.

Analyze how well the following resume matches the job description. Provide:                       
  1. A match score from 0 to 100                                                                    
  2. Key strengths (skills/experience that match well)                                              
  3. Key gaps (important requirements the resume is missing)                                        
  4. A brief overall summary                                                                        
                                                                                                    
  Resume:                                                                                           
  {resume}                                                                                          
                                                                                                    
  Job Description:                                                                                  
  {jd}                                                                                              
                                                                                                    
  Respond in this exact JSON format:                                                                
  {{                                                                                                
    "score": <number 0-100>,                                                                        
    "strengths": ["...", "..."],                                                                    
    "gaps": ["...", "..."],                                                                         
    "summary": "..."                                                                                
  }}
"""

async def score_resume(resume: str, jd: str) -> dict:
    import json
    message = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        thinking={'type':'adaptive'},
        messages=[
            {
                "role": "user",
                "content": PROMPT_TEMPLATE.format(resume=resume, jd=jd)
            }
        ]
    )
    for block in message.content:
        if block.type == "text":
            text = block.text.strip()
            if text.startswith("```"):
                text = text.split("```", 2)[1]
                if text.startswith("json"):
                    text = text[4:]
                text = text.strip()
            return json.loads(text)
    return {"error": "No text response from Claude"}
