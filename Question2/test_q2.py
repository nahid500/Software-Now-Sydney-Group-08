from evaluator import evaluate_file

try:
    result = evaluate_file("sample_input.txt")
    print(result)
except Exception as e:
    print(f"Error: {e}")