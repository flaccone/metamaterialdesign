import nlopt
import numpy as np
from tiledopt import TiledSimulation
from patterns import MyPattern

class Optimization:
    def __init__(self, x, opt_lb, opt_ub):
        self.x = x
        self.opt_lower_bounds = opt_lb
        self.opt_upper_bounds = opt_ub
        self.optimize()

    def optimize(self):
        opt = nlopt.opt(nlopt.LN_BOBYQA, len(self.x))
        opt.set_lower_bounds(self.opt_lower_bounds)
        opt.set_upper_bounds(self.opt_upper_bounds)

        opt.set_min_objective(f)

        opt.set_lower_bounds(self.opt_lower_bounds)
        opt.set_upper_bounds(self.opt_upper_bounds)

        opt.set_ftol_rel(1e-3)
        opt.set_maxeval(50)
        opt.set_xtol_rel(1e-3)

        xopt = opt.optimize(self.x)
        opt_val = opt.last_optimum_value()
        num_evals = opt.get_numevals()

        print('Optimum at: ', xopt)
        print('Optimum value: ', opt_val, ', Number of evaluations: ', num_evals, ', Result code = ', opt.last_optimize_result())

        self.xopt = xopt


def f(x, grad=None):
        target_displacement = [26.64488129600715,40.492252078934584, 42.240157688665285, 27.375365131812124]
        target_roller_displ = [10]
        patterns_list = []
        for i in range(len(x)):
            p = MyPattern(my_design_parameter = x[i])
            patterns_list.append(p)
        til = TiledSimulation(patterns_list)
        print('Displacement norms of tile centers: ', til.displ) #'Roller y-translation: ', til.transl_roller)

        f_x = abs( np.sum(np.square( np.array(til.displ) - np.array(target_displacement) ) ) ) #+ 2 * (til.transl_roller - target_roller_displ)
        print('Objective function: ', f_x)
        return f_x