# Claude Performance Test

This project performs performance testing of Claude models hosted on Anthropic vs AWS Bedrock. It measures and compares:
- Response times
- Throughput
- Token processing speed
- Cost efficiency

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
Create a `.env` file with:
```
ANTHROPIC_API_KEY=your_anthropic_key
AWS_ACCESS_KEY_ID=your_aws_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION=your_aws_region
```

3. Run the test:
```bash
python performance_test.py
```

## Test Configuration

The test can be configured through `config.py`. You can modify:
- Number of test iterations
- Prompt sizes
- Test scenarios
- Model versions
- Concurrent requests

## Output

The test generates:
- CSV files with raw performance data
- Performance comparison charts
- Statistical analysis of results 