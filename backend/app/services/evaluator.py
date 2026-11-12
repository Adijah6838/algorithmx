import subprocess
import time
import tempfile
import os
from sqlalchemy.orm import Session
from app.models.submission import Submission, SubmissionStatus, Language
from app.models.problem import TestCase

def evaluate_submission(submission_id: int, db: Session):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        return

    test_cases = db.query(TestCase).filter(TestCase.problem_id == submission.problem_id).all()
    if not test_cases:
        submission.status = SubmissionStatus.ACCEPTED
        db.commit()
        return

    # Create a temporary directory to run the code safely
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = ""
        compile_cmd = []
        run_cmd = []

        # 1. Setup the code file based on language
        if submission.language == Language.PYTHON:
            file_path = os.path.join(temp_dir, "main.py")
            run_cmd = ["python", file_path]
        elif submission.language == Language.CPP:
            file_path = os.path.join(temp_dir, "main.cpp")
            exe_path = os.path.join(temp_dir, "main.exe")
            run_cmd = [exe_path]
            compile_cmd = ["g++", file_path, "-o", exe_path]
        elif submission.language == Language.JAVA:
            file_path = os.path.join(temp_dir, "Main.java")
            run_cmd = ["java", "-cp", temp_dir, "Main"]
            compile_cmd = ["javac", file_path]
        
        with open(file_path, "w") as f:
            f.write(submission.code)

        # 2. Compile (if necessary)
        if compile_cmd:
            compile_process = subprocess.run(compile_cmd, capture_output=True, text=True)
            if compile_process.returncode != 0:
                submission.status = SubmissionStatus.COMPILATION_ERROR
                submission.error_message = compile_process.stderr
                db.commit()
                return

        # 3. Run against test cases
        max_time = 2.0 # Time limit: 2 seconds
        
        for tc in test_cases:
            start_time = time.time()
            try:
                process = subprocess.run(
                    run_cmd, 
                    input=tc.input_data, 
                    capture_output=True, 
                    text=True, 
                    timeout=max_time
                )
                execution_time = time.time() - start_time
                
                if process.returncode != 0:
                    submission.status = SubmissionStatus.RUNTIME_ERROR
                    submission.error_message = process.stderr
                    db.commit()
                    return

                # Compare output (strip to ignore trailing newlines/spaces)
                actual_output = process.stdout.strip()
                expected_output = tc.expected_output.strip()
                
                if actual_output != expected_output:
                    submission.status = SubmissionStatus.WRONG_ANSWER
                    db.commit()
                    return

                submission.execution_time = max(submission.execution_time or 0, execution_time)

            except subprocess.TimeoutExpired:
                submission.status = SubmissionStatus.TIME_LIMIT_EXCEEDED
                db.commit()
                return

        # If we made it here, all test cases passed!
        submission.status = SubmissionStatus.ACCEPTED
        db.commit()
