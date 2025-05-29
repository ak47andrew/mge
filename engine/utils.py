class PriorityList[T]:
    data: list[tuple[T, int]]
    # --- Magic methods ----
    def __init__(self):
        self.data = []

    def __iter__(self):
        return iter(self.data)

    # --- Public methods ---
    def add(self, item: T, priority: int) -> None:
        index = self._binary_search((item, priority))
        self.data.insert(index, (item, priority))

    def get(self, item: T) -> tuple[T, int] | None:
        for i, (x, priority) in enumerate(self.data):
            if x == item:
                return x, priority
        return None

    def remove(self, item: T) -> None:
        self.data.remove(self.get(item))

    # ---- Util methods ----

    def _binary_search(self, item: tuple[T, int]) -> int:
        low, high = 0, len(self.data)
        while low < high:
            mid = (low + high) // 2
            if self.data[mid][1] < item[1]:  # Compare the integer part
                low = mid + 1
            else:
                high = mid
        return low
