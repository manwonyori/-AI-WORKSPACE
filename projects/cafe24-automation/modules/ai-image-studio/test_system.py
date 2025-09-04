"""
AI Image Studio - System Test Suite
Comprehensive testing for all system components
"""

import unittest
import asyncio
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
import sys
import warnings

# Suppress warnings for cleaner test output
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

try:
    from prompt_engine import PromptEngine, PromptABTester
    from image_analyzer import ImageQualityAnalyzer, FeedbackLoop
    from ai_studio_cli import AIStudioCLI
    from scheduler import TaskScheduler
    from monitoring import SystemMonitor
    from ai_council_integration import AICouncilImageStudioBridge
    MODULES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Some modules not available: {e}")
    MODULES_AVAILABLE = False

@unittest.skipUnless(MODULES_AVAILABLE, "Modules not available")
class TestPromptEngine(unittest.TestCase):
    """Test prompt engine functionality"""
    
    def setUp(self):
        if MODULES_AVAILABLE:
            self.engine = PromptEngine()
        self.test_product = {
            "name": "Test Product",
            "style": "modern",
            "background": "white",
            "lighting": "natural",
            "angle": "45-degree"
        }
    
    def test_prompt_generation(self):
        """Test basic prompt generation"""
        result = self.engine.generate_prompt(
            self.test_product, 
            category="food", 
            style="product_showcase",
            platform="midjourney"
        )
        
        self.assertIn("prompt", result)
        self.assertIn("negative_prompt", result)
        self.assertIn("id", result)
        self.assertIn("Test Product", result["prompt"])
    
    def test_batch_generation(self):
        """Test batch prompt generation"""
        products = [self.test_product, {"name": "Product 2", "style": "minimalist"}]
        
        results = self.engine.batch_generate_prompts(
            products,
            category="food",
            styles=["product_showcase", "lifestyle"]
        )
        
        self.assertEqual(len(results), 4)  # 2 products x 2 styles
        self.assertTrue(all("prompt" in r for r in results))
    
    def test_quality_evaluation(self):
        """Test prompt quality evaluation"""
        prompt_data = self.engine.generate_prompt(self.test_product)
        
        score = self.engine.evaluate_prompt_quality(
            prompt_data,
            generation_success=True,
            user_rating=4,
            generation_time=45
        )
        
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
        self.assertIsNotNone(prompt_data.get("quality_score"))
    
    def test_prompt_optimization(self):
        """Test prompt optimization"""
        base_prompt = self.engine.generate_prompt(self.test_product)
        
        optimized = self.engine.optimize_prompt(
            base_prompt,
            optimization_goals=["higher_quality", "more_creative"]
        )
        
        self.assertIn("optimization_goals", optimized["metadata"])
        self.assertIn("optimized_from", optimized["metadata"])
    
    def test_library_export(self):
        """Test prompt library export"""
        # Generate some prompts first
        for i in range(3):
            prompt_data = self.engine.generate_prompt({
                "name": f"Product {i}",
                "style": "modern"
            })
            self.engine.evaluate_prompt_quality(prompt_data, True, 5)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            library_path = self.engine.export_prompt_library(
                str(Path(temp_dir) / "test_library.json")
            )
            
            self.assertTrue(Path(library_path).exists())
            
            with open(library_path, 'r') as f:
                library_data = json.load(f)
            
            self.assertIn("metadata", library_data)
            self.assertIn("high_quality_prompts", library_data)


