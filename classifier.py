"""
AI Campus Issue Triage System - Rule-based AI Classifier
--------------------------------------------------------
This module simulates AI issue classification using keyword analysis,
natural language pattern matching, and rule-based decision trees.
It is lightweight, easy to understand, and fast.
"""

def classify_issue(issue_text, location=""):
    """
    Analyzes an issue description text and automatically returns:
    1. Category (Network, Equipment, Infrastructure, General)
    2. Priority (HIGH, MEDIUM, LOW)
    3. Responsible Department (IT Support, Maintenance, Facilities, Campus Admin)
    4. Suggested Action (Recommended first step for quick resolution)
    """
    text_lower = issue_text.lower()
    
    # ----------------------------------------------------
    # 1. CATEGORY & DEPARTMENT & ACTION CLASSIFICATION
    # ----------------------------------------------------
    
    network_keywords = ["wifi", "wi-fi", "internet", "network", "router", "lan", "connection", "broadband", "ethernet", "online"]
    equipment_keywords = ["projector", "computer", "pc", "monitor", "keyboard", "mouse", "screen", "mic", "microphone", "speaker", "display", "lab equipment"]
    infrastructure_keywords = ["ac", "air conditioner", "fan", "light", "water", "leak", "pipe", "door", "window", "chair", "bench", "toilet", "washroom", "electricity", "power", "plug"]
    
    category = "General"
    department = "Campus Admin"
    suggested_action = "Review report details and route to relevant staff."
    
    # Check for Network issues
    if any(keyword in text_lower for keyword in network_keywords):
        category = "Network"
        department = "IT Support"
        if "router" in text_lower or "block" in text_lower or "everyone" in text_lower:
            suggested_action = f"Check local Wi-Fi router & main network switch in {location if location else 'specified area'}."
        else:
            suggested_action = "Verify IP configuration, signal strength, and DNS server status."
            
    # Check for Equipment issues
    elif any(keyword in text_lower for keyword in equipment_keywords):
        category = "Equipment"
        department = "Maintenance"
        if "projector" in text_lower:
            suggested_action = "Inspect projector power supply, HDMI input cable, and lamp bulb."
        elif "computer" in text_lower or "pc" in text_lower:
            suggested_action = "Check desktop hardware diagnostics, RAM, and monitor cable connections."
        else:
            suggested_action = "Dispatch technician to inspect classroom / lab equipment hardware."
            
    # Check for Infrastructure issues
    elif any(keyword in text_lower for keyword in infrastructure_keywords):
        category = "Infrastructure"
        department = "Facilities"
        if "water" in text_lower or "leak" in text_lower or "pipe" in text_lower:
            suggested_action = "Dispatch plumbing team urgently to stop water leak and inspect piping."
        elif "ac" in text_lower or "air conditioner" in text_lower:
            suggested_action = "Schedule AC maintenance, check compressor coolant and filter clean-up."
        else:
            suggested_action = "Send facilities maintenance team for physical repair & inspection."

    # ----------------------------------------------------
    # 2. PRIORITY DETERMINATION
    # ----------------------------------------------------
    
    high_urgency_keywords = [
        "everyone", "all", "stopped working", "emergency", "urgent", 
        "fire", "leakage", "smoke", "exam", "entire", "blocked", "outage", "since morning"
    ]
    medium_urgency_keywords = [
        "not working", "flickering", "slow", "broken", "noisy", "damaged", "issue", "problem", "faulty"
    ]
    
    if any(keyword in text_lower for keyword in high_urgency_keywords):
        priority = "HIGH"
    elif any(keyword in text_lower for keyword in medium_urgency_keywords):
        priority = "MEDIUM"
    else:
        priority = "LOW"
        
    return {
        "category": category,
        "priority": priority,
        "department": department,
        "suggested_action": suggested_action
    }
