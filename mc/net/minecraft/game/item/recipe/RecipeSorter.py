class RecipeSorter:

    def __init__(self, craftingManager):
        pass

    def compare(self, recipe1, recipe2):
        if recipe2.getSize() < recipe1.getSize():
            return -1
        elif recipe2.getSize() > recipe2.getSize():
            return 1
        else:
            return 0
