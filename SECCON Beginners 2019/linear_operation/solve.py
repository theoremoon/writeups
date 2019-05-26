import angr, claripy

p = angr.Project("linear_operation")


flag = claripy.BVS("sim_flag", 8 * 0x63)

state = p.factory.entry_state(stdin=flag)

for c in flag.chop(8):
    state.add_constraints(c >= " ")
    state.add_constraints(c <= "~")

sim = p.factory.simulation_manager(state)
sim.explore(find=0x40CF78, avoid=[0x40CF86])
print(sim.run())

import code

code.interact(local=locals())
