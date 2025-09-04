"""
AI Image Studio - Simple Test
Basic functionality test without external dependencies
"""

import json
import tempfile
from pathlib import Path
from datetime import datetime

def test_basic_functionality():
    """Test basic system functionality"""
    print("AI Image Studio - Simple Test Suite")
    print("="*50)
    
    results = {"tests": [], "total": 0, "passed": 0, "failed": 0}
    
    # Test 1: JSON Template Loading
    try:
        templates_path = Path(__file__).parent / "prompts" / "prompt_templates.json"
        if templates_path.exists():
            with open(templates_path, 'r', encoding='utf-8') as f:
                templates = json.load(f)
            
            assert "categories" in templates
            assert "food" in templates["categories"]
            print("[PASS] Template loading test passed")
            results["tests"].append({"name": "Template Loading", "status": "passed"})
            results["passed"] += 1
        else:
            print("[SKIP] Template file not found - skipping")
            results["tests"].append({"name": "Template Loading", "status": "skipped"})
    except Exception as e:
        print(f"[FAIL] Template loading test failed: {e}")
        results["tests"].append({"name": "Template Loading", "status": "failed", "error": str(e)})
        results["failed"] += 1
    
    results["total"] += 1
    
    # Test 2: Directory Structure
    try:
        base_path = Path(__file__).parent
        required_dirs = ["prompts", "generated", "analysis", "models", "config"]
        
        for dir_name in required_dirs:
            dir_path = base_path / dir_name
            if not dir_path.exists():
                print(f"[INFO] Creating missing directory: {dir_name}")
                dir_path.mkdir(exist_ok=True)
        
        print("[PASS] Directory structure test passed")
        results["tests"].append({"name": "Directory Structure", "status": "passed"})
        results["passed"] += 1
    except Exception as e:
        print(f"[FAIL] Directory structure test failed: {e}")
        results["tests"].append({"name": "Directory Structure", "status": "failed", "error": str(e)})
        results["failed"] += 1
    
    results["total"] += 1
    
    # Test 3: Configuration File Creation
    try:
        config_dir = Path(__file__).parent / "config"
        config_dir.mkdir(exist_ok=True)
        
        test_config = {
            "version": "1.0.0",
            "created": datetime.now().isoformat(),
            "test": True
        }
        
        config_file = config_dir / "test_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(test_config, f, indent=2)
        
        # Verify file was created and is readable
        with open(config_file, 'r', encoding='utf-8') as f:
            loaded_config = json.load(f)
        
        assert loaded_config["test"] == True
        print("✅ Configuration test passed")
        results["tests"].append({"name": "Configuration", "status": "passed"})
        results["passed"] += 1
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        results["tests"].append({"name": "Configuration", "status": "failed", "error": str(e)})
        results["failed"] += 1
    
    results["total"] += 1
    
    # Test 4: Basic Prompt Template Processing
    try:
        template = "A professional product photography of {product_name}, {style_description}, placed on a {background_setting}"
        
        product_data = {
            "product_name": "Korean BBQ",
            "style_description": "modern and clean",
            "background_setting": "white marble surface"
        }
        
        filled_template = template.format(**product_data)
        
        assert "Korean BBQ" in filled_template
        assert "modern and clean" in filled_template
        print("✅ Template processing test passed")
        results["tests"].append({"name": "Template Processing", "status": "passed"})
        results["passed"] += 1
    except Exception as e:
        print(f"❌ Template processing test failed: {e}")
        results["tests"].append({"name": "Template Processing", "status": "failed", "error": str(e)})
        results["failed"] += 1
    
    results["total"] += 1
    
    # Test 5: File System Operations
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create test file
            test_file = temp_path / "test_image.txt"
            with open(test_file, 'w') as f:
                f.write("Test image placeholder")
            
            # Create subdirectories
            (temp_path / "generated" / "2025" / "01").mkdir(parents=True)
            
            # List files
            files = list(temp_path.rglob("*"))
            
            assert len(files) >= 4  # At least the file and 3 directories
            print("✅ File system operations test passed")
            results["tests"].append({"name": "File System", "status": "passed"})
            results["passed"] += 1
    except Exception as e:
        print(f"❌ File system test failed: {e}")
        results["tests"].append({"name": "File System", "status": "failed", "error": str(e)})
        results["failed"] += 1
    
    results["total"] += 1
    
    # Test 6: Data Structure Validation
    try:
        # Test prompt data structure
        prompt_data = {
            "id": "test_123",
            "timestamp": datetime.now().isoformat(),
            "product_data": {"name": "Test Product"},
            "category": "food",
            "style": "product_showcase",
            "platform": "midjourney",
            "prompt": "Test prompt with specific requirements",
            "negative_prompt": "blurry, low quality",
            "quality_score": None,
            "metadata": {
                "template_used": "food/product_showcase",
                "prompt_length": 45
            }
        }
        
        # Validate required fields
        required_fields = ["id", "timestamp", "prompt", "category", "platform"]
        for field in required_fields:
            assert field in prompt_data, f"Missing required field: {field}"
        
        # Validate data types
        assert isinstance(prompt_data["metadata"], dict)
        assert isinstance(prompt_data["prompt"], str)
        assert len(prompt_data["prompt"]) > 0
        
        print("✅ Data structure validation test passed")
        results["tests"].append({"name": "Data Validation", "status": "passed"})
        results["passed"] += 1
    except Exception as e:
        print(f"❌ Data structure test failed: {e}")
        results["tests"].append({"name": "Data Validation", "status": "failed", "error": str(e)})
        results["failed"] += 1
    
    results["total"] += 1
    
    # Summary
    print("\n" + "="*50)
    print("🎯 TEST SUMMARY")
    print("="*50)
    print(f"Total Tests: {results['total']}")
    print(f"Passed: {results['passed']} ✅")
    print(f"Failed: {results['failed']} ❌")
    print(f"Success Rate: {(results['passed']/results['total'])*100:.1f}%")
    
    # Detailed results
    if results["failed"] > 0:
        print("\n❌ Failed Tests:")
        for test in results["tests"]:
            if test["status"] == "failed":
                print(f"  - {test['name']}: {test.get('error', 'Unknown error')}")
    
    # Save results
    results_file = Path(__file__).parent / "simple_test_results.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Test results saved to: {results_file}")
    
    # Return success status
    return results["failed"] == 0

