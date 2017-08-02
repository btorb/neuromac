"""
This example growth rule illustrates how to set up a growth cone,
compute directions and use repulsion with respect to other parts
(such as the soma)
"""

from growth_procs import unit_sample_on_sphere,\
     normalize_length,\
     prepare_next_front,\
     direction_to

L_NORM = 5.0

"""
extend_front is the obligatory method. NeuroMac will call this method
of any cell_type specified in the config file.
 
- Do not change the arguments of this function.
- This function ALWAYS has to return a list of

Have a look at the API:
http://b-torbennielsen.home.oist.jp/neuromac/api.html

NeuroMac comes with some auxiliary functions to orient growth cones.
These helper functions are also described in the API.
"""
def extend_front(front,seed,constellation,interstitial) :
    # at the very beginning. See soma is the growth cone. 
    if front.order == 0:
        new_fronts = []
        for i in range(5): # 5 stems
            rnd_dir = unit_sample_on_sphere() # in random directions
            new_pos = normalize_length(rnd_dir,L_NORM)
            new_pos = front.xyz + new_pos
            new_front = prepare_next_front(front,new_pos,set_radius=1.0,add_order=True)
            new_fronts.append(new_front)
        return new_fronts
            
    else:
        rnd_dir = unit_sample_on_sphere() # random direction
        heading = front.xyz - front.parent.xyz # current heading
        soma_dir = -1.0 * normalize_length(\
           direction_to(front,[front.soma_pos],what="nearest"),1.0) #-1: away from soma

        new_dir = normalize_length(heading,1.0) + 10.0*soma_dir + 1.0*rnd_dir
        new_pos = front.xyz + normalize_length(new_dir,L_NORM)
        
        # rnd_dir = unit_sample_on_sphere()
        # new_pos = normalize_length(rnd_dir,L_NORM)
        # new_pos = front.xyz + new_pos
        new_front = prepare_next_front(front,new_pos,set_radius=1.0)
        return [new_front]
