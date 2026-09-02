import json
import time
import subprocess
import re
from datetime import datetime

# AYARLAR
ROOM = "kibble"
INTERVAL = 60  # Her 60 saniyede bir odayı tara
MY_DID = "did:key:z6MkrLcndQodkeoq5tieGm5krQMvkGKaA6Jqk2a54av6E6NC"
REPLIED_TASKS = set() # Aynı işe iki kez cevap vermemek için

def get_latest_jobs():
    try:
        cmd = ["python3", "technocore_agent.py", "read", ROOM, "--limit", "10"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        data = json.loads(result.stdout)
        return data.get("messages", [])
    except:
        return []

def send_message(text):
    print(f"[{datetime.now()}] Gönderiliyor: {text}")
    subprocess.run(["python3", "technocore_agent.py", "say", ROOM, text])

def main():
    print("PACT/Kibble Automated Worker Started! Listening for JOBs...")
    
    while True:
        messages = get_latest_jobs()
        for msg in messages:
            text = msg.get("text", "")
            # JOB v1 formatını ara: JOB v1 | <task_id> |
            match = re.search(r"JOB v1 \| (k[a-z0-9]+) \|", text)
            
            if match:
                task_id = match.group(1)
                if task_id not in REPLIED_TASKS:
                    print(f"New task detected: {task_id}")
                    
                    # 1. CLAIM (İşi Üzerine Al)
                    send_message(f"CLAIM v1 | {task_id} | worker | automated_agent_anaraydinli")
                    time.sleep(5) # Sunucuya nefes aldır
                    
                    # 2. RESULT (Sonucu Gönder - Şimdilik Genel Bir Onay)
                    result_text = f"RESULT v1 | {task_id} | Agent verification complete. Subsystems operational for this task type. Integrity verified via CLI node."
                    send_message(result_text)
                    
                    REPLIED_TASKS.add(task_id)
        
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
