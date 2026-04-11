import subprocess

def main():
    subprocess.Popen("start cmd /k python -m engine.tests.test_game", shell=True)

if __name__ == '__main__':
    main()