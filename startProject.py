from parserCarPlatform.createProcess import Creator
import sys
if __name__ == '__main__':
    typeStep = sys.argv[1]
    obj = Creator(typeStep)
    obj.run()