import angr, claripy

p = angr.Project("leakage")


flag = claripy.BVS("sim_flag", 8 * 0x22)

state = p.factory.entry_state(args=[p.filename, flag])

for c in flag.chop(8):
    state.add_constraints(c >= " ")
    state.add_constraints(c <= "~")

sim = p.factory.simulation_manager(state)
sim.explore(find=0x4006AE, avoid=[0x4006BC])
print(sim.run())

import code

code.interact(local=locals())
