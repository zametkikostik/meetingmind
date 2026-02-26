"""
Meeting Analyzer - LLM-powered meeting analysis
Generates summaries, action items, topics, and insights
"""
import json
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AnalysisResult:
    """Result of meeting analysis"""
    summary: str
    key_topics: List[str]
    action_items: List[Dict[str, Any]]
    sentiment_score: float
    sentiment_label: str
    talk_time_distribution: Dict[str, float]
    key_moments: List[Dict[str, Any]]
    follow_up_questions: List[str]
    decisions_made: List[str]
    risks_identified: List[str]
    knowledge_graph_updates: Dict[str, Any]


class MeetingAnalyzer:
    """
    LLM-powered meeting analyzer
    
    Features:
    - Automatic summarization
    - Action item extraction
    - Topic detection
    - Sentiment analysis
    - Talk time analytics
    - Key moment identification
    - Pre-meeting brief generation
    """
    
    def __init__(
        self,
        llm_provider: str = "openai",
        api_key: Optional[str] = None,
        model: str = "gpt-4o-mini"
    ):
        self.llm_provider = llm_provider
        self.api_key = api_key
        self.model = model
        
        if api_key:
            if llm_provider == "openai":
                import os
                os.environ["OPENAI_API_KEY"] = api_key
            elif llm_provider == "anthropic":
                import os
                os.environ["ANTHROPIC_API_KEY"] = api_key
    
    def analyze_meeting(
        self,
        transcript: List[Dict[str, Any]],
        meeting_title: str = "",
        previous_meetings: List[str] = None
    ) -> AnalysisResult:
        """
        Analyze complete meeting transcript
        
        Args:
            transcript: List of transcript segments with speaker info
            meeting_title: Title of the meeting
            previous_meetings: Optional summaries of previous meetings
            
        Returns:
            AnalysisResult with all insights
        """
        # Format transcript for LLM
        formatted_transcript = self._format_transcript(transcript)
        
        # Build analysis prompt
        prompt = self._build_analysis_prompt(
            formatted_transcript,
            meeting_title,
            previous_meetings
        )
        
        # Get LLM response
        llm_response = self._call_llm(prompt)
        
        # Parse response
        result = self._parse_llm_response(llm_response, transcript)
        
        return result
    
    def _format_transcript(
        self,
        transcript: List[Dict[str, Any]]
    ) -> str:
        """Format transcript for LLM consumption"""
        lines = []
        for segment in transcript:
            speaker = segment.get("speaker", "Unknown")
            text = segment.get("text", "")
            lines.append(f"[{speaker}]: {text}")
        
        return "\n".join(lines)
    
    def _build_analysis_prompt(
        self,
        transcript: str,
        meeting_title: str,
        previous_meetings: List[str] = None
    ) -> str:
        """Build comprehensive analysis prompt"""
        
        context = ""
        if previous_meetings:
            context = "\n\nPrevious Meeting Summaries:\n"
            for i, summary in enumerate(previous_meetings, 1):
                context += f"\nMeeting {i}:\n{summary}\n"
        
        prompt = f"""You are an expert meeting analyst. Analyze the following meeting transcript and provide comprehensive insights.

Meeting Title: {meeting_title}
{context}

=== TRANSCRIPT ===
{transcript}
=== END TRANSCRIPT ===

Provide your analysis in JSON format with the following structure:

{{
    "summary": "Concise 3-5 sentence summary of the meeting",
    "key_topics": ["topic1", "topic2", ...],
    "action_items": [
        {{
            "task": "description",
            "assignee": "person name or email",
            "due_date": "YYYY-MM-DD or null",
            "priority": "high|medium|low"
        }}
    ],
    "sentiment": {{
        "score": 0.0 to 1.0,
        "label": "positive|neutral|negative"
    }},
    "key_moments": [
        {{
            "timestamp": "approximate time or description",
            "description": "what happened",
            "importance": "high|medium|low"
        }}
    ],
    "decisions_made": ["decision1", "decision2", ...],
    "follow_up_questions": ["question1", "question2", ...],
    "risks_identified": ["risk1", "risk2", ...],
    "talk_time_analysis": {{
        "speaker1": percentage,
        "speaker2": percentage
    }}
}}

Be specific and actionable. Extract exact quotes when relevant."""

        return prompt
    
    def _call_llm(self, prompt: str) -> str:
        """Call LLM API"""
        if self.llm_provider == "openai":
            return self._call_openai(prompt)
        elif self.llm_provider == "anthropic":
            return self._call_anthropic(prompt)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.llm_provider}")
    
    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        from openai import OpenAI
        
        client = OpenAI()
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert meeting analyst. Always respond with valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=2000,
        )
        
        return response.choices[0].message.content
    
    def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic API"""
        from anthropic import Anthropic
        
        client = Anthropic()
        
        response = client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        return response.content[0].text
    
    def _parse_llm_response(
        self,
        response: str,
        transcript: List[Dict[str, Any]]
    ) -> AnalysisResult:
        """Parse LLM response into AnalysisResult"""
        # Extract JSON from response
        try:
            # Find JSON in response (might be wrapped in markdown)
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
            else:
                data = json.loads(response)
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
            data = self._create_fallback_response()
        
        # Calculate talk time from transcript
        talk_time = self._calculate_talk_time(transcript)
        
        result = AnalysisResult(
            summary=data.get("summary", ""),
            key_topics=data.get("key_topics", []),
            action_items=data.get("action_items", []),
            sentiment_score=data.get("sentiment", {}).get("score", 0.5),
            sentiment_label=data.get("sentiment", {}).get("label", "neutral"),
            talk_time_distribution=talk_time,
            key_moments=data.get("key_moments", []),
            follow_up_questions=data.get("follow_up_questions", []),
            decisions_made=data.get("decisions_made", []),
            risks_identified=data.get("risks_identified", []),
            knowledge_graph_updates=self._extract_knowledge_graph(data, transcript)
        )
        
        return result
    
    def _calculate_talk_time(
        self,
        transcript: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Calculate talk time distribution per speaker"""
        speaker_times = {}
        total_time = 0
        
        for segment in transcript:
            speaker = segment.get("speaker", "Unknown")
            start = segment.get("start", 0)
            end = segment.get("end", 0)
            duration = end - start
            
            speaker_times[speaker] = speaker_times.get(speaker, 0) + duration
            total_time += duration
        
        # Convert to percentages
        if total_time > 0:
            return {
                speaker: round((time / total_time) * 100, 2)
                for speaker, time in speaker_times.items()
            }
        
        return {}
    
    def _extract_knowledge_graph(
        self,
        data: Dict[str, Any],
        transcript: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Extract knowledge graph updates from analysis"""
        # Extract entities and relationships
        entities = []
        relationships = []
        
        for topic in data.get("key_topics", []):
            entities.append({
                "name": topic,
                "type": "topic"
            })
        
        for decision in data.get("decisions_made", []):
            entities.append({
                "name": decision[:50],
                "type": "decision"
            })
        
        return {
            "entities": entities,
            "relationships": relationships
        }
    
    def _create_fallback_response(self) -> Dict[str, Any]:
        """Create fallback response if JSON parsing fails"""
        return {
            "summary": "Analysis failed to parse.",
            "key_topics": [],
            "action_items": [],
            "sentiment": {"score": 0.5, "label": "neutral"},
            "key_moments": [],
            "decisions_made": [],
            "follow_up_questions": [],
            "risks_identified": [],
            "talk_time_analysis": {}
        }
    
    def generate_pre_meeting_brief(
        self,
        meeting_title: str,
        participants: List[str],
        previous_meetings: List[AnalysisResult]
    ) -> str:
        """
        Generate pre-meeting brief from previous meetings
        
        Args:
            meeting_title: Title of upcoming meeting
            participants: List of participant names
            previous_meetings: Results from previous related meetings
            
        Returns:
            Pre-meeting brief text
        """
        prompt = f"""Generate a concise pre-meeting brief for:

Meeting: {meeting_title}
Participants: {', '.join(participants)}

Previous Meeting Summaries:
"""
        
        for i, result in enumerate(previous_meetings[-3:], 1):  # Last 3 meetings
            prompt += f"\n{i}. {result.summary}\n"
            if result.action_items:
                prompt += "   Action Items:\n"
                for item in result.action_items[:3]:
                    prompt += f"   - {item.get('task', '')}\n"
        
        prompt += """
Generate a brief that includes:
1. Context from previous discussions
2. Pending action items
3. Key topics likely to be discussed
4. Questions to consider

Keep it under 200 words."""

        return self._call_llm(prompt)
    
    def generate_quiz(
        self,
        transcript: List[Dict[str, Any]],
        num_questions: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generate quiz questions from educational meeting
        
        Args:
            transcript: Meeting transcript
            num_questions: Number of questions to generate
            
        Returns:
            List of quiz questions with answers
        """
        formatted_transcript = self._format_transcript(transcript)
        
        prompt = f"""Generate {num_questions} quiz questions based on this educational meeting transcript:

=== TRANSCRIPT ===
{formatted_transcript}
=== END TRANSCRIPT ===

Return JSON array of questions:
[
    {{
        "question": "question text",
        "type": "multiple_choice|short_answer|true_false",
        "options": ["A", "B", "C", "D"],  // for multiple choice
        "answer": "correct answer",
        "explanation": "why this is correct"
    }}
]"""

        response = self._call_llm(prompt)
        
        try:
            import re
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        return []
