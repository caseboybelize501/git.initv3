from typing import Dict, List


def get_host_matrix() -> Dict[str, Dict]:
    return {
        'vercel': {
            'name': 'Vercel',
            'description': 'Next.js, static, API routes',
            'free': True,
            'cold_start': 'no',
            'scoring': 10
        },
        'render': {
            'name': 'Render',
            'description': 'Node/Python web services',
            'free': True,
            'cold_start': '50s',
            'scoring': 8
        },
        'railway': {
            'name': 'Railway',
            'description': 'Any Docker container',
            'free': True,
            'cold_start': 'unknown',
            'scoring': 7
        },
        'fly.io': {
            'name': 'Fly.io',
            'description': 'Docker + persistent VMs',
            'free': True,
            'cold_start': 'no',
            'scoring': 9
        },
        'netlify': {
            'name': 'Netlify',
            'description': 'Static + serverless functions',
            'free': True,
            'cold_start': 'functions',
            'scoring': 6
        },
        'cloudflare_pages': {
            'name': 'Cloudflare Pages',
            'description': 'Static + Workers',
            'free': True,
            'cold_start': 'no',
            'scoring': 10
        },
        'supabase': {
            'name': 'Supabase',
            'description': 'PostgreSQL + Auth + Storage',
            'free': True,
            'cold_start': 'no',
            'scoring': 8
        },
        'neon': {
            'name': 'Neon',
            'description': 'Serverless Postgres',
            'free': True,
            'cold_start': '100ms',
            'scoring': 7
        },
        'huggingface_spaces': {
            'name': 'HuggingFace Spaces',
            'description': 'ML demos, Gradio, Streamlit',
            'free': True,
            'cold_start': 'unknown',
            'scoring': 9
        }
    }


def score_host_selection(plan: Dict, host_matrix: Dict) -> List[Dict]:
    # Simple scoring based on plan characteristics
    scores = []
    
    for host_name, host_info in host_matrix.items():
        score = 0
        
        # Check if host supports the stack
        if 'python' in plan.get('stack', []) and host_info['name'] in ['Render', 'Vercel', 'Fly.io']:
            score += 3
        elif 'node' in plan.get('stack', []) and host_info['name'] in ['Vercel', 'Render', 'Fly.io']:
            score += 3
        
        # Check cold start preference
        if host_info['cold_start'] == 'no':
            score += 2
        elif host_info['cold_start'] == '100ms':
            score += 1
        
        scores.append({
            'host': host_name,
            'score': score,
            'info': host_info
        })
    
    # Sort by score descending
    scores.sort(key=lambda x: x['score'], reverse=True)
    return scores