import traceback

try:
    from .parser import parse, eval
except ImportError:
    from parser import parse, eval
import asyncio

async def solve(expression):
    return parse(expression)

if __name__ == "__main__":
    while True:
        expr = input("> ")
        
        try:
            print(asyncio.get_event_loop().run_until_complete(solve(expr)))
        except Exception as e:
            print(str(e))
            traceback.print_tb(e.__traceback__)
            print(dir(e))