import os
import sys

def check_file(path, required=True):
    exists = os.path.exists(path)
    status = "[OK]" if exists else ("[FAIL]" if required else "[MISSING]")
    print(f"  {status} {path}")
    return exists

def check_content(path, keyword, description):
    if not os.path.exists(path):
        print(f"  [FAIL] {description} (File missing)")
        return False
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            if keyword in content:
                print(f"  [OK] {description}")
                return True
            else:
                print(f"  [FAIL] {description} (Keyword '{keyword}' not found)")
                return False
    except Exception as e:
        print(f"  [ERROR] {description} ({str(e)})")
        return False

def run_checks():
    print("=======================================================")
    print("  ULTIMATE AGENT - Production Readiness Check")
    print("=======================================================")

    score = 0
    total = 12

    print("\n[FILES] Required Files")
    if check_file("Dockerfile"): score += 1
    if check_file("docker-compose.yml"): score += 1
    if check_file("railway.toml"): score += 1
    if check_file("requirements.txt"): score += 1

    print("\n[API] API Logic (app/main.py)")
    if check_content("app/main.py", "/health", "Health check (/health)"): score += 1
    if check_content("app/main.py", "/ready", "Readiness probe (/ready)"): score += 1
    if check_content("app/main.py", "logger", "JSON Logging"): score += 1
    if check_content("app/main.py", "lifespan", "Lifespan (Graceful Shutdown)"): score += 1
    if check_content("app/main.py", "verify_api_key", "Security Middleware"): score += 1

    print("\n[DOCKER] Docker Optimization")
    if check_content("Dockerfile", "builder", "Multi-stage build"): score += 1
    if check_content("Dockerfile", "useradd", "Non-root user"): score += 1
    if check_content("Dockerfile", "HEALTHCHECK", "Healthcheck instruction"): score += 1

    print("\n=======================================================")
    percentage = int((score / total) * 100)
    print(f"  Result: {score}/{total} checks passed ({percentage}%)")
    print("=======================================================")

if __name__ == "__main__":
    run_checks()
