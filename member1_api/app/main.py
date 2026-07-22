from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import db

app = FastAPI(
    title="PWNDORA RiskView360 API",
    description="CISO Posture Intelligence & Risk Metrics Engine",
    version="1.0.0"
)

# Enable CORS so React frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/health")
def health_check():
    return {"status": "ok", "service": "PWNDORA Backend Active"}

@app.get("/api/v1/employees")
def get_employees():
    return {"count": len(db.employees), "data": db.employees}

@app.get("/api/v1/labs")
def get_labs():
    return {"count": len(db.labs), "data": db.labs}

@app.get("/api/v1/metrics")
def get_metrics():
    return {
        "global_risk_score": 78,
        "mitre_coverage_percentage": 64,
        "nist_readiness": "High",
        "nist_breakdown": {
            "Identify": 80,
            "Protect": 72,
            "Detect": 64,
            "Respond": 58,
            "Recover": 50
        }
    }