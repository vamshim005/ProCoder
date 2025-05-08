import os
import subprocess
import tempfile

LANGUAGE_CONFIG = {
    'c': {
        'image': 'gcc:latest',
        'compile': 'gcc /code/code.c -o /code/a.out',
        'run': '/code/a.out',
        'source_name': 'code.c'
    },
    'cpp': {
        'image': 'gcc:latest',
        'compile': 'g++ /code/code.cpp -o /code/a.out',
        'run': '/code/a.out',
        'source_name': 'code.cpp'
    },
    'python2': {
        'image': 'python:2.7',
        'run': 'python /code/code.py',
        'source_name': 'code.py'
    },
    'python3': {
        'image': 'python:3.8',
        'run': 'python /code/code.py',
        'source_name': 'code.py'
    },
    'java': {
        'image': 'openjdk:latest',
        'compile': 'javac /code/Main.java',
        'run': 'java -cp /code Main',
        'source_name': 'Main.java'
    }
}

def judge_submission(submission, test_cases):
    verdict = 'Accepted'
    details = []
    for idx, tc in enumerate(test_cases):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Save code file
            code_path = os.path.join(tmpdir, LANGUAGE_CONFIG[submission.language]['source_name'])
            with open(code_path, 'wb') as f:
                if getattr(submission, 'code_text', None):
                    f.write(submission.code_text.encode())
                else:
                    f.write(submission.code_file.read())
            # Save input file
            input_path = os.path.join(tmpdir, 'input.txt')
            with open(input_path, 'w') as f:
                f.write(tc['input'])
            # Prepare Docker command
            image = LANGUAGE_CONFIG[submission.language]['image']
            compile_cmd = LANGUAGE_CONFIG[submission.language].get('compile')
            run_cmd = LANGUAGE_CONFIG[submission.language]['run']
            docker_run = [
                'docker', 'run', '--rm',
                '-v', f'{tmpdir}:/code',
                '--network', 'none',
                '--memory', '128m',
                '--cpus', '0.5',
                image
            ]
            # Compile if needed
            if compile_cmd:
                compile_proc = subprocess.run(
                    docker_run + compile_cmd.split(),
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                if compile_proc.returncode != 0:
                    verdict = 'Compilation Error'
                    details.append(f'Test case {idx+1}: Compilation Error\n{compile_proc.stderr.decode()}')
                    break
            # Run
            try:
                run_proc = subprocess.run(
                    docker_run + run_cmd.split(),
                    stdin=open(input_path),
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    timeout=2
                )
                output = run_proc.stdout.decode().strip()
                if run_proc.returncode != 0:
                    verdict = 'Runtime Error'
                    details.append(f'Test case {idx+1}: Runtime Error\n{run_proc.stderr.decode()}')
                    break
            except subprocess.TimeoutExpired:
                verdict = 'Time Limit Exceeded'
                details.append(f'Test case {idx+1}: Time Limit Exceeded')
                break
            # Compare output
            expected = tc['output'].strip()
            if output != expected:
                verdict = 'Wrong Answer'
                details.append(f'Test case {idx+1}: Wrong Answer\nExpected: {expected}\nGot: {output}')
                break
            details.append(f'Test case {idx+1}: Passed')
    return verdict, '\n'.join(details) 