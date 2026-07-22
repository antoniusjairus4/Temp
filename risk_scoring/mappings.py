"""
Mappings and configuration for RiskView360 PWNDORA scoring engine.
"""

# Weights and Scoring Configuration (No magic numbers)
BASE_SCORE_MAX = 100
MAX_STREAK_DAYS = 30
STREAK_BONUS_WEIGHT = 0.1  # Up to 10% of score comes from streak
COMPLETION_RATE_WEIGHT = 0.9  # Up to 90% comes from lab completion and performance

# Tactic and NIST definitions for categorization
TACTICS = [
    "Reconnaissance",
    "Initial Access",
    "Execution",
    "Persistence",
    "Privilege Escalation",
    "Defense Evasion",
    "Credential Access",
    "Discovery",
    "Lateral Movement",
    "Collection",
    "Command and Control",
    "Exfiltration",
    "Impact"
]

NIST_FUNCTIONS = [
    "Identify",
    "Protect",
    "Detect",
    "Respond",
    "Recover"
]

# Detailed ATT&CK Technique Metadata
# Maps Technique ID to its Tactic and NIST function mapping
TECHNIQUE_METADATA = {
    # Reconnaissance
    "T1593": {"name": "Search Open Websites/Domains", "tactic": "Reconnaissance", "nist": "Identify"},
    "T1594": {"name": "Search Victim-Owned Websites", "tactic": "Reconnaissance", "nist": "Identify"},
    "T1590": {"name": "Gather Victim Network Information", "tactic": "Reconnaissance", "nist": "Identify"},

    # Initial Access
    "T1566": {"name": "Phishing", "tactic": "Initial Access", "nist": "Protect"},
    "T1566.001": {"name": "Spearphishing Attachment", "tactic": "Initial Access", "nist": "Protect"},
    "T1566.002": {"name": "Spearphishing Link", "tactic": "Initial Access", "nist": "Protect"},
    "T1190": {"name": "Exploit Public-Facing Application", "tactic": "Initial Access", "nist": "Protect"},
    "T1078": {"name": "Valid Accounts", "tactic": "Initial Access", "nist": "Protect"},

    # Execution
    "T1059": {"name": "Command and Scripting Interpreter", "tactic": "Execution", "nist": "Protect"},
    "T1203": {"name": "Exploitation for Client Execution", "tactic": "Execution", "nist": "Protect"},
    "T1609": {"name": "Container Administration Command", "tactic": "Execution", "nist": "Protect"},

    # Persistence
    "T1098": {"name": "Account Manipulation", "tactic": "Persistence", "nist": "Protect"},
    "T1543": {"name": "Create or Modify System Process", "tactic": "Persistence", "nist": "Protect"},
    "T1505": {"name": "Server Software Component", "tactic": "Persistence", "nist": "Protect"},
    "T1525": {"name": "Implant Internal Image", "tactic": "Persistence", "nist": "Protect"},

    # Defense Evasion
    "T1562": {"name": "Impair Defenses", "tactic": "Defense Evasion", "nist": "Detect"},
    "T1070": {"name": "Indicator Removal", "tactic": "Defense Evasion", "nist": "Detect"},
    "T1027": {"name": "Obfuscated Files or Information", "tactic": "Defense Evasion", "nist": "Detect"},
    "T1027.003": {"name": "Steganography", "tactic": "Defense Evasion", "nist": "Detect"},
    "T1055": {"name": "Process Injection", "tactic": "Defense Evasion", "nist": "Detect"},
    "T1140": {"name": "Deobfuscate/Decode Files or Information", "tactic": "Defense Evasion", "nist": "Detect"},
    "T1610": {"name": "Deploy Container", "tactic": "Defense Evasion", "nist": "Protect"},
    "T1222": {"name": "File and Directory Permissions Modification", "tactic": "Defense Evasion", "nist": "Protect"},

    # Credential Access
    "T1003": {"name": "OS Credential Dumping", "tactic": "Credential Access", "nist": "Protect"},

    # Discovery
    "T1087": {"name": "Account Discovery", "tactic": "Discovery", "nist": "Identify"},
    "T1046": {"name": "Network Service Discovery", "tactic": "Discovery", "nist": "Identify"},
    "T1082": {"name": "System Information Discovery", "tactic": "Discovery", "nist": "Identify"},
    "T1016": {"name": "System Network Configuration Discovery", "tactic": "Discovery", "nist": "Identify"},
    "T1069": {"name": "Permission Groups Discovery", "tactic": "Discovery", "nist": "Identify"},

    # Collection
    "T1114": {"name": "Email Collection", "tactic": "Collection", "nist": "Identify"},

    # Command and Control
    "T1071": {"name": "Application Layer Protocol", "tactic": "Command and Control", "nist": "Detect"},
    "T1573": {"name": "Encrypted Channel", "tactic": "Command and Control", "nist": "Detect"},

    # Exfiltration
    "T1048": {"name": "Exfiltration Over Alternative Protocol", "tactic": "Exfiltration", "nist": "Detect"},
}

# Mapping Lab Categories to ATT&CK Techniques
# A single lab category can cover multiple techniques.
CATEGORY_TO_TECHNIQUES = {
    # Offensive / Web
    "Web Exploitation": ["T1190", "T1078", "T1203"],
    
    # Malware & Reverse Engineering
    "Malware Analysis": ["T1059", "T1027", "T1055"],
    
    # Forensics
    "Digital Forensics": ["T1070", "T1003", "T1082"],
    "Network Forensics": ["T1071", "T1573", "T1048"],
    
    # Defense / Blue Team
    "Incident Response": ["T1562", "T1543", "T1098"],
    "SOC / Log Analysis": ["T1190", "T1078"],
    
    # Social Engineering
    "Social Engineering": ["T1566", "T1566.001", "T1566.002"],
    
    # Recon / OSINT (Using PRE-ATT&CK Techniques)
    "Reconnaissance / OSINT": ["T1593", "T1594", "T1590"],
    
    # Specialized Topics
    "Steganography": ["T1027", "T1027.003"],
    "Container Analysis": ["T1609", "T1610", "T1525"],
    "Cryptography / Encoding": ["T1140", "T1027"],
    
    # Fundamentals
    "Networking Fundamentals": ["T1046", "T1016"],
    "Systems Fundamentals (Linux/Windows)": ["T1069", "T1222"],
    "Web Infrastructure / Apache": ["T1505", "T1190"],
    "Pentesting Methodology / Adversary Mindset": ["T1046", "T1087"]
}
