import os
import sys
import argparse


# P1
from practice1_code import caesar, affine, vigenere, monoalpha
from practice1_code.assist import report
from practice1_code.break_caesar import break_caesar
from practice1_code.break_affine import break_affine
from practice1_code.break_vigenere import break_vigenere

# P2
import railfence 
import columnar 
from measure import index_of_coincidence as ic, classify
from kasiski import factor_tally

def read_input(args) -> str:
    if args.in_file:
        if os.path.isfile(args.in_file):
            with open(args.in_file, 'r') as f:
                return f.read().strip()
        else:
            raise FileNotFoundError(2, "No such file or directory", args.in_file)
    return sys.stdin.read().strip()

def write_output(args, text: str) -> None:
    if hasattr(args, 'out_file') and args.out_file:
        with open(args.out_file, 'w') as f:
            f.write(text)
    else:
        print(text)

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="crypto.py")
    subparsers = parser.add_subparsers(dest="cipher", required = True)

    # P1 - Caesar
    caesar_parser = subparsers.add_parser("caesar")
    caesar_parser.add_argument("mode", choices= ["encrypt", "decrypt"])
    caesar_parser.add_argument("--key", type = int, required = True)
    caesar_parser.add_argument("--in", dest = 'in_file', default = None)
    caesar_parser.add_argument("--out", dest = 'out_file', default = None)

    # P1 - Affine
    affine_parser = subparsers.add_parser("affine")
    affine_parser.add_argument("mode", choices= ["encrypt", "decrypt"])
    affine_parser.add_argument("--a", type = int, required = True)
    affine_parser.add_argument("--b", type = int, required = True)
    affine_parser.add_argument("--in", dest = 'in_file', default = None)
    affine_parser.add_argument("--out", dest = 'out_file', default = None)

    # P1 - Monoalpha
    mono_parser = subparsers.add_parser("mono")
    mono_parser.add_argument("mode", choices= ["encrypt", "decrypt"])
    mono_parser.add_argument("--key", type = str)
    mono_parser.add_argument("--keyword", type = str)
    mono_parser.add_argument("--in", dest = 'in_file', default = None)
    mono_parser.add_argument("--out", dest = 'out_file', default = None)

    # P1 - Vigenère
    vig_parser = subparsers.add_parser("vigenere")
    vig_parser.add_argument("mode", choices = ["encrypt", "decrypt"])
    vig_parser.add_argument("--key", type = str, required = True)
    vig_parser.add_argument("--in", dest= "in_file", default = None)
    vig_parser.add_argument("--out", dest= "out_file", default = None)

    # P1 - Break
    break_parser = subparsers.add_parser("break")
    break_parser.add_argument("target", choices = ["caesar", "affine", "vigenere"])
    break_parser.add_argument("--m", type = int)
    break_parser.add_argument("--in", dest = "in_file", default = None)
    break_parser.add_argument("--out", dest = "out_file", default = None)
    break_parser.add_argument("--lang", default = "en")

    # P1 - Assist
    assist_parser = subparsers.add_parser("assist")
    assist_parser.add_argument("--in", dest= "in_file", default = None)
    assist_parser.add_argument("--out", dest= "out_file", default = None)
    assist_parser.add_argument("--lang", default = "en")

    # P2 - Railfence
    rf_parser = subparsers.add_parser("railfence")
    rf_parser.add_argument("mode", choices= ["encrypt", "decrypt"])
    rf_parser.add_argument("--rails", type = int, required=True)
    rf_parser.add_argument("--in", dest="in_file", required=True)
    rf_parser.add_argument("--out", dest= "out_file", default=None)

    # P2 - Measure
    m_parser = subparsers.add_parser("measure")
    m_sub = m_parser.add_subparsers(dest="metric", required=True)

    ic_p = m_sub.add_parser("ic")
    ic_p.add_argument("--in", dest="in_file", required=True)

    class_p = m_sub.add_parser("classify")
    class_p.add_argument("--in", dest="in_file", required=True)
    class_p.add_argument("--lang", choices=["en", "es"], default="en")

    kas_p = m_sub.add_parser("kasiski")
    kas_p.add_argument("--in", dest="in_file", required=True)

    return parser

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.cipher == "caesar":
            text = read_input(args)
            if args.key is None:
                raise ValueError("caesar requires key.")
                
            if args.mode == "encrypt":
                write_output(args, caesar.encrypt(text, args.key))
            else:
                write_output(args, caesar.decrypt(text, args.key))

        elif args.cipher == "affine":
            text = read_input(args)
            if args.a is None or args.b is None:
                raise ValueError("affine requires a & b.")
                
            if args.mode == "encrypt":
                write_output(args, affine.encrypt(text, args.a, args.b))
            else:
                write_output(args, affine.decrypt(text, args.a, args.b))

        elif args.cipher == "mono":
            text = read_input(args)
            if args.keyword:
                key = monoalpha.key_from_keyword(args.keyword)
            elif args.key:
                key = args.key
            else:
                raise ValueError("mono requires a key or keyword")
                
            if args.mode == "encrypt":
                write_output(args, monoalpha.encrypt(text,key))
            else:
                write_output(args, monoalpha.decrypt(text,key))

        elif args.cipher == "vigenere":
            text = read_input(args)
            if args.key is None:
                raise ValueError("vigenere requires key")
                
            if args.mode == "encrypt":
                write_output(args, vigenere.encrypt(text, args.key))
            else:
                write_output(args, vigenere.decrypt(text, args.key))

        elif args.cipher == "break":
            text = read_input(args)
            
            if args.target == "caesar":
                k, plain = break_caesar(text, args.lang)
                write_output(args, f"k={k}\n{plain}")
                
            elif args.target == "affine":
                key, plain = break_affine(text, args.lang)
                write_output(args, f"key={key}\n{plain}")

            elif args.target == "vigenere":
                if args.m is None:
                    raise ValueError("break vigenererequires m")
                key, plain = break_vigenere(text, args.m, args.lang)
                write_output(args, f"k={key}\n{plain}")

        elif args.cipher == "assist":
            text = read_input(args)
            write_output(args, report(text, args.lang))

        # P2
        elif args.cipher == "railfence":
            text = read_input(args)
            if args.mode == "encrypt":
                write_output(args, railfence.encrypt(text, args.rails))
            else:
                write_output(args, railfence.decrypt(text, args.rails))

        elif args.cipher == "columnar":
            text = read_input(args)
            if args.mode == "encrypt":
                write_output(args, columnar.encrypt(text, args.key))
            else:
                write_output(args, columnar.decrypt(text, args.key))

        elif args.cipher == "measure":
            text = read_input(args)
            if args.metric == "ic":
                write_output(args, f"{ic(text):.4f}")
            elif args.metric == "classify":
                write_output(args, classify(text, language=args.lang))
            elif args.metric == "kasiski":
                tally = factor_tally(text)
                write_output(args, str(tally))

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Error: File not found: {e.filename}", file = sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
                

    
    
    