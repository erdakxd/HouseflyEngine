import subprocess

def main():
    subprocess.Popen("start cmd.exe /k python -m engine.tests.test_main", shell=True)

if __name__ == '__main__':
    main()