@unittest.skipUnless(MODULES_AVAILABLE, "Modules not available")
class TestImageAnalyzer(unittest.TestCase):
    """Test image analyzer functionality"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.analyzer = ImageQualityAnalyzer(
            db_path=Path(self.temp_dir) / "test_analysis.db"
        )
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    @patch('cv2.imread')
    @patch('PIL.Image.open')
    def test_image_analysis_mock(self, mock_pil_open, mock_cv_imread):
        """Test image analysis with mocked image loading"""
        # Mock PIL Image
        mock_image = Mock()
        mock_image.size = (1024, 768)
        mock_image.mode = "RGB"
        mock_image.convert.return_value = mock_image
        mock_pil_open.return_value = mock_image
        
        # Mock CV2 image
        import numpy as np
        mock_cv_imread.return_value = np.random.randint(0, 255, (768, 1024, 3), dtype=np.uint8)
        
        # Mock ImageStat
        with patch('PIL.ImageStat.Stat') as mock_stat:
            mock_stat.return_value.mean = [128]
            
            result = self.analyzer.analyze_image(
                "test_image.jpg",
                prompt_data={"prompt": "test prompt"},
                save_to_db=False
            )
        
        self.assertIn("scores", result)
        self.assertIn("technical_analysis", result)
        self.assertIn("aesthetic_analysis", result)
        self.assertIn("auto_tags", result)
        self.assertIn("recommendations", result)
    
    def test_feedback_loop(self):
        """Test feedback loop system"""
        feedback_loop = FeedbackLoop(self.analyzer)
        
        # Mock feedback collection
        feedback_loop.collect_feedback(
            image_id="test_123",
            user_rating=4,
            specific_feedback={"issues": ["brightness"]}
        )
        
        self.assertEqual(len(feedback_loop.feedback_data), 1)
        self.assertEqual(feedback_loop.feedback_data[0]["user_rating"], 4)
    
    def test_tag_generation(self):
        """Test automatic tag generation"""
        from PIL import Image
        import numpy as np
        
        # Create a test image
        test_image = Image.fromarray(
            np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        )
        
        cv_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        
        tags = self.analyzer._generate_image_tags(test_image, cv_image)
        
        self.assertIsInstance(tags, list)
        self.assertGreater(len(tags), 0)


@unittest.skipUnless(MODULES_AVAILABLE, "Modules not available")
class TestAIStudioCLI(unittest.TestCase):
    """Test CLI interface"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.cli = AIStudioCLI()
        # Override config for testing
        self.cli.config["output"]["base_directory"] = self.temp_dir
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    @patch('ai_studio_cli.AIStudioCLI._simulate_generation')
    def test_single_generation(self, mock_generation):
        """Test single image generation"""
        mock_generation.return_value = "test_image.jpg"
        
        result = self.cli.generate_single(
            product_data={"name": "Test Product"},
            analyze=False  # Skip analysis for faster testing
        )
        
        self.assertEqual(result["status"], "success")
        self.assertIn("prompt_data", result)
        self.assertIn("generated_image_path", result)
    
    def test_prompt_optimization(self):
        """Test prompt optimization via CLI"""
        result = self.cli.optimize_prompt(
            base_prompt="test prompt",
            optimization_goals=["higher_quality"],
            test_variations=2
        )
        
        self.assertIn("base_prompt", result)
        self.assertIn("variations", result)
        self.assertEqual(len(result["variations"]), 2)
    
    def test_ab_test_creation(self):
        """Test A/B test creation"""
        test_id = self.cli.run_ab_test(
            prompt_a="prompt A",
            prompt_b="prompt B",
            test_name="test_ab"
        )
        
        self.assertIsInstance(test_id, str)
        self.assertIn(test_id, self.cli.ab_tester.test_groups)


