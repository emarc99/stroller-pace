import subprocess
import json
import sys

def stage_and_publish_article():
    with open("SUBMISSION_ARTICLE.md", "r", encoding="utf-8") as f:
        content = f.read()

    title = "StrollerPulse: The Screen-Free Shock & Terrain Watchdog Powered by Prior Labs TabPFN"
    exe_path = r"C:\Users\LENOVO\.devrelay\bin\dev_mlh_mcp_server.exe"
    
    cmd = [
        exe_path, "articles", "update", "4832777",
        "--title", title,
        "--body", content
    ]
    
    print("Publishing article to DEV via devrelay direct exe...")
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    print("Return code:", proc.returncode)
    if proc.returncode == 0:
        try:
            data = json.loads(proc.stdout)
            print("Successfully updated article ID:", data.get("id"))
            print("Title:", data.get("title"))
            print("Published status:", data.get("published"))
            print("Permanent URL:", data.get("url"))
            print("Edit URL:", data.get("edit_url"))
        except Exception as e:
            print("Output received (length):", len(proc.stdout))
    else:
        print("Error output:", proc.stderr)

if __name__ == "__main__":
    stage_and_publish_article()
