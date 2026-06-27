import argparse as arg 



if __name__ == "__main__":
    parsargs = arg.ArgumentParser()
    parsargs.add_argument("--output", "takes the output file path",  default="data/output/function_calls.json")
    parsargs.add_argument("--input", "takes inputs file path", default="data/input/function_calling_tests.json")

