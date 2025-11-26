#!/usr/bin/env python3
"""
OpenRouter API Verification Script
===================================

Verifies that the OpenRouter API key is configured correctly and
can access the Gemini 2.0 Flash FREE model.

Usage:
    python scripts/verify_openrouter.py
"""

import os
import sys
import json
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

# Load .env file if exists
env_file = PROJECT_ROOT / ".env"
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip()


def check_env_variables():
    """Check that required environment variables are set."""
    print("=" * 60)
    print("1. CHECKING ENVIRONMENT VARIABLES")
    print("=" * 60)

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        print("[FAIL] OPENROUTER_API_KEY not set")
        print("\nTo fix this:")
        print("  1. Get an API key from https://openrouter.ai")
        print("  2. Set the environment variable:")
        print("     Windows: set OPENROUTER_API_KEY=sk-or-v1-your-key")
        print("     Linux/Mac: export OPENROUTER_API_KEY=sk-or-v1-your-key")
        print("  3. Or add it to your .env file")
        return None

    # Mask the key for display
    masked_key = api_key[:12] + "..." + api_key[-4:] if len(api_key) > 20 else "***"
    print(f"[OK] OPENROUTER_API_KEY found: {masked_key}")

    return api_key


def check_api_connectivity(api_key: str):
    """Check that we can connect to OpenRouter API."""
    print("\n" + "=" * 60)
    print("2. CHECKING API CONNECTIVITY")
    print("=" * 60)

    try:
        import httpx
    except ImportError:
        print("[WARN] httpx not installed, installing...")
        os.system(f"{sys.executable} -m pip install httpx")
        import httpx

    try:
        client = httpx.Client(
            base_url="https://openrouter.ai/api/v1",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            timeout=30.0
        )

        # Check models endpoint
        response = client.get("/models")
        response.raise_for_status()

        models_data = response.json()
        print(f"[OK] Connected to OpenRouter API")
        print(f"[OK] Found {len(models_data.get('data', []))} available models")

        return client

    except Exception as e:
        print(f"[FAIL] Could not connect to OpenRouter: {e}")
        return None


def check_gemini_model(client):
    """Check that Gemini 2.0 Flash FREE model is available."""
    print("\n" + "=" * 60)
    print("3. CHECKING GEMINI 2.0 FLASH FREE MODEL")
    print("=" * 60)

    target_model = "google/gemini-2.0-flash-exp:free"

    try:
        response = client.get("/models")
        response.raise_for_status()

        models = response.json().get("data", [])

        # Find Gemini models
        gemini_models = [m for m in models if "gemini" in m.get("id", "").lower()]

        print(f"[INFO] Found {len(gemini_models)} Gemini models:")
        for model in gemini_models[:10]:
            model_id = model.get("id", "")
            pricing = model.get("pricing", {})
            prompt_price = pricing.get("prompt", "N/A")
            completion_price = pricing.get("completion", "N/A")
            print(f"  - {model_id}")
            print(f"    Input: ${float(prompt_price)*1000000:.2f}/1M tokens, Output: ${float(completion_price)*1000000:.2f}/1M tokens" if prompt_price != "N/A" else "    Pricing: N/A")

        # Check if our target model exists
        target_found = any(m.get("id") == target_model for m in models)

        if target_found:
            print(f"\n[OK] Target model '{target_model}' is available")
            return True
        else:
            print(f"\n[WARN] Target model '{target_model}' not found in model list")
            print("[INFO] This may still work - OpenRouter dynamically routes models")
            return True  # Try anyway

    except Exception as e:
        print(f"[FAIL] Could not check models: {e}")
        return False