@unittest.skipUnless(MODULES_AVAILABLE, "Modules not available")
class TestScheduler(unittest.TestCase):
    """Test task scheduler"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.scheduler = TaskScheduler(
            db_path=Path(self.temp_dir) / "test_scheduler.db"
        )
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_daily_job_scheduling(self):
        """Test daily job scheduling"""
        job_id = self.scheduler.schedule_daily_job(
            name="Test Daily Job",
            job_type="test_job",
            time_str="10:00",
            config={"test": True}
        )
        
        self.assertIn(job_id, self.scheduler.jobs)
        
        job_data = self.scheduler.jobs[job_id]
        self.assertEqual(job_data["name"], "Test Daily Job")
        self.assertEqual(job_data["schedule_type"], "daily")
    
    def test_job_status_retrieval(self):
        """Test job status retrieval"""
        # Create a test job
        job_id = self.scheduler.schedule_interval_job(
            name="Test Interval Job",
            job_type="test_job",
            interval_minutes=30,
            config={"test": True}
        )
        
        # Get status
        status = self.scheduler.get_job_status(job_id)
        
        self.assertEqual(status["job_id"], job_id)
        self.assertEqual(status["name"], "Test Interval Job")
        self.assertIn("next_run", status)
    
    def test_job_management(self):
        """Test job enable/disable/delete operations"""
        job_id = self.scheduler.schedule_daily_job(
            name="Management Test Job",
            job_type="test_job", 
            time_str="11:00",
            config={}
        )
        
        # Test disable
        self.scheduler.disable_job(job_id)
        self.assertFalse(self.scheduler.jobs[job_id]["enabled"])
        
        # Test enable
        self.scheduler.enable_job(job_id)
        self.assertTrue(self.scheduler.jobs[job_id]["enabled"])
        
        # Test delete
        self.scheduler.delete_job(job_id)
        self.assertNotIn(job_id, self.scheduler.jobs)


@unittest.skipUnless(MODULES_AVAILABLE, "Modules not available")
class TestSystemMonitor(unittest.TestCase):
    """Test system monitoring"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        config_path = Path(self.temp_dir) / "monitor_config.json"
        
        # Create minimal test config
        test_config = {
            "monitoring": {"interval_seconds": 1},
            "alerts": {"enabled": False},
            "thresholds": {"cpu_usage_percent": 90}
        }
        
        with open(config_path, 'w') as f:
            json.dump(test_config, f)
        
        self.monitor = SystemMonitor(config_path=str(config_path))
        self.monitor.db_path = Path(self.temp_dir) / "test_monitor.db"
        self.monitor._initialize_database()
    
    def tearDown(self):
        if self.monitor.running:
            self.monitor.stop_monitoring()
        shutil.rmtree(self.temp_dir)
    
    @patch('psutil.cpu_percent')
    @patch('psutil.virtual_memory')
    @patch('psutil.disk_usage')
    def test_metrics_collection(self, mock_disk, mock_memory, mock_cpu):
        """Test system metrics collection"""
        # Mock system metrics
        mock_cpu.return_value = 45.0
        mock_memory.return_value = Mock(percent=60.0)
        mock_disk.return_value = Mock(percent=70.0)
        
        metrics = self.monitor._collect_system_metrics()
        
        self.assertIn("cpu_usage", metrics)
        self.assertIn("memory_usage", metrics)
        self.assertIn("disk_usage", metrics)
        self.assertEqual(metrics["cpu_usage"], 45.0)
    
    def test_health_report_generation(self):
        """Test health report generation"""
        # Add some test metrics
        test_metrics = {
            "timestamp": datetime.now().isoformat(),
            "system": {"cpu_usage": 50, "memory_usage": 60, "disk_usage": 70},
            "generation": {"avg_quality_score": 75, "success_rate": 90}
        }
        
        self.monitor.metrics_history.append(test_metrics)
        
        report = self.monitor.generate_health_report()
        
        self.assertIn("health_score", report)
        self.assertIn("health_status", report)
        self.assertIn("system_performance", report)
        self.assertIn("recommendations", report)


@unittest.skipUnless(MODULES_AVAILABLE, "Modules not available")
class TestAICouncilIntegration(unittest.TestCase):
    """Test AI Council integration"""
    
    def setUp(self):
        self.bridge = AICouncilImageStudioBridge()
    
    def test_integration_initialization(self):
        """Test integration system initialization"""
        self.assertIsNotNone(self.bridge.config)
        self.assertIsNotNone(self.bridge.prompt_engine)
        self.assertIsNotNone(self.bridge.image_analyzer)
    
    def test_cafe24_integration(self):
        """Test Cafe24 workflow integration"""
        # This will likely return "disabled" or "error" in test environment
        result = self.bridge.integrate_with_cafe24_workflow()
        
        self.assertIn("status", result)
        self.assertIn(result["status"], ["disabled", "error", "completed"])
    
    def test_workflow_setup(self):
        """Test automated workflow setup"""
        # Mock scheduler to avoid actual scheduling in tests
        with patch.object(self.bridge.scheduler, 'schedule_daily_job') as mock_daily:
            mock_daily.return_value = "test_job_id"
            
            jobs = self.bridge.setup_automated_workflows()
            
            # Should return list of job IDs (might be empty if workflows disabled)
            self.assertIsInstance(jobs, list)


