
import os, sys

def runtestdir(subdir):
    test_files = [
        f for f in os.listdir(subdir)
        if f.startswith("test_") and f.endswith(".py")
    ]
    errs = 0
    for f in test_files:
        test_file = os.path.join(subdir, f)
        print >> sys.stderr, "FILE:", test_file
        exit_code = os.system(sys.executable + " " + test_file)
        if exit_code != 0:
            errs += 1
    print >> sys.stderr, "SUMMARY: %s -> %s total / %s error (%s)" \
        % (subdir, len(test_files), errs, sys.executable)


if __name__ == "__main__":
    PROJECT_DIR = os.path.abspath(os.path.dirname( __file__ ))
    os.chdir(PROJECT_DIR)
    os.environ["PYTHONPATH"] = PROJECT_DIR
    runtestdir("rafttest")

