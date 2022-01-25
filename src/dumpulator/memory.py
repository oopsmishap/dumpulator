from enum import Enum

class State(Enum):
    Free = 0
    Reserved = 1
    Committed = 2

class Protect(Enum):
    NoAccess = 0
    Read = 1
    ReadWrite = 2
    ReadExecute = 3
    ReadWriteExecute = 4

class Page:
    def __init__(self, start: int, end: int, state: State, protect: Protect):
        self.start = start
        self.end = end
        self.state = state
        self.protect = protect

    @property
    def size(self):
        return self.end - self.start

    def __contains__(self, addr):
        return self.start <= addr < self.end

# TODO: KUSER_SHARED_DATA can't be changed, PEB/TEB page protection can't be changed
class VirtualMemory:
    def __init__(self, start: int = 0, end: int = 0x10000000000000000):
        self.start = start
        self.end = end
        self.pages = [Page(start, end, State.Free, Protect.NoAccess)]

    def find_page_index(self, addr):
        for i in range(0, len(self.pages)):
            if addr in self.pages[i]:
                return i
        raise Exception(f"Address {addr:016x} not found in virtual memory")

    def reserve(self, addr, size):
        index = self.find_page_index(addr)
        page = self.pages[index]
        end = addr + size
        assert end <= page.end
        assert page.state == State.Free

        insert = []
        if addr > page.start:
            insert.append(Page(page.start, addr, page.state, page.protect))
        insert.append(Page(addr, end, State.Reserved, Protect.NoAccess))
        if end < page.end:
            insert.append(Page(end, page.end, page.state, page.protect))

        self.pages.pop(index)
        self.pages[index:len(insert)] = insert

    def release(self, addr, size):
        index = self.find_page_index(addr)
        page = self.pages[index]
        end = addr + size
        assert end <= page.end
        assert page.state != State.Free

        insert = []
        if page.start < addr:
            insert.append(Page(page.start, addr, page.state, page.protect))
        insert.append(Page(addr, end, State.Free, Protect.NoAccess))
        if page.end > end:
            insert.append(Page(end, page.end, page.state, page.protect))

        self.pages.pop(index)
        self.pages[index:len(insert)] = insert

        # TODO: merge free pages
        print(f"index: {index}")

        for i in range(max(index - 1, 0), len(self.pages)):
            if self.pages[i].state != State.Free:
                break
            print(f"{i}")

    def commit(self, addr, size, protect):
        pass

    def decommit(self, addr, size):
        pass

    def find_free(self, size):
        pass

    def __str__(self):
        result = ""
        for page in self.pages:
            if len(result) > 0:
                result += "\n"
            end = page.end
            if end == 0x10000000000000000 or end == 0x100000000:
                end -= 1
            result += f"{page.start:016x}-{end:016x}:{page.state}"
        return result
