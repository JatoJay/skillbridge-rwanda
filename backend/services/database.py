import json
import uuid
from datetime import datetime
from typing import Optional
from pathlib import Path


class InMemoryDatabase:
    def __init__(self):
        self.candidates: dict[str, dict] = {}
        self.jobs: dict[str, dict] = {}
        self.chat_sessions: dict[str, list] = {}
        self.matches: list[dict] = []
        self._load_seed_data()

    def _load_seed_data(self):
        seed_jobs = [
            {"title": "Senior Software Engineer", "company": "Andela", "description": "We are looking for a Senior Software Engineer to join our distributed team. You will work on building scalable web applications using modern technologies.", "required_skills": ["JavaScript", "React", "Node.js", "AWS", "PostgreSQL"], "preferred_skills": ["TypeScript", "Docker", "Kubernetes"], "experience_level": "senior", "sector": "ICT", "location": "Kigali", "salary_range": "RWF 2,000,000 - 4,000,000", "employment_type": "full-time"},
            {"title": "Data Analyst", "company": "Bank of Kigali", "description": "Join our analytics team to drive data-driven decision making across the bank. You will analyze large datasets, create visualizations, and provide insights.", "required_skills": ["SQL", "Python", "Excel", "Data Visualization", "Statistics"], "preferred_skills": ["Tableau", "Power BI", "Machine Learning"], "experience_level": "mid", "sector": "Finance", "location": "Kigali", "salary_range": "RWF 800,000 - 1,500,000", "employment_type": "full-time"},
            {"title": "Mobile Developer", "company": "MTN Rwanda", "description": "Develop and maintain mobile applications for our growing customer base. Experience with both Android and iOS development is essential.", "required_skills": ["Android", "Kotlin", "iOS", "Swift", "REST APIs"], "preferred_skills": ["Flutter", "React Native", "Firebase"], "experience_level": "mid", "sector": "ICT", "location": "Kigali", "salary_range": "RWF 1,200,000 - 2,000,000", "employment_type": "full-time"},
            {"title": "DevOps Engineer", "company": "Norrsken Kigali", "description": "We need a DevOps engineer to manage our cloud infrastructure and CI/CD pipelines. You will work with multiple startups in our hub.", "required_skills": ["Docker", "Kubernetes", "AWS", "CI/CD", "Linux"], "preferred_skills": ["Terraform", "Ansible", "Python"], "experience_level": "mid", "sector": "ICT", "location": "Kigali", "salary_range": "RWF 1,500,000 - 2,500,000", "employment_type": "full-time"},
            {"title": "Junior Web Developer", "company": "Irembo", "description": "Join Rwanda's leading e-government platform. Help build digital services that impact millions of Rwandans.", "required_skills": ["HTML", "CSS", "JavaScript", "Git"], "preferred_skills": ["React", "Vue.js", "Python"], "experience_level": "entry", "sector": "ICT", "location": "Kigali", "salary_range": "RWF 400,000 - 700,000", "employment_type": "full-time"},
            {"title": "Drone Operations Specialist", "company": "Zipline", "description": "Operate and maintain autonomous drone systems delivering medical supplies across Rwanda.", "required_skills": ["Technical Maintenance", "Problem Solving", "Logistics", "English"], "preferred_skills": ["Aviation Knowledge", "Electronics", "Data Analysis"], "experience_level": "entry", "sector": "Healthcare", "location": "Muhanga", "salary_range": "RWF 500,000 - 900,000", "employment_type": "full-time"},
            {"title": "Clinical Officer", "company": "Partners In Health Rwanda", "description": "Provide clinical care in rural health centers with a multidisciplinary team.", "required_skills": ["Clinical Assessment", "Patient Care", "Medical Documentation", "Kinyarwanda"], "preferred_skills": ["French", "HIV/AIDS Management", "Community Health"], "experience_level": "mid", "sector": "Healthcare", "location": "Butaro", "salary_range": "RWF 600,000 - 1,000,000", "employment_type": "full-time"},
            {"title": "Healthcare Administrator", "company": "King Faisal Hospital", "description": "Manage hospital operations and administrative processes. Strong leadership required.", "required_skills": ["Healthcare Management", "Leadership", "Budgeting", "English", "Kinyarwanda"], "preferred_skills": ["MBA", "Project Management", "EHR Systems"], "experience_level": "senior", "sector": "Healthcare", "location": "Kigali", "salary_range": "RWF 1,500,000 - 2,500,000", "employment_type": "full-time"},
            {"title": "Pharmacy Technician", "company": "Rwanda Biomedical Centre", "description": "Support pharmaceutical supply chain and medication dispensing operations.", "required_skills": ["Pharmacy Knowledge", "Inventory Management", "Attention to Detail", "Record Keeping"], "preferred_skills": ["Supply Chain", "Quality Assurance", "Computer Skills"], "experience_level": "entry", "sector": "Healthcare", "location": "Kigali", "salary_range": "RWF 350,000 - 550,000", "employment_type": "full-time"},
            {"title": "Medical Laboratory Scientist", "company": "BIOVAC Rwanda", "description": "Conduct laboratory tests and research. Support vaccine development and quality control.", "required_skills": ["Laboratory Techniques", "Microbiology", "Quality Control", "Research Methods"], "preferred_skills": ["Molecular Biology", "Bioinformatics", "GLP"], "experience_level": "mid", "sector": "Healthcare", "location": "Kigali", "salary_range": "RWF 800,000 - 1,400,000", "employment_type": "full-time"},
            {"title": "Agricultural Extension Officer", "company": "Rwanda Agriculture Board", "description": "Work directly with farmers to improve agricultural practices and productivity.", "required_skills": ["Agriculture", "Training", "Kinyarwanda", "Communication", "Farming Techniques"], "preferred_skills": ["Agronomy", "Climate-Smart Agriculture", "Data Collection"], "experience_level": "entry", "sector": "AgriTech", "location": "Musanze", "salary_range": "RWF 300,000 - 500,000", "employment_type": "full-time"},
            {"title": "AgriTech Product Manager", "company": "Hello Tractor", "description": "Lead product development for agricultural technology platform connecting farmers with services.", "required_skills": ["Product Management", "Agile", "Market Research", "User Research"], "preferred_skills": ["Agriculture Knowledge", "Data Analysis", "Mobile Platforms"], "experience_level": "senior", "sector": "AgriTech", "location": "Kigali", "salary_range": "RWF 1,800,000 - 3,000,000", "employment_type": "full-time"},
            {"title": "Farm Manager", "company": "Inyange Industries", "description": "Manage large-scale dairy farming operations. Oversee production and staff.", "required_skills": ["Farm Management", "Livestock Management", "Team Leadership", "Quality Control"], "preferred_skills": ["Dairy Science", "Business Management", "Veterinary Knowledge"], "experience_level": "mid", "sector": "AgriTech", "location": "Rwamagana", "salary_range": "RWF 700,000 - 1,200,000", "employment_type": "full-time"},
            {"title": "Irrigation Technician", "company": "Rwanda Water Resources Board", "description": "Install and maintain irrigation systems for agricultural projects.", "required_skills": ["Irrigation Systems", "Technical Maintenance", "Water Management", "Field Work"], "preferred_skills": ["Plumbing", "Solar Systems", "GIS"], "experience_level": "entry", "sector": "AgriTech", "location": "Eastern Province", "salary_range": "RWF 280,000 - 450,000", "employment_type": "full-time"},
            {"title": "Agricultural Data Scientist", "company": "One Acre Fund", "description": "Use data science to improve agricultural outcomes for smallholder farmers.", "required_skills": ["Python", "Machine Learning", "Statistics", "SQL", "Data Visualization"], "preferred_skills": ["R", "Remote Sensing", "Agriculture Knowledge"], "experience_level": "mid", "sector": "AgriTech", "location": "Kigali", "salary_range": "RWF 1,200,000 - 2,200,000", "employment_type": "full-time"},
            {"title": "Financial Analyst", "company": "I&M Bank Rwanda", "description": "Analyze financial data and prepare reports for senior management.", "required_skills": ["Financial Analysis", "Excel", "Financial Modeling", "Reporting"], "preferred_skills": ["CFA", "Bloomberg Terminal", "Python"], "experience_level": "mid", "sector": "Finance", "location": "Kigali", "salary_range": "RWF 900,000 - 1,600,000", "employment_type": "full-time"},
            {"title": "Loan Officer", "company": "BPR Bank", "description": "Evaluate loan applications and build relationships with clients.", "required_skills": ["Credit Analysis", "Customer Service", "Kinyarwanda", "Sales", "Financial Assessment"], "preferred_skills": ["Microfinance", "SME Banking", "French"], "experience_level": "entry", "sector": "Finance", "location": "Rubavu", "salary_range": "RWF 350,000 - 600,000", "employment_type": "full-time"},
            {"title": "Mobile Money Operations Manager", "company": "MTN Mobile Money", "description": "Oversee mobile money operations and agent network. Drive financial inclusion.", "required_skills": ["Operations Management", "Mobile Money", "Team Leadership", "Analytics"], "preferred_skills": ["Fintech", "Fraud Prevention", "Customer Experience"], "experience_level": "senior", "sector": "Finance", "location": "Kigali", "salary_range": "RWF 2,000,000 - 3,500,000", "employment_type": "full-time"},
            {"title": "Accountant", "company": "PwC Rwanda", "description": "Provide accounting and audit services to diverse clients in a Big 4 firm.", "required_skills": ["Accounting", "IFRS", "Auditing", "Excel", "Financial Statements"], "preferred_skills": ["ACCA", "CPA", "Tax"], "experience_level": "entry", "sector": "Finance", "location": "Kigali", "salary_range": "RWF 450,000 - 800,000", "employment_type": "full-time"},
            {"title": "Insurance Underwriter", "company": "Sanlam Rwanda", "description": "Assess insurance applications and determine coverage terms.", "required_skills": ["Risk Assessment", "Insurance Knowledge", "Analysis", "Communication"], "preferred_skills": ["Actuarial Basics", "Customer Service", "Data Analysis"], "experience_level": "mid", "sector": "Finance", "location": "Kigali", "salary_range": "RWF 600,000 - 1,100,000", "employment_type": "full-time"},
            {"title": "Tour Guide", "company": "Thousand Hills Expeditions", "description": "Lead tourists through Rwanda's landscapes and cultural sites.", "required_skills": ["English", "Kinyarwanda", "Tourism Knowledge", "Customer Service", "Communication"], "preferred_skills": ["French", "German", "Wildlife Knowledge", "First Aid"], "experience_level": "entry", "sector": "Tourism", "location": "Kigali", "salary_range": "RWF 250,000 - 450,000", "employment_type": "full-time"},
            {"title": "Hotel General Manager", "company": "Radisson Blu Kigali", "description": "Lead all aspects of hotel operations. Ensure exceptional guest experiences.", "required_skills": ["Hotel Management", "Leadership", "Operations", "Customer Service", "Budgeting"], "preferred_skills": ["Revenue Management", "F&B Management", "French"], "experience_level": "senior", "sector": "Tourism", "location": "Kigali", "salary_range": "RWF 3,000,000 - 5,000,000", "employment_type": "full-time"},
            {"title": "Wildlife Conservation Officer", "company": "African Parks Rwanda", "description": "Protect endangered wildlife in Akagera National Park.", "required_skills": ["Wildlife Conservation", "Field Work", "Data Collection", "Physical Fitness"], "preferred_skills": ["Biology", "GIS", "Community Engagement"], "experience_level": "mid", "sector": "Tourism", "location": "Akagera", "salary_range": "RWF 500,000 - 850,000", "employment_type": "full-time"},
            {"title": "Events Coordinator", "company": "Kigali Convention Centre", "description": "Plan and execute conferences, weddings, and corporate events.", "required_skills": ["Event Planning", "Communication", "Organization", "Vendor Management"], "preferred_skills": ["Marketing", "Budget Management", "Project Management"], "experience_level": "mid", "sector": "Tourism", "location": "Kigali", "salary_range": "RWF 550,000 - 900,000", "employment_type": "full-time"},
            {"title": "Gorilla Trekking Guide", "company": "Rwanda Development Board - Tourism", "description": "Lead gorilla trekking experiences in Volcanoes National Park.", "required_skills": ["Wildlife Knowledge", "Physical Fitness", "English", "Kinyarwanda", "Customer Service"], "preferred_skills": ["French", "First Aid", "Photography"], "experience_level": "mid", "sector": "Tourism", "location": "Musanze", "salary_range": "RWF 450,000 - 750,000", "employment_type": "full-time"},
            {"title": "Civil Engineer", "company": "RSSB Construction", "description": "Design and oversee construction of infrastructure projects.", "required_skills": ["Civil Engineering", "AutoCAD", "Project Management", "Structural Design"], "preferred_skills": ["BIM", "Primavera", "Green Building"], "experience_level": "mid", "sector": "Construction", "location": "Kigali", "salary_range": "RWF 900,000 - 1,600,000", "employment_type": "full-time"},
            {"title": "Site Supervisor", "company": "NPD Cotraco", "description": "Supervise construction sites and manage work crews.", "required_skills": ["Construction Management", "Team Leadership", "Quality Control", "Safety Management"], "preferred_skills": ["AutoCAD", "MS Project", "Heavy Equipment"], "experience_level": "mid", "sector": "Construction", "location": "Kigali", "salary_range": "RWF 600,000 - 1,000,000", "employment_type": "full-time"},
            {"title": "Architect", "company": "Mass Design Group", "description": "Design impactful buildings that improve community health and wellbeing.", "required_skills": ["Architecture", "AutoCAD", "SketchUp", "Design Thinking", "Building Codes"], "preferred_skills": ["Revit", "Sustainable Design", "Community Engagement"], "experience_level": "mid", "sector": "Construction", "location": "Kigali", "salary_range": "RWF 1,000,000 - 1,800,000", "employment_type": "full-time"},
            {"title": "Quantity Surveyor", "company": "Real Contractors", "description": "Manage construction costs and contracts. Prepare bills of quantities.", "required_skills": ["Quantity Surveying", "Cost Estimation", "Contract Management", "Excel"], "preferred_skills": ["RICS", "Construction Law", "Tender Management"], "experience_level": "mid", "sector": "Construction", "location": "Kigali", "salary_range": "RWF 800,000 - 1,400,000", "employment_type": "full-time"},
            {"title": "Electrician", "company": "STECOL Corporation Rwanda", "description": "Install and maintain electrical systems in construction projects.", "required_skills": ["Electrical Installation", "Wiring", "Safety Standards", "Technical Drawing"], "preferred_skills": ["Solar Installation", "Industrial Electrical", "PLC"], "experience_level": "entry", "sector": "Construction", "location": "Nyagatare", "salary_range": "RWF 300,000 - 500,000", "employment_type": "full-time"},
            {"title": "UI/UX Designer", "company": "Kasha Rwanda", "description": "Design user interfaces for e-commerce platform serving women in Rwanda.", "required_skills": ["Figma", "User Research", "Prototyping", "Visual Design"], "preferred_skills": ["Adobe XD", "Usability Testing", "Mobile Design"], "experience_level": "mid", "sector": "ICT", "location": "Kigali", "salary_range": "RWF 800,000 - 1,400,000", "employment_type": "full-time"},
            {"title": "Marketing Manager", "company": "RwandAir", "description": "Lead digital marketing initiatives and brand strategy for national airline.", "required_skills": ["Digital Marketing", "SEO", "Content Marketing", "Analytics"], "preferred_skills": ["Social Media", "Brand Management", "CRM"], "experience_level": "senior", "sector": "Tourism", "location": "Kigali", "salary_range": "RWF 1,500,000 - 2,500,000", "employment_type": "full-time"},
            {"title": "Customer Service Representative", "company": "Equity Bank Rwanda", "description": "Handle inquiries, resolve complaints, provide excellent banking support.", "required_skills": ["Customer Service", "Communication", "Kinyarwanda", "English", "Problem Solving"], "preferred_skills": ["Banking Knowledge", "French", "CRM Systems"], "experience_level": "entry", "sector": "Finance", "location": "Kigali", "salary_range": "RWF 300,000 - 500,000", "employment_type": "full-time"},
            {"title": "Full Stack Developer", "company": "Kasha Rwanda", "description": "Build web applications using React and Python Django for e-commerce.", "required_skills": ["React", "Python", "Django", "PostgreSQL", "REST APIs"], "preferred_skills": ["TypeScript", "Docker", "AWS"], "experience_level": "mid", "sector": "ICT", "location": "Kigali", "salary_range": "RWF 1,200,000 - 2,000,000", "employment_type": "full-time"},
            {"title": "HR Manager", "company": "Bralirwa", "description": "Lead human resources operations for beverage manufacturing company.", "required_skills": ["HR Management", "Recruitment", "Employee Relations", "Labor Law"], "preferred_skills": ["HRIS", "Training Development", "Compensation"], "experience_level": "senior", "sector": "Manufacturing", "location": "Kigali", "salary_range": "RWF 1,500,000 - 2,500,000", "employment_type": "full-time"},
            {"title": "Supply Chain Coordinator", "company": "Sulfo Rwanda", "description": "Coordinate supply chain operations for FMCG distribution.", "required_skills": ["Supply Chain", "Logistics", "Inventory Management", "Excel"], "preferred_skills": ["ERP Systems", "Procurement", "Negotiation"], "experience_level": "mid", "sector": "Retail", "location": "Kigali", "salary_range": "RWF 700,000 - 1,200,000", "employment_type": "full-time"},
            {"title": "Sales Executive", "company": "Airtel Rwanda", "description": "Drive sales growth for telecom products and services.", "required_skills": ["Sales", "Negotiation", "Customer Relationships", "Communication"], "preferred_skills": ["Telecom Knowledge", "B2B Sales", "CRM"], "experience_level": "mid", "sector": "ICT", "location": "Kigali", "salary_range": "RWF 600,000 - 1,000,000", "employment_type": "full-time"},
            {"title": "Quality Assurance Engineer", "company": "Volkswagen Rwanda", "description": "Ensure quality standards in vehicle assembly operations.", "required_skills": ["Quality Control", "ISO Standards", "Testing", "Documentation"], "preferred_skills": ["Six Sigma", "Automotive", "Process Improvement"], "experience_level": "mid", "sector": "Manufacturing", "location": "Kigali", "salary_range": "RWF 800,000 - 1,400,000", "employment_type": "full-time"},
            {"title": "Cybersecurity Analyst", "company": "Bank of Kigali", "description": "Protect banking systems from cyber threats and ensure compliance.", "required_skills": ["Cybersecurity", "Network Security", "Threat Analysis", "SIEM"], "preferred_skills": ["Penetration Testing", "CISSP", "Cloud Security"], "experience_level": "mid", "sector": "Finance", "location": "Kigali", "salary_range": "RWF 1,200,000 - 2,000,000", "employment_type": "full-time"},
            {"title": "Nurse", "company": "CHUK Hospital", "description": "Provide nursing care in university teaching hospital.", "required_skills": ["Nursing", "Patient Care", "Medical Documentation", "Kinyarwanda"], "preferred_skills": ["Critical Care", "French", "Emergency Care"], "experience_level": "mid", "sector": "Healthcare", "location": "Kigali", "salary_range": "RWF 400,000 - 700,000", "employment_type": "full-time"},
            {"title": "Teacher - Secondary School", "company": "Green Hills Academy", "description": "Teach secondary students in international school setting.", "required_skills": ["Teaching", "Subject Expertise", "English", "Classroom Management"], "preferred_skills": ["IB Curriculum", "EdTech", "Student Counseling"], "experience_level": "mid", "sector": "Education", "location": "Kigali", "salary_range": "RWF 600,000 - 1,000,000", "employment_type": "full-time"},
            {"title": "Procurement Officer", "company": "Rwanda Energy Group", "description": "Manage procurement processes for energy infrastructure projects.", "required_skills": ["Procurement", "Contract Management", "Supplier Relations", "Negotiation"], "preferred_skills": ["ERP Systems", "Energy Sector", "Tender Management"], "experience_level": "mid", "sector": "Energy", "location": "Kigali", "salary_range": "RWF 700,000 - 1,200,000", "employment_type": "full-time"},
            {"title": "Graphic Designer", "company": "Rwanda Broadcasting Agency", "description": "Create visual content for national broadcasting.", "required_skills": ["Adobe Photoshop", "Adobe Illustrator", "Visual Design", "Typography"], "preferred_skills": ["Motion Graphics", "Video Editing", "Branding"], "experience_level": "mid", "sector": "Media", "location": "Kigali", "salary_range": "RWF 500,000 - 900,000", "employment_type": "full-time"},
            {"title": "Environmental Specialist", "company": "REMA", "description": "Monitor environmental compliance and conduct impact assessments.", "required_skills": ["Environmental Science", "EIA", "Data Analysis", "Report Writing"], "preferred_skills": ["GIS", "Policy Analysis", "Climate Change"], "experience_level": "mid", "sector": "Environment", "location": "Kigali", "salary_range": "RWF 800,000 - 1,400,000", "employment_type": "full-time"},
            {"title": "Chef de Cuisine", "company": "Marriott Kigali", "description": "Lead kitchen operations in international hotel.", "required_skills": ["Culinary Arts", "Kitchen Management", "Menu Planning", "Food Safety"], "preferred_skills": ["International Cuisine", "Cost Control", "Team Training"], "experience_level": "senior", "sector": "Tourism", "location": "Kigali", "salary_range": "RWF 1,200,000 - 2,000,000", "employment_type": "full-time"},
            {"title": "Legal Counsel", "company": "Development Bank of Rwanda", "description": "Provide legal advisory services for development finance.", "required_skills": ["Legal Analysis", "Contract Law", "Regulatory Compliance", "English"], "preferred_skills": ["Banking Law", "Corporate Law", "French"], "experience_level": "senior", "sector": "Finance", "location": "Kigali", "salary_range": "RWF 2,000,000 - 3,500,000", "employment_type": "full-time"},
            {"title": "Mechanical Engineer", "company": "CIMERWA", "description": "Maintain and optimize cement manufacturing equipment.", "required_skills": ["Mechanical Engineering", "Maintenance", "Troubleshooting", "AutoCAD"], "preferred_skills": ["Industrial Equipment", "Process Engineering", "PLC"], "experience_level": "mid", "sector": "Manufacturing", "location": "Rusizi", "salary_range": "RWF 900,000 - 1,500,000", "employment_type": "full-time"},
            {"title": "Research Associate", "company": "African Institute for Mathematical Sciences", "description": "Conduct research in data science and AI applications.", "required_skills": ["Research Methods", "Python", "Statistics", "Machine Learning"], "preferred_skills": ["PhD", "Publications", "Grant Writing"], "experience_level": "mid", "sector": "Education", "location": "Kigali", "salary_range": "RWF 1,000,000 - 1,800,000", "employment_type": "full-time"},
            {"title": "Warehouse Manager", "company": "BPN Rwanda", "description": "Manage warehouse operations for gas distribution.", "required_skills": ["Warehouse Management", "Inventory Control", "Logistics", "Team Leadership"], "preferred_skills": ["WMS", "Safety Management", "Fleet Management"], "experience_level": "mid", "sector": "Logistics", "location": "Kigali", "salary_range": "RWF 700,000 - 1,200,000", "employment_type": "full-time"}
        ]
        for job in seed_jobs:
            job_id = str(uuid.uuid4())
            job["id"] = job_id
            job["created_at"] = datetime.now().isoformat()
            job["is_active"] = True
            self.jobs[job_id] = job

    async def create_candidate(self, profile: dict) -> str:
        candidate_id = str(uuid.uuid4())
        profile["id"] = candidate_id
        profile["created_at"] = datetime.now().isoformat()
        profile["updated_at"] = datetime.now().isoformat()
        self.candidates[candidate_id] = profile
        return candidate_id

    async def get_candidate(self, candidate_id: str) -> Optional[dict]:
        return self.candidates.get(candidate_id)

    async def update_candidate(self, candidate_id: str, profile: dict):
        if candidate_id in self.candidates:
            profile["updated_at"] = datetime.now().isoformat()
            self.candidates[candidate_id].update(profile)

    async def get_all_candidates(self) -> list[dict]:
        return list(self.candidates.values())

    async def create_job(self, job: dict) -> str:
        job_id = str(uuid.uuid4())
        job["id"] = job_id
        job["created_at"] = datetime.now().isoformat()
        job["is_active"] = True
        self.jobs[job_id] = job
        return job_id

    async def get_job(self, job_id: str) -> Optional[dict]:
        return self.jobs.get(job_id)

    async def get_all_jobs(self) -> list[dict]:
        return list(self.jobs.values())

    async def get_active_jobs(self) -> list[dict]:
        return [j for j in self.jobs.values() if j.get("is_active", True)]

    async def save_chat_session(self, session_id: str, messages: list):
        self.chat_sessions[session_id] = messages

    async def get_chat_session(self, session_id: str) -> list:
        return self.chat_sessions.get(session_id, [])

    async def record_match(self, candidate_id: str, job_id: str, score: float):
        self.matches.append({
            "candidate_id": candidate_id,
            "job_id": job_id,
            "score": score,
            "created_at": datetime.now().isoformat()
        })

    async def get_insights(self) -> dict:
        skill_counts = {}
        for job in self.jobs.values():
            for skill in job.get("required_skills", []):
                skill_counts[skill] = skill_counts.get(skill, 0) + 1

        sector_counts = {}
        for job in self.jobs.values():
            sector = job.get("sector", "Other")
            sector_counts[sector] = sector_counts.get(sector, 0) + 1

        return {
            "top_skills": sorted(
                [{"name": k, "count": v} for k, v in skill_counts.items()],
                key=lambda x: x["count"],
                reverse=True
            )[:10],
            "sectors_hiring": sorted(
                [{"name": k, "count": v} for k, v in sector_counts.items()],
                key=lambda x: x["count"],
                reverse=True
            ),
            "skill_gaps_by_region": [
                {"region": "Kigali", "gap_score": 35},
                {"region": "Northern Province", "gap_score": 55},
                {"region": "Southern Province", "gap_score": 48},
                {"region": "Eastern Province", "gap_score": 52},
                {"region": "Western Province", "gap_score": 50}
            ],
            "total_candidates": len(self.candidates),
            "total_jobs": len(self.jobs),
            "matches_made": len(self.matches)
        }


db = InMemoryDatabase()
