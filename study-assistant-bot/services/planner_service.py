"""
Study Planner Service
Generate personalized study plans
"""

from typing import Optional, Dict, List
from datetime import datetime, timedelta
from services.ai_service import AIService
from utils.logger import logger


class PlannerService:
    """Service for generating and managing study plans"""

    def __init__(self):
        """Initialize planner service"""
        self.ai_service = AIService()

    def generate_study_plan(
        self,
        subjects: List[str],
        exam_date: str,
        available_hours: float,
        current_level: str = "intermediate",
        goals: str = "",
    ) -> Optional[Dict]:
        """
        Generate personalized study plan

        Args:
            subjects: List of subjects to study
            exam_date: Exam date in format YYYY-MM-DD
            available_hours: Available study hours per day
            current_level: Current knowledge level
            goals: Specific goals or notes

        Returns:
            Dictionary with study plan or None
        """
        try:
            # Calculate days until exam
            exam_datetime = datetime.strptime(exam_date, "%Y-%m-%d")
            today = datetime.now()
            days_remaining = (exam_datetime - today).days

            if days_remaining <= 0:
                logger.error("Exam date must be in the future")
                return None

            subjects_text = ", ".join(subjects)
            goals_text = f"Goals: {goals}\n" if goals else ""

            prompt = f"""Create a detailed study plan for the following:

Subjects: {subjects_text}
Exam Date: {exam_date}
Days Remaining: {days_remaining}
Available Study Hours/Day: {available_hours}
Current Level: {current_level}
{goals_text}

Create a JSON study plan with:
1. "overview": Overall strategy (2-3 sentences)
2. "daily_breakdown": Dict mapping week numbers to study schedules
3. "subject_focus": Dict mapping subjects to recommended hours per week
4. "milestones": List of weekly milestones to achieve
5. "tips": List of study tips for this plan
6. "resources": List of recommended resource types

Return ONLY valid JSON."""

            system_prompt = "You are an expert academic advisor. Create realistic, personalized study plans."

            response = self.ai_service.generate_json(prompt, system_prompt=system_prompt)

            if response:
                response["exam_date"] = exam_date
                response["days_remaining"] = days_remaining
                response["created_at"] = datetime.now().isoformat()
                return response

            return None

        except Exception as e:
            logger.error(f"Error generating study plan: {e}")
            return None

    def generate_weekly_schedule(
        self,
        subjects: List[str],
        available_hours: float,
        difficulty_preference: str = "balanced",
    ) -> Optional[Dict]:
        """
        Generate weekly study schedule

        Args:
            subjects: Subjects to study
            available_hours: Available hours per day
            difficulty_preference: How to distribute difficulty (morning_hard, evening_hard, balanced)

        Returns:
            Weekly schedule or None
        """
        try:
            subjects_text = ", ".join(subjects)
            total_weekly_hours = available_hours * 6  # Monday-Saturday

            prompt = f"""Create a detailed weekly study schedule:

Subjects: {subjects_text}
Total Weekly Hours Available: {total_weekly_hours}
Daily Hours Available: {available_hours}
Difficulty Distribution: {difficulty_preference}

Generate a JSON schedule with:
- "monday" through "saturday": Daily schedule objects containing:
  - "morning_session": {{ "subject": "...", "duration": X, "activity": "..." }}
  - "afternoon_session": {{ "subject": "...", "duration": X, "activity": "..." }}
  - "evening_session": {{ "subject": "...", "duration": X, "activity": "..." }}
  - "break_times": List of recommended break times
- "weekly_focus": Focus areas for the week
- "review_sessions": Recommended review times

Return ONLY valid JSON."""

            system_prompt = "You are an expert in scheduling and time management. Create effective study schedules."

            return self.ai_service.generate_json(prompt, system_prompt=system_prompt)

        except Exception as e:
            logger.error(f"Error generating weekly schedule: {e}")
            return None

    def generate_revision_schedule(
        self,
        total_content_hours: float,
        available_hours: float,
        days_until_exam: int,
        subjects: List[str],
    ) -> Optional[Dict]:
        """
        Generate revision schedule using spaced repetition

        Args:
            total_content_hours: Total hours of content to revise
            available_hours: Available hours per day
            days_until_exam: Days until exam
            subjects: Subjects to revise

        Returns:
            Revision schedule or None
        """
        try:
            subjects_text = ", ".join(subjects)

            prompt = f"""Create a spaced repetition revision schedule:

Subjects: {subjects_text}
Total Content Hours: {total_content_hours}
Available Daily Hours: {available_hours}
Days Until Exam: {days_until_exam}

Generate a JSON schedule using spaced repetition principles:
- "revision_phases": List of revision phases (Phase 1 to N)
- "daily_schedule": Dict mapping day numbers to revision tasks
- "spacing_intervals": Recommended spacing between revisions (2 days, 7 days, etc.)
- "cumulative_revisions": How many times each subject should be revised
- "final_week_plan": Special plan for the final week
- "exam_day_tips": Tips for exam day

Return ONLY valid JSON."""

            system_prompt = "You are an expert in spaced repetition and exam preparation. Create effective revision schedules."

            return self.ai_service.generate_json(prompt, system_prompt=system_prompt)

        except Exception as e:
            logger.error(f"Error generating revision schedule: {e}")
            return None

    def generate_focused_session(
        self,
        subject: str,
        duration_minutes: int,
        focus_area: str = "",
    ) -> Optional[Dict]:
        """
        Generate focused study session plan

        Args:
            subject: Subject to study
            duration_minutes: Duration of session
            focus_area: Specific area to focus on

        Returns:
            Session plan or None
        """
        try:
            focus_text = f" (Focus: {focus_area})" if focus_area else ""

            prompt = f"""Create a focused study session plan:

Subject: {subject}{focus_text}
Duration: {duration_minutes} minutes

Generate a JSON session plan with:
- "overview": What will be covered
- "warm_up": 5-minute warm-up activity
- "main_study": Main content with time breakdown
- "active_recall": Active recall/practice questions
- "cool_down": Final 5-minute summary
- "key_takeaways": Main points to remember
- "next_session_prep": Preparation for next session

Return ONLY valid JSON."""

            system_prompt = "You are an expert in focused study sessions. Create structured, effective study plans."

            return self.ai_service.generate_json(prompt, system_prompt=system_prompt)

        except Exception as e:
            logger.error(f"Error generating focused session: {e}")
            return None

    def calculate_study_pace(
        self,
        total_topics: int,
        available_hours: float,
        days_remaining: int,
    ) -> Dict:
        """
        Calculate study pace recommendations

        Args:
            total_topics: Total number of topics
            available_hours: Available hours per day
            days_remaining: Days until exam

        Returns:
            Study pace statistics
        """
        try:
            total_available_hours = available_hours * days_remaining
            hours_per_topic = total_available_hours / total_topics if total_topics > 0 else 0

            # Calculate with 20% buffer for revision
            study_days = int(days_remaining * 0.8)
            hours_per_topic_tight = total_available_hours / total_topics if total_topics > 0 else 0

            return {
                "total_available_hours": total_available_hours,
                "hours_per_topic": round(hours_per_topic, 2),
                "study_days": study_days,
                "topics_per_day": round(total_topics / study_days, 2) if study_days > 0 else 0,
                "pace_recommendation": self._get_pace_recommendation(hours_per_topic),
                "feasibility": self._assess_feasibility(total_topics, available_hours, days_remaining),
            }

        except Exception as e:
            logger.error(f"Error calculating study pace: {e}")
            return {}

    @staticmethod
    def _get_pace_recommendation(hours_per_topic: float) -> str:
        """Get pace recommendation based on hours per topic"""
        if hours_per_topic >= 3:
            return "Relaxed pace - plenty of time for deep learning and revision"
        elif hours_per_topic >= 1.5:
            return "Moderate pace - balanced learning and revision"
        elif hours_per_topic >= 0.75:
            return "Fast pace - focus on core concepts"
        else:
            return "Very fast pace - prioritize high-weight topics"

    @staticmethod
    def _assess_feasibility(total_topics: int, available_hours: float, days_remaining: int) -> str:
        """Assess feasibility of study plan"""
        total_hours = available_hours * days_remaining
        minimum_hours_needed = total_topics * 0.5  # Minimum 30 min per topic

        if total_hours < minimum_hours_needed:
            return "Challenging - may need to prioritize topics"
        elif total_hours < minimum_hours_needed * 1.5:
            return "Tight - requires consistent effort"
        elif total_hours < minimum_hours_needed * 3:
            return "Feasible - achievable with good discipline"
        else:
            return "Very feasible - comfortable pace possible"

    def format_plan_for_display(self, plan: Dict) -> str:
        """
        Format study plan for display

        Args:
            plan: Study plan dictionary

        Returns:
            Formatted text
        """
        try:
            text = "📅 Study Plan\n" + "=" * 40 + "\n"

            if "overview" in plan:
                text += f"Overview:\n{plan['overview']}\n\n"

            if "days_remaining" in plan:
                text += f"Days Until Exam: {plan['days_remaining']}\n"

            if "subject_focus" in plan:
                text += "\nSubject Focus:\n"
                for subject, hours in plan["subject_focus"].items():
                    text += f"  • {subject}: {hours} hours/week\n"

            if "milestones" in plan:
                text += "\nKey Milestones:\n"
                for milestone in plan["milestones"][:5]:  # First 5
                    text += f"  • {milestone}\n"

            if "tips" in plan:
                text += "\nStudy Tips:\n"
                for tip in plan["tips"][:3]:  # First 3
                    text += f"  • {tip}\n"

            return text

        except Exception as e:
            logger.error(f"Error formatting plan: {e}")
            return "Error displaying study plan"