def test_model_inference(client):
    """Test actual model inference with Gemini 2.0 Flash (FREE)."""
    print("\n" + "=" * 60)
    print("4. TESTING MODEL INFERENCE")
    print("=" * 60)

    model = "google/gemini-2.0-flash-exp:free"

    test_prompt = """You are a legal document analyzer.

Extract the key facts from this text:
"John Smith and Jane Smith were married on 15 March 2010 in Sydney.
They separated on 1 June 2020. They have two children aged 8 and 10."

Return a JSON object with: parties, marriage_date, separation_date, children_count.
"""

    print(f"[INFO] Sending test request to {model}...")

    try:
        response = client.post(
            "/chat/completions",
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant that outputs JSON."},
                    {"role": "user", "content": test_prompt}
                ],
                "temperature": 0.1,
                "max_tokens": 500
            }
        )
        response.raise_for_status()

        result = response.json()
        content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        usage = result.get("usage", {})

        print(f"[OK] Model responded successfully!")
        print(f"\n[RESPONSE]:")
        print("-" * 40)
        print(content[:500])
        print("-" * 40)

        print(f"\n[USAGE]:")
        print(f"  - Prompt tokens: {usage.get('prompt_tokens', 'N/A')}")
        print(f"  - Completion tokens: {usage.get('completion_tokens', 'N/A')}")
        print(f"  - Total tokens: {usage.get('total_tokens', 'N/A')}")

        return True

    except Exception as e:
        print(f"[FAIL] Model inference failed: {e}")
        if hasattr(e, 'response'):
            print(f"[DEBUG] Response: {e.response.text if hasattr(e.response, 'text') else e.response}")
        return False


def test_gsw_components():
    """Test that GSW components can initialize with the API key."""
    print("\n" + "=" * 60)
    print("5. TESTING GSW COMPONENTS")
    print("=" * 60)

    components_ok = True

    # Test LegalOperator
    try:
        from src.gsw.legal_operator import LegalOperator
        operator = LegalOperator()
        print(f"[OK] LegalOperator initialized (model: {operator.model})")
    except Exception as e:
        print(f"[FAIL] LegalOperator: {e}")
        components_ok = False

    # Test LegalReconciler
    try:
        from src.gsw.legal_reconciler import LegalReconciler
        reconciler = LegalReconciler()
        print(f"[OK] LegalReconciler initialized (model: {reconciler.model})")
    except Exception as e:
        print(f"[FAIL] LegalReconciler: {e}")
        components_ok = False

    # Test LegalSpacetime
    try:
        from src.gsw.legal_spacetime import LegalSpacetime
        spacetime = LegalSpacetime()
        print(f"[OK] LegalSpacetime initialized (model: {spacetime.model})")
    except Exception as e:
        print(f"[FAIL] LegalSpacetime: {e}")
        components_ok = False

    # Test LegalSummary
    try:
        from src.gsw.legal_summary import LegalSummary
        summary = LegalSummary()
        print(f"[OK] LegalSummary initialized (model: {summary.model})")
    except Exception as e:
        print(f"[FAIL] LegalSummary: {e}")
        components_ok = False

    return components_ok


def print_summary(all_ok: bool):
    """Print final summary."""
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)

    if all_ok:
        print("""
[SUCCESS] All checks passed!

Your OpenRouter API is configured correctly for production use.

Model Configuration:
  - Primary: google/gemini-2.0-flash-exp:free
  - Context Window: 1,048,576 tokens (1M)
  - Pricing: FREE! $0.00

Ready to process the 9.4GB Australian Legal Corpus at ZERO COST!

Next steps:
  1. Run domain extraction:
     python gsw_pipeline.py extract --input ../corpus.jsonl

  2. Process a domain:
     python gsw_pipeline.py process --domain family --limit 10

  3. Run full pipeline:
     python gsw_pipeline.py full --domain family --limit 100
""")
    else:
        print("""
[FAILURE] Some checks failed.

Please review the errors above and fix the configuration issues.

Common fixes:
  1. Set OPENROUTER_API_KEY environment variable
  2. Check your API key balance at https://openrouter.ai
  3. Ensure you have internet connectivity
  4. Install required dependencies: pip install httpx openai
""")


def main():
    print("""
    ============================================================
    OpenRouter API Verification for Legal GSW System
    ============================================================
    Model: google/gemini-2.0-flash-exp:free (FREE!)
    Purpose: Production readiness check for 9.4GB corpus
    ============================================================
    """)

    all_ok = True

    # Step 1: Check environment
    api_key = check_env_variables()
    if not api_key:
        print_summary(False)
        return 1

    # Step 2: Check API connectivity
    client = check_api_connectivity(api_key)
    if not client:
        print_summary(False)
        return 1

    # Step 3: Check Gemini model
    model_ok = check_gemini_model(client)
    if not model_ok:
        all_ok = False

    # Step 4: Test inference
    inference_ok = test_model_inference(client)
    if not inference_ok:
        all_ok = False

    # Step 5: Test GSW components
    components_ok = test_gsw_components()
    if not components_ok:
        all_ok = False

    # Summary
    print_summary(all_ok)

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
