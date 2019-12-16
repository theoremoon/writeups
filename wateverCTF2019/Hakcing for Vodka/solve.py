import angr
import claripy

p = angr.Project("./vodka", load_options={"auto_load_libs": False})


class PHook(angr.SimProcedure):
    def run(self, args):
        return claripy.BVV(0, 64)


p.hook_symbol("ptrace", PHook())

state = p.factory.entry_state()
simgr = p.factory.simulation_manager(state)
simgr.explore(find=0x400000 + 0xC4F)

try:
    print(simgr.found[0].posix.dumps(0))
except:
    print("Not found")
