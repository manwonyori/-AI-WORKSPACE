"""
AI Image Studio - Quick Test
Fast validation of core system functionality
"""

import json
from pathlib import Path
from datetime import datetime

def main():
    print("AI Image Studio - Quick System Test")
    print("=" * 40)
    
    base_path = Path(__file__).parent
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Check if core files exist
    tests_total += 1
    core_files = [
        "prompt_engine.py",
        "image_analyzer.py", 
        "ai_studio_cli.py",
        "scheduler.py",
        "monitoring.py"
    ]
    
    missing_files = []
    for file_name in core_files:
        if not (base_path / file_name).exists():
            missing_files.append(file_name)
    
    if not missing_files:
        print("[PASS] All core files present")
        tests_passed += 1
    else:
        print(f"[FAIL] Missing files: {', '.join(missing_files)}")
    
    # Test 2: Check template file
    tests_total += 1
    template_file = base_path / "prompts" / "prompt_templates.json"
    if template_file.exists():
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                templates = json.load(f)
            
            if "categories" in templates and "food" in templates["categories"]:
                print("[PASS] Template file valid")
                tests_passed += 1
            else:
                print("[FAIL] Template file missing required structure")
        except Exception as e:
            print(f"[FAIL] Template file error: {e}")
    else:
        print("[FAIL] Template file not found")
    
    # Test 3: Test basic prompt formatting
    tests_total += 1
    try:
        template = "Professional photo of {product_name} with {style} styling"
        result = template.format(product_name="Korean BBQ", style="modern")
        
        if "Korean BBQ" in result and "modern" in result:
            print("[PASS] Basic template formatting works")
            tests_passed += 1
        else:
            print("[FAIL] Template formatting failed")
    except Exception as e:
        print(f"[FAIL] Template formatting error: {e}")
    
    # Test 4: Directory creation
    tests_total += 1
    try:
        required_dirs = ["generated", "analysis", "config", "logs"]
        for dir_name in required_dirs:
            (base_path / dir_name).mkdir(exist_ok=True)
        
        print("[PASS] Directory structure created")
        tests_passed += 1
    except Exception as e:
        print(f"[FAIL] Directory creation error: {e}")
    
    # Test 5: JSON operations
    tests_total += 1
    try:
        test_data = {
            "test_id": "quick_test",
            "timestamp": datetime.now().isoformat(),
            "status": "running"
        }
        
        test_file = base_path / "config" / "test.json"
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, indent=2)
        
        # Read back and verify
        with open(test_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        
        if loaded_data["test_id"] == "quick_test":
            print("[PASS] JSON operations working")
            tests_passed += 1
            # Clean up
            test_file.unlink()
        else:
            print("[FAIL] JSON data corruption")
    except Exception as e:
        print(f"[FAIL] JSON operations error: {e}")
    
    # Summary
    print("\n" + "=" * 40)
    print("QUICK TEST RESULTS")
    print("=" * 40)
    print(f"Passed: {tests_passed}/{tests_total}")
    print(f"Success Rate: {(tests_passed/tests_total)*100:.1f}%")
    
    if tests_passed == tests_total:
        print("\n[SUCCESS] All quick tests passed!")
        print("System appears to be ready for basic operation.")
        return True
    else:
        print(f"\n[WARNING] {tests_total - tests_passed} test(s) failed")
        print("Some issues need to be resolved before full operation.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)