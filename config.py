"""Configuration settings for the performance test."""

# Test Parameters
NUM_ITERATIONS = 1
CONCURRENT_REQUESTS = 1
TIMEOUT_SECONDS = 30  # Timeout for each request

# Model Configurations
ANTHROPIC_MODEL = "claude-3-7-sonnet-latest"

# Test Provider
TEST_PROVIDER = "anthropic"  # Options: "anthropic" or "bedrock"

# Test Scenarios
TEST_SCENARIOS = [
    {
        "name": "short_response",
        "prompt": "What is 2+2? Answer with just the number.",
        "description": "Testing short, quick responses"
    },
    {
        "name": "medium_response",
        "prompt": "Write a paragraph about artificial intelligence.",
        "description": "Testing medium-length responses"
    },
    {
        "name": "long_response",
        "prompt": "Write a detailed essay about the history of computing. Include at least 5 major milestones.",
        "description": "Testing long-form content generation"
    },
    {
        "name": "input_1k_tokens",
        "prompt": "word " * 1000,
        "description": "Testing with a 1,000 token input prompt"
    },
    {
        "name": "input_5k_tokens",
        "prompt": "word " * 5000,
        "description": "Testing with a 5,000 token input prompt"
    },
    {
        "name": "input_10k_tokens",
        "prompt": "word " * 10000,
        "description": "Testing with a 10,000 token input prompt"
    },
    {
        "name": "input_20k_tokens",
        "prompt": "word " * 20000,
        "description": "Testing with a 20,000 token input prompt"
    },
    {
        "name": "input_20_tokens",
        "prompt": "word " * 20,
        "description": "Testing with a 20 token input prompt"
    },
    {
        "name": "output_1k_tokens",
        "prompt": "Repeat the word 'echo' 1,000 times.",
        "description": "Prompt to generate about 1,000 output tokens",
        "max_tokens": 1000
    },
    {
        "name": "output_5k_tokens",
        "prompt": "Repeat the word 'echo' 5,000 times.",
        "description": "Prompt to generate about 5,000 output tokens",
        "max_tokens": 5000
    },
    {
        "name": "output_10k_tokens",
        "prompt": "Repeat the word 'echo' 10,000 times.",
        "description": "Prompt to generate about 10,000 output tokens",
        "max_tokens": 10000
    },
    {
        "name": "output_20k_tokens",
        "prompt": "Repeat the word 'echo' 20,000 times.",
        "description": "Prompt to generate about 20,000 output tokens",
        "max_tokens": 20000
    },
    {
        "name": "output_20_tokens",
        "prompt": "Repeat the word 'echo' 20 times.",
        "description": "Prompt to generate about 20 output tokens",
        "max_tokens": 20
    },
    {
        "name": "small_input_large_output_500",
        "prompt": "Say 'echo' 500 times.",
        "description": "Small input, request 500 output tokens",
        "max_tokens": 500
    },
    {
        "name": "small_input_large_output_1000",
        "prompt": "Say 'echo' 1,000 times.",
        "description": "Small input, request 1,000 output tokens",
        "max_tokens": 1000
    },
    {
        "name": "small_input_large_output_2000",
        "prompt": "Say 'echo' 2,000 times.",
        "description": "Small input, request 2,000 output tokens",
        "max_tokens": 2000
    },
]

# Output Configuration
OUTPUT_DIR = "test_results"
CHART_OUTPUT_DIR = "charts"

# API Configuration
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds between retries 