import os
import time
import json
import asyncio
import logging
from datetime import datetime
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import anthropic
import boto3
from concurrent.futures import ThreadPoolExecutor
from config import *

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PerformanceTest:
    def __init__(self):
        self.anthropic_client = anthropic.AsyncAnthropic(
            api_key=os.getenv('ANTHROPIC_API_KEY')
        )
        
        self.bedrock_client = None
        if TEST_PROVIDER == "bedrock":
            self.bedrock_client = boto3.client(
                'bedrock-runtime',
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                region_name=os.getenv('AWS_REGION')
            )
        
        # Create output directories
        Path(OUTPUT_DIR).mkdir(exist_ok=True)
        Path(CHART_OUTPUT_DIR).mkdir(exist_ok=True)
        
        self.results = []

    async def test_anthropic_api(self, prompt, max_tokens=None):
        start_time = time.time()
        try:
            response = await self.anthropic_client.messages.create(
                model=ANTHROPIC_MODEL,
                max_tokens=max_tokens or 1000,
                messages=[{"role": "user", "content": prompt}]
            )
            end_time = time.time()
            input_tokens = getattr(response.usage, 'input_tokens', None)
            output_tokens = getattr(response.usage, 'output_tokens', None)
            logger.info(f"Input tokens: {input_tokens}, Output tokens: {output_tokens}")
            return {
                'success': True,
                'latency': end_time - start_time,
                'response': response.content[0].text,
                'provider': 'Anthropic',
                'input_tokens': input_tokens,
                'output_tokens': output_tokens,
                'model': ANTHROPIC_MODEL
            }
        except Exception as e:
            logger.error(f"Anthropic API error: {str(e)}")
            return {
                'success': False,
                'latency': time.time() - start_time,
                'error': str(e),
                'provider': 'Anthropic',
                'input_tokens': None,
                'output_tokens': None,
                'model': ANTHROPIC_MODEL
            }

    async def test_bedrock_api(self, prompt):
        start_time = time.time()
        try:
            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": prompt}]
            })
            
            response = self.bedrock_client.invoke_model(
                modelId=BEDROCK_MODEL,
                body=body
            )
            
            response_body = json.loads(response['body'].read())
            end_time = time.time()
            
            return {
                'success': True,
                'latency': end_time - start_time,
                'response': response_body['content'][0]['text'],
                'provider': 'Bedrock'
            }
        except Exception as e:
            logger.error(f"Bedrock API error: {str(e)}")
            return {
                'success': False,
                'latency': time.time() - start_time,
                'error': str(e),
                'provider': 'Bedrock'
            }

    async def run_concurrent_tests(self, scenario):
        tasks = []
        for _ in range(CONCURRENT_REQUESTS):
            if TEST_PROVIDER == "anthropic":
                max_tokens = scenario.get('max_tokens', None)
                tasks.append(self.test_anthropic_api(scenario['prompt'], max_tokens=max_tokens))
            elif TEST_PROVIDER == "bedrock":
                tasks.append(self.test_bedrock_api(scenario['prompt']))
        results = await asyncio.gather(*tasks)
        return results

    def analyze_results(self, scenario_results, scenario_name):
        df = pd.DataFrame(scenario_results)
        
        # Calculate statistics
        stats = df.groupby('provider').agg({
            'latency': ['mean', 'std', 'min', 'max'],
            'success': 'mean'
        }).round(3)
        
        # Plot results
        plt.figure(figsize=(10, 6))
        df.boxplot(column='latency', by='provider')
        plt.title(f'Response Time Distribution - {scenario_name}')
        plt.ylabel('Latency (seconds)')
        plt.savefig(f'{CHART_OUTPUT_DIR}/{scenario_name}_boxplot.png')
        plt.close()
        
        return stats

    def run_tests(self):
        summary_rows = []
        for scenario in TEST_SCENARIOS:
            logger.info(f"Running scenario: {scenario['name']}")
            
            all_results = []
            for iteration in range(NUM_ITERATIONS):
                logger.info(f"Iteration {iteration + 1}/{NUM_ITERATIONS}")
                
                # Run concurrent tests
                results = asyncio.run(self.run_concurrent_tests(scenario))
                all_results.extend(results)
            
            # Analyze and save results
            stats = self.analyze_results(all_results, scenario['name'])
            logger.info(f"\nResults for {scenario['name']}:\n{stats}")
            
            # Prepare summary row (use first successful result, or first result if all failed)
            result_row = next((r for r in all_results if r['success']), all_results[0] if all_results else None)
            if result_row:
                summary_rows.append({
                    'test_name': scenario['name'],
                    'model': result_row.get('model', ''),
                    'input_tokens': result_row.get('input_tokens', ''),
                    'output_tokens': result_row.get('output_tokens', ''),
                    'latency': round(result_row.get('latency', 0), 3),
                    'success': 'success' if result_row.get('success') else 'failed'
                })

        # Save summary CSV
        if summary_rows:
            summary_df = pd.DataFrame(summary_rows)
            summary_df.to_csv(f"{OUTPUT_DIR}/summary_results.csv", index=False)

def main():
    logger.info("Starting performance tests...")
    test = PerformanceTest()
    test.run_tests()
    logger.info("Performance tests completed!")

if __name__ == "__main__":
    main() 