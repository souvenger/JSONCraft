import unittest
import coverage
from json_parser import tokenizer, parser, is_valid_json

# Start coverage measurement
cov = coverage.Coverage()
cov.start()

test_files = [
    "tests/step1/valid.json",
    "tests/step1/invalid.json",
    "tests/step2/invalid2.json",
    "tests/step2/valid.json",
    "tests/step2/valid2.json",
    "tests/step3/invalid.json",
    "tests/step3/valid.json",
    "tests/step4/valid.json",
    "tests/step4/valid2.json",
    "tests/step4/invalid.json",
]


class TestJsonParser(unittest.TestCase):
    def test_valid_json(self):
        for json_file_path in test_files:
            if "invalid" in json_file_path:
                print("Invalid")
                with self.subTest(json_file_path=json_file_path):
                    with open(f"json_parser/{json_file_path}", "r") as file:
                        json_content = file.read().replace("\n", "")
                        print(f"Content of {json_file_path}:\n{json_content}")
                    flag = is_valid_json(str(json_content))
                    self.assertEqual(flag, False)
            else:
                print("Valid")
                with self.subTest(json_file_path=json_file_path):
                    with open(f"json_parser/{json_file_path}", "r") as file:
                        json_content = file.read().replace("\n", "")
                        print(f"Content of {json_file_path}:\n{json_content}")
                    flag = is_valid_json(str(json_content))
                    self.assertEqual(flag, True)


# Generate coverage report
cov.report()

if __name__ == "__main__":
    unittest.main()
