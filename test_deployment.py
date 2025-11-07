#!/usr/bin/env python3
"""
Test script to validate the deployment package before pushing to Streamlit Cloud.
Run this locally to catch issues early.
"""

import sys
import os
from pathlib import Path

def test_file_structure():
    """Check that all required files exist."""
    print("🔍 Testing file structure...")
    
    required_files = [
        "app.py",
        "requirements.txt",
        ".streamlit/config.toml",
        "README.md",
        "DEPLOYMENT_GUIDE.md",
        ".gitignore"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
            print(f"  ❌ Missing: {file}")
        else:
            print(f"  ✅ Found: {file}")
    
    if missing_files:
        print(f"\n❌ Missing {len(missing_files)} required file(s)")
        return False
    
    print("✅ All required files present\n")
    return True

def test_requirements():
    """Check requirements.txt format."""
    print("🔍 Testing requirements.txt...")
    
    try:
        with open("requirements.txt", "r") as f:
            lines = f.readlines()
        
        if not lines:
            print("  ❌ requirements.txt is empty")
            return False
        
        required_packages = ["streamlit", "pandas", "plotly", "numpy"]
        found_packages = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#"):
                package = line.split(">=")[0].split("==")[0].lower()
                found_packages.append(package)
                print(f"  ✅ {line}")
        
        missing = [pkg for pkg in required_packages if pkg not in found_packages]
        if missing:
            print(f"  ⚠️  Missing recommended packages: {', '.join(missing)}")
        
        print("✅ requirements.txt is valid\n")
        return True
        
    except Exception as e:
        print(f"  ❌ Error reading requirements.txt: {e}")
        return False

def test_imports():
    """Test that all imports in app.py can be resolved."""
    print("🔍 Testing imports...")
    
    try:
        # Try importing the required packages
        import streamlit
        print(f"  ✅ streamlit {streamlit.__version__}")
        
        import pandas
        print(f"  ✅ pandas {pandas.__version__}")
        
        import plotly
        print(f"  ✅ plotly {plotly.__version__}")
        
        import numpy
        print(f"  ✅ numpy {numpy.__version__}")
        
        print("✅ All imports successful\n")
        return True
        
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        print("  💡 Run: pip install -r requirements.txt")
        return False

def test_app_syntax():
    """Check app.py for syntax errors."""
    print("🔍 Testing app.py syntax...")
    
    try:
        with open("app.py", "r") as f:
            code = f.read()
        
        compile(code, "app.py", "exec")
        print("  ✅ No syntax errors")
        print("✅ app.py syntax is valid\n")
        return True
        
    except SyntaxError as e:
        print(f"  ❌ Syntax error in app.py: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Error reading app.py: {e}")
        return False

def test_config():
    """Check Streamlit config file."""
    print("🔍 Testing .streamlit/config.toml...")
    
    try:
        config_path = Path(".streamlit/config.toml")
        if not config_path.exists():
            print("  ⚠️  Config file not found (optional)")
            return True
        
        with open(config_path, "r") as f:
            content = f.read()
        
        if "[theme]" in content or "[server]" in content:
            print("  ✅ Config file has valid sections")
        
        print("✅ Config file is valid\n")
        return True
        
    except Exception as e:
        print(f"  ❌ Error reading config: {e}")
        return False

def test_no_secrets():
    """Check for common secret patterns."""
    print("🔍 Checking for secrets...")
    
    try:
        with open("app.py", "r") as f:
            content = f.read().lower()
        
        secret_patterns = [
            "api_key",
            "password",
            "secret",
            "token",
            "aws_access",
            "private_key"
        ]
        
        found_secrets = []
        for pattern in secret_patterns:
            if pattern in content and "=" in content:
                # Simple check - might have false positives
                found_secrets.append(pattern)
        
        if found_secrets:
            print(f"  ⚠️  Potential secrets found: {', '.join(found_secrets)}")
            print("  💡 Make sure these are not hardcoded values")
        else:
            print("  ✅ No obvious secrets detected")
        
        print("✅ Security check complete\n")
        return True
        
    except Exception as e:
        print(f"  ❌ Error checking secrets: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("🚀 Streamlit Deployment Package Validator")
    print("=" * 60)
    print()
    
    tests = [
        ("File Structure", test_file_structure),
        ("Requirements", test_requirements),
        ("Imports", test_imports),
        ("App Syntax", test_app_syntax),
        ("Config", test_config),
        ("Security", test_no_secrets)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Test '{name}' failed with error: {e}\n")
            results.append((name, False))
    
    print("=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Ready to deploy to Streamlit Cloud.")
        print("\n📝 Next steps:")
        print("   1. Push to GitHub: git push origin main")
        print("   2. Deploy on Streamlit Cloud: https://share.streamlit.io")
        print("   3. Follow DEPLOYMENT_GUIDE.md for detailed instructions")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix the issues before deploying.")
        print("   Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