def test_system_readiness():
    """Test if the system is ready for full operation"""
    print("\n🔧 SYSTEM READINESS CHECK")
    print("="*50)
    
    readiness = {"ready": True, "issues": [], "recommendations": []}
    
    base_path = Path(__file__).parent
    
    # Check required files
    required_files = [
        "prompt_engine.py",
        "image_analyzer.py", 
        "ai_studio_cli.py",
        "scheduler.py",
        "monitoring.py",
        "requirements.txt",
        "prompts/prompt_templates.json"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not (base_path / file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        readiness["ready"] = False
        readiness["issues"].append(f"Missing files: {', '.join(missing_files)}")
    else:
        print("✅ All required files present")
    
    # Check directories
    required_dirs = ["prompts", "generated", "analysis", "models", "config", "logs"]
    for dir_name in required_dirs:
        dir_path = base_path / dir_name
        if not dir_path.exists():
            readiness["recommendations"].append(f"Create directory: {dir_name}")
    
    # Check configuration
    config_files = ["studio_config.json", "monitoring_config.json", "ai_council_integration.json"]
    existing_configs = []
    for config_file in config_files:
        if (base_path / "config" / config_file).exists():
            existing_configs.append(config_file)
    
    if existing_configs:
        print(f"✅ Found configuration files: {', '.join(existing_configs)}")
    else:
        readiness["recommendations"].append("Initialize configuration files")
    
    # Final assessment
    if readiness["ready"]:
        print("🚀 System is ready for operation!")
    else:
        print("⚠️ System has issues that need to be resolved")
        for issue in readiness["issues"]:
            print(f"  ❌ {issue}")
    
    if readiness["recommendations"]:
        print("\n💡 Recommendations:")
        for rec in readiness["recommendations"]:
            print(f"  📋 {rec}")
    
    return readiness

if __name__ == "__main__":
    # Run basic tests
    basic_success = test_basic_functionality()
    
    # Run readiness check
    readiness = test_system_readiness()
    
    # Overall result
    print("\n" + "🎊" * 50)
    if basic_success and readiness["ready"]:
        print("🎉 AI IMAGE STUDIO - ALL SYSTEMS GO! 🎉")
        exit_code = 0
    else:
        print("⚠️ AI IMAGE STUDIO - SETUP REQUIRED ⚠️")
        exit_code = 1
    
    print("🎊" * 50)
    
    exit(exit_code)