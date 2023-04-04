import numpy as np
import ray

ray.init(num_cpus=16)


@ray.remote
def mul(x):
    return x * 10


arr = np.random.random(1000000)
arr = ray.put(arr)
result = ray.get(mul.remote(arr))