import angr, claripy

p = angr.Project('high_quality_checks', auto_load_libs=False)

find = 0x00400ad2
avoid = 0x00400ae0

state = p.factory.entry_state()

# bvs_flag = claripy.BVS('sim_flag', 8*19)
# for c in bvs_flag.chop(8):
# 	state.solver.add(state.solver.Or(
#             state.solver.And(c <= '9', c >= '0'),
#             state.solver.And(c <= 'Z', c >= 'A'),
#             state.solver.And(c <= 'z', c >= 'a'),
#             c == '_',
#             c == '{',
#             c == '}',
#         ))

sim = p.factory.simulation_manager(state)
print('[*] running simulation')
sim.use_technique(angr.exploration_techniques.Explorer(find=find, avoid=avoid))
print(sim.run())

import code
code.interact(local=locals())
# flag_int = sim.found[0].solver.eval(bvs_flag)
# print(flag_int)
