import json
from typing import Dict, Any
from pydantic import BaseModel


class AdjudicatorAgent:
    def __init__(self):
        pass

    async def make_final_ruling(self, plan: Dict, feedbacks: Dict) -> Dict:
        # Collect all verdicts
        arch_verdict = feedbacks.get('architecture', {}).get('verdict', 'APPROVED')
        deploy_verdict = feedbacks.get('deployment', {}).get('verdict', 'APPROVED')
        security_verdict = feedbacks.get('security', {}).get('verdict', 'APPROVED')
        
        # Check confidence levels
        arch_confidence = feedbacks.get('architecture', {}).get('confidence', 0.0)
        deploy_confidence = feedbacks.get('deployment', {}).get('confidence', 0.0)
        security_confidence = feedbacks.get('security', {}).get('confidence', 0.0)
        
        # If all approved and confidence is high enough
        if (arch_verdict == 'APPROVED' and 
            deploy_verdict == 'APPROVED' and 
            security_verdict == 'APPROVED' and
            arch_confidence >= 0.6 and
            deploy_confidence >= 0.6 and
            security_confidence >= 0.6):
            
            # Update plan status
            plan['plan_status'] = 'approved'
            
            return {
                'ruling': 'approved',
                'revised_plan': None,
                'revision_summary': '',
                'escalate_to_user': False
            }
        else:
            # Need revision or escalation
            return {
                'ruling': 'failed',
                'revised_plan': None,
                'revision_summary': 'Plan failed validation - requires user review',
                'escalate_to_user': True
            }