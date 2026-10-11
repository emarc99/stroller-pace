import subprocess
import json
import sys

def stage_article():
    with open("SUBMISSION_ARTICLE.md", "r", encoding="utf-8") as f:
        content = f.read()

    title = "StrollerPulse: The Screen-Free Shock & Terrain Watchdog Powered by Prior Labs TabPFN"
    exe_path = r"C:\Users\LENOVO\.devrelay\bin\dev_mlh_mcp_server.exe"
    
    cmd = [
        exe_path, "articles", "update", "4832777",
        "--title", title,
        "--body", content
    ]
    
    print("Staging article to DEV via devrelay direct exe...")
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    print("Return code:", proc.returncode)
    print("Stdout:", proc.stdout)
    if proc.stderr:
        print("Stderr:", proc.stderr)

if __name__ == "__main__":
    stage_article()