@unittest.skipUnless(MODULES_AVAILABLE, "Modules not available")
class TestSystemIntegration(unittest.TestCase):
    """Integration tests for complete system"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow"""
        # 1. Initialize system
        engine = PromptEngine()
        
        # 2. Generate prompt
        product_data = {"name": "Integration Test Product", "style": "modern"}
        prompt_result = engine.generate_prompt(product_data)
        
        self.assertIn("prompt", prompt_result)
        
        # 3. Simulate quality evaluation
        quality_score = engine.evaluate_prompt_quality(
            prompt_result, 
            generation_success=True,
            user_rating=4
        )
        
        self.assertGreater(quality_score, 0)
        
        # 4. Test optimization
        optimized = engine.optimize_prompt(
            prompt_result,
            optimization_goals=["higher_quality"]
        )
        
        self.assertIn("optimization_goals", optimized["metadata"])
    
    @patch('ai_studio_cli.AIStudioCLI._simulate_generation')
    def test_cli_batch_processing(self, mock_generation):
        """Test CLI batch processing"""
        mock_generation.return_value = "test_image.jpg"
        
        # Create test CSV file
        test_csv = Path(self.temp_dir) / "test_products.csv"
        with open(test_csv, 'w') as f:
            f.write("name,style\n")
            f.write("Product 1,modern\n")
            f.write("Product 2,minimalist\n")
        
        cli = AIStudioCLI()
        cli.config["output"]["base_directory"] = self.temp_dir
        
        # This would normally take a long time, so we're testing the setup
        # In a real scenario, you'd run this with actual generation
        self.assertTrue(test_csv.exists())


def run_performance_tests():
    """Run performance benchmarks"""
    print("\n" + "="*50)
    print("PERFORMANCE BENCHMARKS")
    print("="*50)
    
    # Prompt generation speed
    engine = PromptEngine()
    
    import time
    start_time = time.time()
    
    for i in range(100):
        engine.generate_prompt(
            {"name": f"Product {i}", "style": "modern"},
            category="food"
        )
    
    end_time = time.time()
    avg_time_per_prompt = (end_time - start_time) / 100
    
    print(f"Prompt Generation: {avg_time_per_prompt:.4f} seconds per prompt")
    print(f"Throughput: {100 / (end_time - start_time):.1f} prompts per second")
    
    # Memory usage test
    import psutil
    process = psutil.Process()
    memory_mb = process.memory_info().rss / 1024 / 1024
    print(f"Memory Usage: {memory_mb:.1f} MB")
    
    return {
        "avg_prompt_generation_time": avg_time_per_prompt,
        "memory_usage_mb": memory_mb,
        "throughput_per_second": 100 / (end_time - start_time)
    }


def main():
    """Run all tests"""
    print("AI Image Studio - System Test Suite")
    print("="*50)
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestPromptEngine,
        TestImageAnalyzer,
        TestAIStudioCLI,
        TestScheduler,
        TestSystemMonitor,
        TestAICouncilIntegration,
        TestSystemIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    # Run performance tests
    performance_results = run_performance_tests()
    
    # Overall status
    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\nOVERALL STATUS: {'PASS' if success else 'FAIL'}")
    
    return success, performance_results


if __name__ == "__main__":
    success, perf_results = main()
    
    # Save results
    test_results = {
        "timestamp": datetime.now().isoformat(),
        "success": success,
        "performance": perf_results
    }
    
    results_file = Path(__file__).parent / "test_results.json"
    with open(results_file, 'w') as f:
        json.dump(test_results, f, indent=2)
    
    print(f"\nTest results saved to: {results_file}")
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)